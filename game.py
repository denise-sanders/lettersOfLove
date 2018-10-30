# make a server, and a client.

import flask
import random
import copy

class Player:
	def __init__(self, name):
		self.name = name
		self.card = None
		self.roundsWon = 0

class Card:
	def __init__(self, name):
		self.name = name

		# could return which player loses, or none. If I can modify a players caerd Im good.
		if name == "guard":
			self.value = 1
			self.action = Game.guardAction	
		elif name == "priest":
			self.value = 2
			self.action = Game.priestAction
		elif name == "baron":
			self.value = 3
			self.action = Game.baronAction
		elif name == "handmaid":
			self.value = 4
			self.action = Game.handmaidAction
		elif name == "prince":
			self.value = 5
			self.action = Game.princeAction
		elif name == "king":
			self.value = 6
			self.action = Game.kingAction
		elif name == "countess":
			self.value = 7
			self.action = Game.countessAction
		elif name == "princess":
			self.value = 8
			self.action = Game.princessAction
		elif name == "none":
			self.value = 0
		else:
			raise ValueError

class Game:

	def getOpponentFromPrompt(self, yourself, prompt):
		while True:
			name = input(prompt)
			found = False
			for player in self.tempPlayers:
				if name == player.name:
					found = True
					if player == yourself:
						print("You cannot play a card against yourself") 
					elif player in self.handmaid:
						if len(self.tempPlayers) == len(self.handmaid) + 1:
							return player	
						print("You cannot choose a player that played handmaid last turn")
					else:
						return player
			if not found:
				print("There is no active player named " + name)

	def getIntFromPrompt(self, prompt):
		while True:
			rawInput = input(prompt)
			try:
				result = int(rawInput)
				if result > 1 and result < 9:
					return result
				else:
					print("please enter an integer 2 - 8")	
			except ValueError:
				print("please enter an integer 2 - 8")
				continue

	def guardAction(self, player):
		opponent = self.getOpponentFromPrompt(player, "Which player would you like to guess?")
		guess = self.getIntFromPrompt("What number of card (2 - 8) do you think they have?")
		if opponent in self.handmaid:
			print(opponent.name + " is protected by the handmaid!")
		elif opponent.card.value == guess:
			self.playerLoses(opponent)

	def priestAction(self, player):
		opponent = self.getOpponentFromPrompt(player, "Which player's card would you like see?")
		if opponent in self.handmaid:
			print(opponent.name + " is protected by the handmaid!")
		else:
			print(opponent.card.name)

	def baronAction(self, player):
		opponent = self.getOpponentFromPrompt(player, "Which player would you like to challenge?")
		print("Your opponent had " + opponent.card.name)
		if opponent in self.handmaid:
			print(opponent.name + " is protected by the handmaid!")
		elif opponent.card.value < player.card.value:
			self.playerLoses(opponent)
		elif opponent.card.value > player.card.value:
			self.playerLoses(player)
		else:
			print("You tied!")

	def handmaidAction(self, player):
		self.handmaid.add(player)

	def princeAction(self, player):
		opponent = self.getOpponentFromPrompt(player, "Which player would you like to discard their card?")
		if opponent in self.handmaid:
			print(opponent.name + " is protected by the handmaid!")
		elif opponent.card.name == "princess":
			self.playerLoses(opponent)
		elif len(self.deck) > 0:
			opponent.card = self.deck.pop()
		else:
			opponent.card = Card("none")

	def kingAction(self, player):
		opponent = self.getOpponentFromPrompt(player, "Which player would you like to trade your card with?")
		if opponent in self.handmaid:
			print(opponent.name + " is protected by the handmaid!")
		else:
			opponent.card, player.card = player.card, opponent.card

	def countessAction(self, player):
		return

	def princessAction(self, player):
		self.playerLoses(player)

	def __init__(self):
		self.heartsNeededToWin = 7
		self.deck = None
		self.players = []
		self.score = {}

	def addPlayer(self, name):
		self.players.append(Player(name))
		self.score[name] = 0

	def playerLoses(self, player):
		print(player.name + " loses!")
		self.tempPlayers.remove(player)

	def playerWins(self, player):
		print(player.name + " wins!")
		self.score[player.name] += 1
		

	def createDeck(self):
		deck = []

		numCards = {}
		numCards["guard"] = 5
		numCards["priest"] = 2
		numCards["baron"] = 2
		numCards["handmaid"] = 2
		numCards["prince"] = 2
		numCards["king"] = 1
		numCards["countess"] = 1
		numCards["princess"] = 1

		for key in numCards:
			for i in range(numCards[key]):
				deck.append(Card(key))

		# shuffle
		# for i in range(len(deck)-1, 0, -1):
		#	indx = random.randint(0, i)
		#	deck[i], deck[indx] = deck[indx], deck[i]

		return sorted(deck, key=lambda x: random.random())

	def setUpGames(self):
		self.addPlayer("Nathan")
		self.addPlayer("Denise")

		while True:
			winner = self.play()
			self.playerWins(winner)

			for name in self.score:
				print(name + " won " + str(self.score[name]) + " times.")

			if self.score[winner.name] == self.heartsNeededToWin:
				print(winner.name + "won " + self.heartsNeededToWin + " times! " + winner.name + " captured the heart of the princess!")
				break

	def getPlayerWithHighestCard(self):
		maxScore = -1
		winner = None
		for player in self.tempPlayers:
			if player.card.value > maxScore:
				winner = player
				maxScore = winner.card.value
		return winner

	def play(self, lastWinner = None):
		self.deck = self.createDeck()
		self.tempPlayers = copy.deepcopy(self.players)
		self.invisibleFriend = self.deck.pop()
		self.handmaid = set()

		# winner goes first
		if lastWinner:
			playerIndex = self.tempPlayers.index(lastWinner)
		else:
			playerIndex = random.randint(0, len(self.tempPlayers)-1)

		for player in self.tempPlayers:
			player.card = self.deck.pop()

		while len(self.deck) > 0 and len(self.tempPlayers) > 1: 
			self.turn(self.tempPlayers[playerIndex])
			playerIndex = (playerIndex + 1) % len(self.tempPlayers)

		if len(self.tempPlayers) == 1:
			return self.tempPlayers[0]
		else:
			return self.getPlayerWithHighestCard()


	def turn(self, player):
		# draw card
		self.handmaid.discard(player)

		newCard = self.deck.pop()

		while True:
			# add check that if you have the countess and king or prince you must play king or prince
			if (player.card.name == "countess" or newCard.name == "countess") and ((newCard.name == "prince" or player.card.name == "prince") or (newCard.name == "king" or player.card.name == "king")):
				print("If you have the countess and a prince or king, you must play the countess!")
				if player.card.name == countess:
					choice = newCard.name
				else:
					choice = player.card.name
				break
				
			choice = input("Would you like to play " + player.card.name + " or " + newCard.name + "?")
			if choice == player.card.name or choice == newCard.name: 
				break
		if choice == player.card.name:
			player.card, newCard = newCard, player.card
			newCard.action(self, player)
		else:
			newCard.action(self, player)


game = Game()
game.setUpGames()


