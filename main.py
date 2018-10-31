import server
import game

connections = startServer()
game = Game(connections)
game.setUpGames()