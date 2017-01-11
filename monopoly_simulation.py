# Monopoly simulation
# Calculating probability of landing 

import random
from random import shuffle

# number of players
players = 4

# number of turns
turns = 30

# number of simulation
simulation = 50000

# player initialize
player_position = [0]*players
jailed = [0]*players

# variables
rolls = [1,2,3,4,5,6]
count = {}
for i in range(0,40):
	count[i] = 0
total = 0

# Community chest cards
community = [""]*14
community.append("go")
community.append("jail")
shuffle(community)

# Chance Cards
chance = ["go", "illinois", "st charls", "utility", "railroad", "railroad","back3", "jail", "reading", "boardwalk","","","","","",""]
shuffle(chance)

board = [[],[],["community"],[],[],[],[],["chance"],[],[],
		[], [],[], [],[],[], [],["community"], [],[],
		[],[],["chance"],[],[],[],[],[],[], [],
		["go_to_jail"], [],[],["community"],[],[],["chance"],[],[],[]]

go = 0
jail = 10
railroad = 5, 15, 25, 35
utility = 12, 28

def take_community(player, position):
	card = community.pop(0)
	community.append(card)
	global total
	if card == "go":
		return 0
	elif card == "jail":
		return 10
	# no positional change
	return player_position[player]
		

def take_chance(player, position):
	card = chance.pop(0)
	chance.append(card)
	if card == "go":
		return 0
	elif card == "jail":
		return 10
	elif card == "illinois":
		return 24
	elif card == "st charls":
		return 11
	elif card == "reading":
		return 5
	elif card == "boardwalk":
		return 39
	elif card == "railroad":
		position = player_position[player]
		if position == 7:
			return 15
		elif position == 22:
			return 25
		elif position == 36:
			return 5
	elif card == "utility":
		position = player_position[player]
		if position == 7:
			return 12
		elif position == 22:
			return 28
		elif position == 36:
			return 12
	elif card == "back3":
		return player_position[player]-3
	else:
        # no change
		return player_position[player]
	
	
def turn(player, position ,double):
	global total 
	
	# roll 2 dice
	roll1 = rolls[random.randint(0,5)]
	roll2 = rolls[random.randint(0,5)]
		
	# New position 
	position = (position + roll1 + roll2)%40
	player_position[player] = position
        
    # check if it landed on special square
	total += 1
	square = board[position]
	if square != []:
		
		# Go to jail
		if square == ["go_to_jail"]:
			count[10] += 1
			jailed[player] = 3
			return 10
			
		# Community Chest
		elif square == ["community"]:
			position = take_community(player, position)
			if( position == 10):
				count[10] += 1
				jailed[player] = 3
				return 10
		
		# Chance 
		elif square == ["chance"]:
			position = take_chance(player, position)
			if( position == 10):
				jailed[player] = 3
				count[10] += 1
				return 10
	
	count[position] += 1
		
	# doubles, roll again
	if roll1 == roll2:
		double = double + 1
		# 3 doubles send player to jail
		if double == 3:
			#print("3Double Jail")
			count[10] += 1
			jailed[player] = 3
			return 10
		# roll again 
		player_position[player] = position
		position = turn(player, position ,double)
	
	return position

def main():
	global total
	global player_position
	global jailed
	
	# Do simulation number of times
	for _ in range(simulation):
		
		player_position = [0]*players
		jailed = [0]*players
		shuffle(community)
		shuffle(chance)

		# Do turn number of times
		for __ in range(turns):

			# cycle through turns
			for i in range(len(player_position)):
				
				# check if in jail
				if jailed[i] == 0:
					
					# number of doubles rolled
					double = 0
					
					# Do turn
					player_position[i] = turn(i, player_position[i],double)
				
				else:
				
					#print("Player", i, "In Jail", end = " ")
					# spent turn in jail
					jailed[i] = jailed[i] - 1
					
					# attempt at bail
					roll1 = rolls[random.randint(0,5)]
					roll2 = rolls[random.randint(0,5)]
					# rolled a double or time to leave
					if roll1 == roll2 or jailed[i] == 0:
						jailed[i] = 0
						#print("leaving +", roll1+roll2, end = " ")
						player_position[i] = (player_position[i] + roll1 + roll2)%40
						count[player_position[i]] += 1
						total += 1
						
						# landed on Chance
						if roll1+roll2 == 12:
							#print("chance", end = " ")
							player_position[i] = take_chance(i, player_position[i])	
					
				#print(player_position)
				

main()

percent = {}

def result():
	print("Total:", total)
	for i in count:
		percent[i] = count[i]*100/total
	for i in percent:
		print(i, ":", percent[i])
		
result()
