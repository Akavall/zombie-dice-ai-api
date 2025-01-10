
### What is Zombie Dice?**

Zombie Dice is a push-your-luck dice game where players try to collect as many brains as possible without getting shot three times. Each turn, players roll dice representing humans (green, yellow, or red), and each die type has different probabilities for outcomes: brains, footsteps, and shotguns. The player who collects 13 brains first wins the game.

### AI Approach to Zombie Dice**

### Pure Monte Carlo strategy


### Data Generation
We simulate **N=25,000** games at random, collecting features. We designate Player A as the first mover and Player B as the second mover. The AI focuses on decision-making from Player B's perspective.

### Features
At each turn, we extract the following game and player state features:
- `player_a_total_score`: Total score of Player A.
- `player_b_total_score`: Total score of Player B.
- `player_b_current_score`: Current score of Player B for the ongoing turn.
- `player_b_times_shot`: Number of times Player B has been "shot" in the current turn.
- `player_b_n_green_walks`: Number of green dice showing "walk".
- `player_b_n_yellow_walks`: Number of yellow dice showing "walk".
- `player_b_n_red_walks`: Number of red dice showing "walk".
- `green_dice_left`: Number of green dice remaining in the deck.
- `yellow_dice_left`: Number of yellow dice remaining in the deck.
- `red_dice_left`: Number of red dice remaining in the deck.

Additionally, for each turn, we evaluate two possible actions:
- `will_move`: Whether Player B will continue their turn (`True`) or stop (`False`).

### Target Variable
The ultimate outcome of the game is recorded as the target:
- `1`: Player A wins.
- `-1`: Player B wins.

### Model Training
We train a **LightGBM regression model** to predict the game's outcome based on the extracted features. During training, we evaluate two feature sets for each game state:
- **Set 1**: `will_move = True`
- **Set 2**: `will_move = False`

All other features remain consistent between these sets.

### AI Agent Decision Process
During gameplay, the AI evaluates the two feature sets using the trained model:
- `Model(set 1)`: Predicted outcome if the AI continues its turn.
- `Model(set 2)`: Predicted outcome if the AI stops its turn.

The AI chooses to continue if:

```plaintext
Model(set 1) < Model(set 2)
```

Otherwise the AI Agent ends the turn. Most of this logic is implemented in models/monte_carlo.py


### Self Player Reinforcement Learning (Exploratory)

While the pure Monte Carlo strategy has proven effective, relying solely on random moves can be inefficient, as it often explores many improbable paths. A more focused approach involves training against a rule-based, relatively intelligent agent.

This strategy leverages the same features and model architecture described earlier. However, learning occurs iteratively: a new model plays games against the rule-based opponent, generating gameplay data from these matches. The resulting data is added to the training set, and the model is updated incrementally. This process continues while monitoring performance against the rule-based agent to assess improvements.

This iterative logic is implemented in /model/self_play_rl_mc.py.


### Evaluation Strategy

We compared how the Pure MC model that is trained on 25000 games compares against a rule based model, where an agent keeps moving until they have been shot twice, if they agent was shot twice the agent stops. 

The Pure MC model beats this agent about 57% of the time. 

This code is implemented in model/matches.py


### How can Zombie Dice be deployed to API

The repo also provides a way to play Zombie Dice against the agent in an API locally or deploy the API remotly using docker. 

the /api directory provides the server logic and very simple code for UI.