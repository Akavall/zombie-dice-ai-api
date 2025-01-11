import uuid
from typing import Dict, List
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse, JSONResponse
import os
import lightgbm as lgb
import pandas as pd
import logging

from zombie_dice.zombie_dice import PlayerState, GameState, Player, init_game_state, init_player_state
from model.monte_carlo import reformat_game_state_b
from api.utils import load_model

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = FastAPI()

MODEL = load_model()

PATH_TO_MODEL = os.getenv("PATH_TO_MODEL")

@app.get("/zombie_dice")
def serve_index():
    """
    When someone visits "/", return the zombie_dice.html file.
    """

    file_path = os.path.join(os.path.dirname(__file__), "zombie_dice.html")
    return FileResponse(file_path, media_type="text/html")

games: Dict[str, "GameState"] = {}

@app.post("/zombie_dice/start_game")
def start_game():
    # Build a list of (name, is_ai) based on how many players we want
    # This is minimal logic: you can expand for more players if needed
    
    player_a = Player(init_player_state(), "You", False, 0)
    player_b = Player(init_player_state(), "AI Player", True, 0)

    players = [player_a, player_b]

    game_uuid = str(uuid.uuid4())
    game_state = init_game_state(players, game_uuid)

    games[game_uuid] = game_state

    logging.info(f"Game created: {game_uuid}")
    logging.info(f"Number of games stored: {len(games)}")

    return game_uuid

@app.post("/zombie_dice/take_turn")
def take_turn(request: Request):
    """
    Handles a turn in the Zombie Dice game.
    """

    bool_mapper = {"false": False, "true": True}

    qp = request.query_params
    uuid = qp.get("uuid")
    player_id = qp.get("player_id")
    should_continue = qp.get("continue") 

    if should_continue not in bool_mapper:
        message = f"Invalid value for should_continue: {should_continue}"
        logging.error(message)
        raise HTTPException(status_code=400, detail=message)

    should_continue = bool_mapper[should_continue]

    if uuid.startswith('"') and uuid.endswith('"'):
        uuid = uuid.strip('"')

    if uuid not in games:
        message = "Game not found"
        logging.error(message)
        raise HTTPException(status_code=400, detail=message)

    game_state = games[uuid]
    player_id_to_player = {player.id: player for player in game_state.players}

    if player_id not in player_id_to_player:
        message = "Player not found"
        logging.error(message)
        raise HTTPException(status_code=400, detail=message)

    player = player_id_to_player[player_id]

    if player.is_ai:

        features_move, cols_move = reformat_game_state_b(game_state, 1)
        features_not_move, cols_not_move = reformat_game_state_b(game_state, 0)

        move_df = pd.DataFrame(data=[features_move], columns=cols_move)
        not_move_df = pd.DataFrame(data=[features_not_move], columns=cols_not_move)

        move_score = MODEL.predict(move_df)
        not_move_score = MODEL.predict(not_move_df)

        # Log the detailed AI state in debug mode
        debug_info = {
            "game_id": uuid,
            "cols_move": cols_move,
            "cols_not_move": cols_not_move,
            "features_move": features_move,
            "features_not_move": features_not_move,
            "path_to_model": PATH_TO_MODEL,
        }
        logging.debug(f"Detailed AI State: {debug_info}")

        # Model A optimizes positive score
        # Model B optimizes negative score

        # This is assuming model B, since AI moves 2nd
        if move_score < not_move_score:
            should_continue = True 
        else:
            should_continue = False

    turn_data = {}

    if should_continue:

        turn_result = player.take_turn(game_state.zombie_deck)

    else:

        turn_result = [["", ""], ["", ""], ["", ""]]

    turn_data["TurnResult"] = turn_result
    turn_data["PlayerId"] = player_id
    turn_data["TimesShot"] = player.player_state.times_shot
    turn_data["RoundScore"] = player.player_state.current_score
    turn_data["IsDead"] = player.player_state.is_dead
    turn_data["TotalScore"] = player.total_score
    turn_data["ContinueTurn"] = should_continue

    if not player.is_ai:    
        if player.player_state.is_dead or should_continue is False:
            game_state.end_turn()
    else:
        if player.player_state.is_dead or should_continue is False:
            game_state.end_turn()
            game_state.end_round()

    if game_state.winner:
        turn_data["Winner"] = game_state.winner.id
    else:
        turn_data["Winner"] = ""

    return JSONResponse(turn_data)
