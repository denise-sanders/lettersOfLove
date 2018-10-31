# Letters of Love

I really like this game and I wanted to play this game with my friends who live far away.


## TODO

implement client connection logic (each player gets a connection object I guess, maybe a thread listens to each one)
make a function to send messages to players, different messages if they are player or opponent or bystander
make a function to wait for and get input from the current player
add rules instructions

## Phases

player connection phase: socket listens for more connections, until player 1 says there are enough.
game plays
when the game is over, it asks to play again, or exit.