import uuid
import random
from typing import Dict, List
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

import os
import uuid

from zombie_dice.zombie_dice import PlayerState, GameState, Player, init_game_state, init_player_state

app = FastAPI()

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

    return game_uuid


@app.post("/zombie_dice/take_turn")
def take_turn(request: Request):
    """
    In the .html:
      $.post("/zombie_dice/take_turn?uuid=" + game_state_id + 
             "&player=You&continue=true", ...)
    We'll interpret 'continue=true' to mean "roll," and 'continue=false' to mean "stop turn."
    We then return JSON that parseTurnData can use.
    """


    bool_mapper = {"false": False, "true": True}


    qp = request.query_params
    uuid = qp.get("uuid")
    player_id = qp.get("player_id")
    should_continue = qp.get("continue") 

    if should_continue not in bool_mapper:
        raise HTTPException(status_code=404, detail=f"Invalid value for should_continue: {should_continue}")

    should_continue = bool_mapper[should_continue]

    if uuid.startswith('"') and uuid.endswith('"'):
        uuid = uuid.strip('"')

    if uuid not in games:
        raise HTTPException(status_code=404, detail="Game not found")

    game_state = games[uuid]
    player_id_to_player = {player.id: player for player in game_state.players}

    if player_id not in player_id_to_player:
        raise HTTPException(status_code=404, detail="Player not found")

    player = player_id_to_player[player_id]

    if player.is_ai:

        # implement AI logic here

        if random.choice([0, 1]) == 0:
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
