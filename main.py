#!/usr/bin/env python3

"""

"""

import time
from random import randrange


# Player class
class player():
    def __init__(self):
        self.color = ''
        self.initial_spin = 0
        self.tie_break_spin = 0
        self.location = 0
        self.skip_next_turn = False
        self.cats = 0
        self.win = 0
        self.prev_move_nbr = 0

    def skip_next_turn(self):
        self.skip_next_turn = True
        

# Move class
class move():
    def __init__(self):
        self.round_nbr = 0
        self.move_nbr = 0
        self.player_nbr = 0
        self.spin_value = 0
        self.landing_space = 0
        self.player_1_cats = 0
        self.player_2_cats = 0
        self.player_3_cats = 0
        self.player_4_cats = 0
        self.game_tray_cats = 0
        self.animal_shelter_cats = 0
        self.player_1_location = 0
        self.player_2_location = 0
        self.player_3_location = 0
        self.player_4_location = 0
        self.last_move = 0
        self.player_prev_move_nbr = 0
        self.player_prev_location = 0


def spin():
    """ return a number between 1 and 6 """
    return randrange(1,7)

  
# global variables
player_count = 4
total_games = 10000       # number of games to simulate
path_th = 10             # threshold for entering the branched path
choose_highest = True    # when given the option to take from/give to a player, 
                         # choose the player with the most/fewest) cats
allow_tray_runout = True       # allow the tray to run out
allow_shelter_runout = True    # allow the animal shelter to run out
color_list = ['pink', 'blue', 'yellow', 'orange']   # clockwise order of colors  


# cycle through games
start_time = time.time()
  
for game_nbr in range(total_games):
    
    # initialize a list of players
    players = []
    tie_break_spins = {}
    for p in range(player_count):
        players.append(player)

        # assign a color, in clockwise order
        n = randrange(0, player_count)
        players[p].color = color_list[(n+p) % 4]

        players[p].initial_spin = spin()
        tie_break_spins[p] = players[p].initial_spin
                
        players[p].cats = 2
        players[p].location = 1
    
    # tie break the initial spin, if necessary        
    while sum(v > 0 for v in tie_break_spins.values()) > 1:  
        max_spin = -1
        tied = False
        for v in tie_break_spins.values():
            if v > max_spin: 
                max_spin = v
            elif max_spin == v:
                tied = True
    
        if tied == True:
            for k, v in tie_break_spins.items():
                if v == max_spin:
                    tie_break_spins[k] = spin()    # spin again
                else:
                    tie_break_spins[k] = 0    
        else:
            tied = False
            for k, v in tie_break_spins.items():
                if v != max_spin:
                    tie_break_spins[k] = 0
                else:
                    players[k].tie_break_spin = v
                    
    print(tie_break_spins)
    
    testit = []
    for i in range(player_count):
        testit.append(players[i].initial_spin)
    print(testit)
    
  


#initial_spin(1, 1) = "orange"
#initial_spin(1, 2) = "pink"
#initial_spin(1, 3) = "blue"
#initial_spin(1, 4) = "yellow"
#  
#'record spins
#initial_spin_count = 1
#For i = 1 To 4
#  initial_spin(2, i) = spin()    'used for retention
#  initial_spin(3, i) = initial_spin(2, i)    'used for tie break
#Next i
#
#'find the player with the highest spin and check for tie
#Do
#  'find highest
#  highest_spin = 0
#  For i = 1 To 4
#    If initial_spin(3, i) > highest_spin Then highest_spin = initial_spin(3, i)
#  Next i
#  
#  'check for tie
#  tied_count = 0
#  For i = 1 To 4
#    If initial_spin(3, i) = highest_spin Then
#      tied_count = tied_count + 1
#    End If
#  Next i
#
#  'spin again to tie break
#  If tied_count > 1 Then
#    initial_spin_count = initial_spin_count + 1
#    For i = 1 To 4
#      If initial_spin(3, i) = highest_spin Then
#        initial_spin(3, i) = spin()
#      Else
#        initial_spin(3, i) = 0
#      End If
#    Next i
#  End If
#Loop Until tied_count = 1
#
#'find the first player
#For c = 1 To 4
#  If initial_spin(3, c) = highest_spin Then Exit For    'c is the player with the highest spin
#Next c
#   
#
#'--- initialize player info ----------------------------------------
#
#For i = 1 To 4
#  player_status(1, i) = i    'player #
#  player_status(2, i) = initial_spin(1, ((i + (c - 2)) Mod 4) + 1)    'color
#  player_status(3, i) = initial_spin(2, ((i + (c - 2)) Mod 4) + 1)    'initial spin
#  If initial_spin_count > 1 And initial_spin(3, ((i + (c - 2)) Mod 4) + 1) > 0 Then
#    player_status(4, i) = initial_spin(3, ((i + (c - 2)) Mod 4) + 1)    'initial spin tie break
#  Else
#    player_status(4, i) = 0
#  End If
#  player_status(5, i) = 1   'start space
#  player_status(6, i) = False   'skip next turn
#  player_status(7, i) = 2   'initial allocation of pieces
#  player_status(8, i) = 0   'set win flag to zero
#  player_status(9, i) = 0   'initialize prev move to zero
#Next i
#
#
#'--- play ----------------------------------------
#
#turn_nbr = 0
#move_nbr = 0
#
#Do
#  turn_nbr = turn_nbr + 1
#  
#  For player_nbr = 1 To 4
#    
#    'does this player skip a turn?
#    If player_status(6, player_nbr) = True Then
#      player_status(6, player_nbr) = False    'reset the flag
#      GoTo next_player
#    End If
#    
#player_spin:
#    'spin
#    s = spin()
#    
#    move_nbr = move_nbr + 1
#    total_moves = total_moves + 1
#    
#    ReDim Preserve moves(1 To 18, 1 To total_moves - moves_break)   'add a record
#    moves(1, total_moves - moves_break) = game_nbr
#    moves(2, total_moves - moves_break) = move_nbr
#    moves(3, total_moves - moves_break) = turn_nbr
#    moves(4, total_moves - moves_break) = player_status(2, player_nbr)
#    moves(5, total_moves - moves_break) = s
#    moves(17, total_moves - moves_break) = player_status(9, player_nbr)    'previous move nbr
#    moves(18, total_moves - moves_break) = player_status(5, player_nbr)    'previous location
#    
#    
#    'find the landing space (path is branched after space 28 based on # of cats)
#    If player_status(5, player_nbr) + s <= 28 Then
#    'landing space is before or on the split
#      moves(6, total_moves - moves_break) = player_status(5, player_nbr) + s    'current space + spin
#    ElseIf (player_status(5, player_nbr) <= 28 And player_status(7, player_nbr) < path_th) _
#           Or (player_status(5, player_nbr) > 28 And player_status(5, player_nbr) <= 33) Then
#    'before the split and not enough cats -- OR -- already on upper path --> take upper path
#      moves(6, total_moves - moves_break) = ((player_status(5, player_nbr) + s - 1) Mod 33) + 1
#    Else
#    'before the split and cats >= threshold -- OR -- player already on the lower path --> take the lower path
#        moves(6, total_moves - moves_break) = player_status(5, player_nbr) + IIf(player_status(5, player_nbr) <= 28, 5, 0) + s
#        If moves(6, total_moves - moves_break) > 40 Then moves(6, total_moves - moves_break) = 40    'stop at home (last) space
#    End If
#    player_status(5, player_nbr) = moves(6, total_moves - moves_break)    'update last space
#    player_status(9, player_nbr) = total_moves    'update last move
#    
#
#    'initialize the cat counts
#    If move_nbr = 1 Then    'players start with two cats each
#      moves(7, total_moves - moves_break) = 2              'player 1
#      moves(8, total_moves - moves_break) = 2              'player 2
#      moves(9, total_moves - moves_break) = 2              'player 3
#      moves(10, total_moves - moves_break) = 2             'player 4
#      moves(11, total_moves - moves_break) = 50 - 2 * 4    'game tray
#      moves(12, total_moves - moves_break) = 0             'animal shelter
#    Else
#      moves(7, total_moves - moves_break) = moves(7, total_moves - moves_break - 1)       'player 1
#      moves(8, total_moves - moves_break) = moves(8, total_moves - moves_break - 1)       'player 2
#      moves(9, total_moves - moves_break) = moves(9, total_moves - moves_break - 1)       'player 3
#      moves(10, total_moves - moves_break) = moves(10, total_moves - moves_break - 1)     'player 4
#      moves(11, total_moves - moves_break) = moves(11, total_moves - moves_break - 1)     'game tray
#      moves(12, total_moves - moves_break) = moves(12, total_moves - moves_break - 1)     'animal shelter
#    End If
#    
#    
#    'initialize locations
#    moves(13, total_moves - moves_break) = player_status(5, 1)    'player 1
#    moves(14, total_moves - moves_break) = player_status(5, 2)    'player 2
#    moves(15, total_moves - moves_break) = player_status(5, 3)    'player 3
#    moves(16, total_moves - moves_break) = player_status(5, 4)    'player 4
#     
#
#    'check for player(s) on the same space (take one of their cats)
#    For p = 1 To 4
#      If p <> player_nbr And player_status(5, p) = moves(6, total_moves - moves_break) And moves(6 + p, total_moves - moves_break) > 0 Then
#        'another player is on the same space and the player has at least one cat
#        
#        'take from other player
#        moves(6 + p, total_moves - moves_break) = moves(6 + p, total_moves - moves_break) - 1
#        player_status(7, p) = moves(6 + p, total_moves - moves_break)
#        
#        'add to current player
#        moves(6 + player_nbr, total_moves - moves_break) = moves(6 + player_nbr, total_moves - moves_break) + 1
#        player_status(7, player_nbr) = moves(6 + player_nbr, total_moves - moves_break)
#      End If
#    Next p
#
#
#    'take action based on the space
#select_move_action:
#    If moves(6, total_moves - moves_break) = 1 _
#       Or moves(6, total_moves - moves_break) = 28 Then    'start or branch point
#          '(do nothing)
#
#
#    '--- spaces with: gain 1 from game tray ------------------------------
#    ElseIf moves(6, total_moves - moves_break) = 2 _
#           Or moves(6, total_moves - moves_break) = 3 _
#           Or moves(6, total_moves - moves_break) = 5 _
#           Or moves(6, total_moves - moves_break) = 7 _
#           Or moves(6, total_moves - moves_break) = 14 _
#           Or moves(6, total_moves - moves_break) = 27 _
#           Or moves(6, total_moves - moves_break) = 36 Then
#      '2 = find a cat curled up in a wheelbarrow
#      '3 = bribe a skittish cat with tuna treats
#      '5 = pick up stray
#      '7 = save a cat stuck in a tree
#      '14 = find a stray by the railroad tracks
#      '27 = kitten falls from sky into your pocket
#      '36 = find a feral cat in a dumpster
#
#      'increment the current player
#      If allow_tray_runout = False Or moves(11, total_moves - moves_break) >= 1 Then
#        moves(6 + player_nbr, total_moves - moves_break) = moves(6 + player_nbr, total_moves - moves_break) + 1
#          player_status(7, player_nbr) = moves(6 + player_nbr, total_moves - moves_break)   'increment the player status array
#        moves(11, total_moves - moves_break) = moves(11, total_moves - moves_break) - 1  'decrement the game tray
#      End If
#
#
#    '--- gain from animal shelter ------------------------------
#    ElseIf moves(6, total_moves - moves_break) = 32 _
#           Or moves(6, total_moves - moves_break) = 33 Then
#      '32 - rescue a grumpy old cat from the pound
#      '33 - rescue all cats from the shelter
#    
#      'number of cats
#      If moves(6, total_moves - moves_break) = 33 Then 'all cats from shelter
#        c = moves(12, total_moves - moves_break)
#      Else
#        c = 1
#      End If
#      
#      'if the flag has been set to allow shelter runout, then limit to the number in the shelter
#      'otherwise, allow the shelter to go negative
#      If allow_shelter_runout = True Then
#        If c > moves(12, total_moves - moves_break) Then c = moves(12, total_moves - moves_break)
#      End If
#                
#      'increment the current player
#      moves(6 + player_nbr, total_moves - moves_break) = moves(6 + player_nbr, total_moves - moves_break) + c
#        player_status(7, player_nbr) = moves(6 + player_nbr, total_moves - moves_break)    'increment the player status array
#      moves(12, total_moves - moves_break) = moves(12, total_moves - moves_break) - c    'decrement the animal shelter
#
#
#    '--- spin and gain from game tray ------------------------------
#    ElseIf moves(6, total_moves - moves_break) = 20 _
#           Or moves(6, total_moves - moves_break) = 23 _
#           Or moves(6, total_moves - moves_break) = 39 Then
#      '20 = supermarket
#      '23 = pet store
#      '39 = home
#
#      'number to gain
#      c = spin()
#
#      'if flag was set to allow tray runout, limit to the number of cats in the tray
#      'otherwise, allow the tray go negative
#      If allow_tray_runout = True Then
#        If c > moves(11, total_moves - moves_break) Then c = moves(11, total_moves - moves_break)
#      End If
#
#      'increment the current player
#      moves(6 + player_nbr, total_moves - moves_break) = moves(6 + player_nbr, total_moves - moves_break) + c
#        player_status(7, player_nbr) = moves(6 + player_nbr, total_moves - moves_break)   'increment the player status array
#      moves(11, total_moves - moves_break) = moves(11, total_moves - moves_break) - c  'decrement the game tray
#
#
#    '--- lose to animal shelter ------------------------------
#    ElseIf moves(6, total_moves - moves_break) = 4 _
#           Or moves(6, total_moves - moves_break) = 9 _
#           Or moves(6, total_moves - moves_break) = 10 _
#           Or moves(6, total_moves - moves_break) = 15 _
#           Or moves(6, total_moves - moves_break) = 19 _
#           Or moves(6, total_moves - moves_break) = 35 Then
#      '4 = beware of dog
#      '9 = park - cat chases butterfly
#      '10 = cat more interested in cardboard box
#      '15 = kitten distracted by bit of fluff
#      '19 = milk truck spill
#      '35 = cat fight
#
#      'how many cats to remove
#      Select Case moves(6, total_moves - moves_break)
#        Case 19
#          c = 3
#        Case 35
#          c = 2
#        Case Else
#          c = 1
#      End Select
#      If c > moves(6 + player_nbr, total_moves - moves_break) Then c = moves(6 + player_nbr, total_moves - moves_break)
#
#
#      'remove cats from current player (if they have one)
#      moves(6 + player_nbr, total_moves - moves_break) = moves(6 + player_nbr, total_moves - moves_break) - c
#        player_status(7, player_nbr) = moves(6 + player_nbr, total_moves - moves_break)   'update the player status array
#
#      moves(12, total_moves - moves_break) = moves(12, total_moves - moves_break) + c  'increment the animal shelter
#
#
#    '--- animal control confiscates half your cats, then go to start ------------------------------
#    ElseIf moves(6, total_moves - moves_break) = 38 Then
#
#      'how many cats to remove
#      c = Int(moves(6 + player_nbr, total_moves - moves_break) / 2)    'if an odd number, round down in the player's favor
#
#      'remove cats from current player (if they have one)
#      moves(6 + player_nbr, total_moves - moves_break) = moves(6 + player_nbr, total_moves - moves_break) - c
#        player_status(7, player_nbr) = moves(6 + player_nbr, total_moves - moves_break)   'increment the player status array
#
#      moves(12, total_moves - moves_break) = moves(12, total_moves - moves_break) + c  'increment the animal shelter
#
#
#     'add new move
#      move_nbr = move_nbr + 1
#      total_moves = total_moves + 1
#      ReDim Preserve moves(1 To 18, 1 To total_moves - moves_break)   'add a record
#      moves(1, total_moves - moves_break) = game_nbr
#      moves(2, total_moves - moves_break) = move_nbr
#      moves(3, total_moves - moves_break) = turn_nbr
#      moves(4, total_moves - moves_break) = player_status(2, player_nbr)
#      moves(6, total_moves - moves_break) = 1    'start
#      moves(7, total_moves - moves_break) = moves(7, total_moves - moves_break - 1)
#      moves(8, total_moves - moves_break) = moves(8, total_moves - moves_break - 1)
#      moves(9, total_moves - moves_break) = moves(9, total_moves - moves_break - 1)
#      moves(10, total_moves - moves_break) = moves(10, total_moves - moves_break - 1)
#      moves(11, total_moves - moves_break) = moves(11, total_moves - moves_break - 1)
#      moves(12, total_moves - moves_break) = moves(12, total_moves - moves_break - 1)
#      moves(13, total_moves - moves_break) = moves(13, total_moves - moves_break - 1)
#      moves(14, total_moves - moves_break) = moves(14, total_moves - moves_break - 1)
#      moves(15, total_moves - moves_break) = moves(15, total_moves - moves_break - 1)
#      moves(16, total_moves - moves_break) = moves(16, total_moves - moves_break - 1)
#      
#      moves(17, total_moves - moves_break) = player_status(9, player_nbr)   'update last move nbr
#      player_status(9, player_nbr) = total_moves
#      
#      moves(18, total_moves - moves_break) = player_status(5, player_nbr)
#      player_status(5, player_nbr) = moves(6, total_moves - moves_break)    'update last space
#
#      GoTo select_move_action
#
#
#    '--- lose to game tray (veterinarian) ------------------------------
#    ElseIf moves(6, total_moves - moves_break) = 26 Then
#
#      'how many cats to remove
#      c = Int(Rnd() * 6) + 1
#      If c > moves(6 + player_nbr, total_moves - moves_break) Then c = moves(6 + player_nbr, total_moves - moves_break)
#
#      'remove cats from current player (if they have one)
#      moves(6 + player_nbr, total_moves - moves_break) = moves(6 + player_nbr, total_moves - moves_break) - c
#        player_status(7, player_nbr) = moves(6 + player_nbr, total_moves - moves_break)   'increment the player status array
#
#      moves(11, total_moves - moves_break) = moves(11, total_moves - moves_break) + c  'increment the game tray
#
#
#    '--- spin again ------------------------------
#    ElseIf moves(6, total_moves - moves_break) = 6 _
#           Or moves(6, total_moves - moves_break) = 13 _
#           Or moves(6, total_moves - moves_break) = 24 _
#           Or moves(6, total_moves - moves_break) = 31 Then
#      GoTo player_spin
#
#
#    '--- lose next turn ------------------------------
#    ElseIf moves(6, total_moves - moves_break) = 8 _
#           Or moves(6, total_moves - moves_break) = 22 _
#           Or moves(6, total_moves - moves_break) = 37 Then
#      '8 = pick catnip
#      '22 = stop to pet a cat
#      '37 = hairball
#
#      player_status(6, player_nbr) = True    'skip next turn
#      GoTo next_player
#
#
#    '--- take 1 from any player ------------------------------
#    ElseIf moves(6, total_moves - moves_break) = 11 _
#           Or moves(6, total_moves - moves_break) = 17 Then
#      '11 - catsit
#      '17 - fall in love with neighborhood cat
#
#      'choose player
#      If choose_highest = True Then    'fill the array with player(s) that have the most cats
#        
#        'find the highest number of cats
#        j = 0
#        For i = 1 To 4
#          If i <> player_nbr And moves(6 + i, total_moves - moves_break) > j Then j = moves(6 + i, total_moves - moves_break)
#        Next i
#      
#        If j = 0 Then GoTo next_player    'no cats to take
#        
#        'find the player(s) with the highest number of cats (possibility of tie)
#        c = 0
#        For i = 1 To 4
#          If i <> player_nbr And moves(6 + i, total_moves - moves_break) = j Then    'not current player and has max cats
#            c = c + 1
#            ReDim Preserve available_players(1 To c)
#            available_players(c) = i    'add this player to the array
#          End If
#        Next i
#         
#      Else    'pick a player at random - fill the array with any player with cats > 0
#        c = 0
#        For i = 1 To 4
#          If i <> player_nbr And moves(6 + i, total_moves - moves_break) >= 1 Then    'not current player and has cats
#            c = c + 1
#            ReDim Preserve available_players(1 To c)
#            available_players(c) = i    'add this player to the array
#          End If
#        Next i
#  
#        If c = 0 Then GoTo next_player    'no cats to take
#          
#      End If
#      
#      'pick from the array of available players
#      r = Rnd()
#      p = available_players(Int(r * c) + 1)
#                
#      'decrement the chosen player
#      moves(6 + p, total_moves - moves_break) = moves(6 + p, total_moves - moves_break) - 1
#      player_status(7, p) = moves(6 + p, total_moves - moves_break)
#
#      'increment the current player
#      moves(6 + player_nbr, total_moves - moves_break) = moves(6 + player_nbr, total_moves - moves_break) + 1
#      player_status(7, player_nbr) = moves(6 + player_nbr, total_moves - moves_break)    'increment the player status array
#
#
#    '--- take 1 from each player ------------------------------
#    ElseIf moves(6, total_moves - moves_break) = 30 Then
#      '30 - catnip in your pocket lures cats
#
#      For p = 1 To 4
#        If p <> player_nbr And moves(6 + p, total_moves - moves_break) >= 1 Then    'not the current player, and they have at least 1 cat
#          'decrement the other player
#          moves(6 + p, total_moves - moves_break) = moves(6 + p, total_moves - moves_break) - 1
#          player_status(7, p) = moves(6 + p, total_moves - moves_break)
#
#          'increment the current player
#          moves(6 + player_nbr, total_moves - moves_break) = moves(6 + player_nbr, total_moves - moves_break) + 1
#          player_status(7, player_nbr) = moves(6 + player_nbr, total_moves - moves_break)
#       End If
#     Next p
#
#
#    '--- go to another space ------------------------------
#    ElseIf moves(6, total_moves - moves_break) = 12 _
#           Or moves(6, total_moves - moves_break) = 16 _
#           Or moves(6, total_moves - moves_break) = 18 _
#           Or moves(6, total_moves - moves_break) = 21 _
#           Or moves(6, total_moves - moves_break) = 29 _
#           Or moves(6, total_moves - moves_break) = 34 Then
#      '12 = kitty litter emergency (supermarket)
#      '16 = forgot cat food coupons (return to start)
#      '18 = pursue a mangy cat (park)
#      '21 = sick cat (vet)
#      '29 = hear the mews of caged cats (animal shelter)
#      '34 = forgot flea collars (vet)
#
#      'add new move
#      move_nbr = move_nbr + 1
#      total_moves = total_moves + 1
#      ReDim Preserve moves(1 To 18, 1 To total_moves - moves_break)   'add a record
#      moves(1, total_moves - moves_break) = game_nbr
#      moves(2, total_moves - moves_break) = move_nbr
#      moves(3, total_moves - moves_break) = turn_nbr
#      moves(4, total_moves - moves_break) = player_status(2, player_nbr)
#      'leave row 5 (spin) blank
#
#      Select Case moves(6, total_moves - moves_break - 1)
#        Case 12
#          moves(6, total_moves - moves_break) = 20   'supermarket
#        Case 16
#          moves(6, total_moves - moves_break) = 1    'start
#        Case 18
#          moves(6, total_moves - moves_break) = 9    'park
#        Case 21
#          moves(6, total_moves - moves_break) = 26   'vet
#        Case 29
#          moves(6, total_moves - moves_break) = 33   'animal shelter
#        Case 34
#          moves(6, total_moves - moves_break) = 26   'vet
#      End Select
#
#      moves(7, total_moves - moves_break) = moves(7, total_moves - moves_break - 1)
#      moves(8, total_moves - moves_break) = moves(8, total_moves - moves_break - 1)
#      moves(9, total_moves - moves_break) = moves(9, total_moves - moves_break - 1)
#      moves(10, total_moves - moves_break) = moves(10, total_moves - moves_break - 1)
#      moves(11, total_moves - moves_break) = moves(11, total_moves - moves_break - 1)
#      moves(12, total_moves - moves_break) = moves(12, total_moves - moves_break - 1)
#      moves(13, total_moves - moves_break) = moves(13, total_moves - moves_break - 1)
#      moves(14, total_moves - moves_break) = moves(14, total_moves - moves_break - 1)
#      moves(15, total_moves - moves_break) = moves(15, total_moves - moves_break - 1)
#      moves(16, total_moves - moves_break) = moves(16, total_moves - moves_break - 1)
#      
#      moves(17, total_moves - moves_break) = player_status(9, player_nbr)
#      player_status(9, player_nbr) = total_moves     'update previous move
#
#      moves(18, total_moves - moves_break) = player_status(5, player_nbr)
#      player_status(5, player_nbr) = moves(6, total_moves - moves_break)    'update prev space
#
#
#      GoTo select_move_action
#
#
#    '--- wildcat ------------------------------
#    ElseIf moves(6, total_moves - moves_break) = 25 Then
#
#      'select wildcat card (1 of 4)
#      c = Int(Rnd() * 4) + 1
#      
#      'perform action on card
#      Select Case c
#        
#        Case 1
#        'Your great aunt passes away, leaving you eight cats and a box of yarn.
#      
#          'number of cats to move
#          c = 8
#          If allow_tray_runout = True And moves(11, total_moves - moves_break) <= c Then c = moves(11, total_moves - moves_break)
#                        
#          'add cats to current player
#          moves(6 + player_nbr, total_moves - moves_break) = moves(6 + player_nbr, total_moves - moves_break) + c
#          player_status(7, player_nbr) = moves(6 + player_nbr, total_moves - moves_break)
#
#          'decrement the game tray
#          moves(11, total_moves - moves_break) = moves(11, total_moves - moves_break) - c
#
#      Case 2
#      'You are overcome with the intese desire to own every cat you see.
#      'Each player spins, then gives you that many of their cats.
#      
#        For p = 1 To 4
#          If p <> player_nbr Then    'not the current player
#            c = spin()
#            If moves(6 + p, total_moves - moves_break) < c Then c = moves(6 + p, total_moves - moves_break) 'player doesn't have enough cats
#            
#            'add c cats to current player
#            moves(6 + player_nbr, total_moves - moves_break) = moves(6 + player_nbr, total_moves - moves_break) + c
#            player_status(7, player_nbr) = moves(6 + player_nbr, total_moves - moves_break)
#
#            'remove c cats from player p
#            moves(6 + p, total_moves - moves_break) = moves(6 + p, total_moves - moves_break) - c
#            player_status(7, p) = moves(6 + p, total_moves - moves_break)
#                         
#          End If
#        Next p
#
#      Case Else    'c = 3 or 4 (there are two copies of this card)
#      'You feel sorry for a friend who doesn't have enough cats.
#      'Choose a player, spin, then give them that many of your cats.
#
#        If moves(6 + player_nbr, total_moves - moves_break) = 0 Then GoTo next_player    'current player doesn't have any cats
#        
#        'choose a player
#        If choose_highest Then    'choose the player with the lowest number of cats
#        
#          'find the lowest number of cats
#          j = 9999
#          For i = 1 To 4
#            If i <> player_nbr And moves(6 + i, total_moves - moves_break) < j Then j = moves(6 + i, total_moves - moves_break)
#          Next i
#      
#          'find the player(s) with the lowest number of cats (possibility of tie)
#          c = 0
#          For i = 1 To 4
#            If i <> player_nbr And moves(6 + i, total_moves - moves_break) = j Then    'not current player and has max cats
#              c = c + 1
#              ReDim Preserve available_players(1 To c)
#              available_players(c) = i    'add this player to the array
#            End If
#          Next i
#           
#        Else    'fill the array with all other players
#          ReDim available_players(1 To 3)
#          c = 0
#          For i = 1 To 4
#            If i <> player_nbr Then
#              c = c + 1
#              available_players(c) = i    'add this player to the array
#            End If
#          Next i
#          
#        End If
#      
#        'pick from the array of available players
#        r = Rnd()
#        p = available_players(Int(r * c) + 1)
#        
#        'number of cats
#        c = spin()
#        If c > moves(6 + player_nbr, total_moves - moves_break) Then c = moves(6 + player_nbr, total_moves - moves_break) 'current player doesn't have enough cats
#        
#        'add to the chosen player
#        moves(6 + p, total_moves - moves_break) = moves(6 + p, total_moves - moves_break) + c
#        player_status(7, p) = moves(6 + p, total_moves - moves_break)
# 
#        'remove from the current player
#        moves(6 + player_nbr, total_moves - moves_break) = moves(6 + player_nbr, total_moves - moves_break) - c
#        player_status(7, player_nbr) = moves(6 + player_nbr, total_moves - moves_break)
#
#     End Select
#
#
#    '--- end game ------------------------------
#    ElseIf moves(6, total_moves - moves_break) = 40 Then
#      'find highest count
#      c = 0
#      j = 0    'max
#      For i = 1 To 4
#        If moves(6 + player_nbr, total_moves - moves_break) > j Then
#          j = moves(6 + player_nbr, total_moves - moves_break)
#        End If
#      Next i
#
#      'mark the winner(s)
#      For i = 1 To 4
#        If moves(6 + i, total_moves - moves_break) = j Then
#          player_status(8, i) = 1
#        Else
#          player_status(8, i) = 0
#        End If
#      Next i
#      GoTo end_game
#    
#    End If
#      
#next_player:
#  Next player_nbr
#Loop    'round
#  
#end_game:
#'copy ending player status
#ReDim Preserve end_player_status(1 To 10, 1 To game_nbr * 4)
#For j = 1 To 4
#  For i = 1 To 10
#    If i = 10 Then
#      end_player_status(i, (game_nbr - 1) * 4 + j) = game_nbr
#    Else
#      end_player_status(i, (game_nbr - 1) * 4 + j) = player_status(i, j)
#    End If
#  Next i
#Next j
#  
#  
#If game_nbr Mod games_break = 0 Then    'if the game number is an increment of the break
#  file_count = Int((game_nbr - 1) / games_break) + 1
#  
#  On Error Resume Next
#  Sheets("moves" & file_count).Select
#  If Err.Number <> 0 Then
#    'create the sheet
#    ActiveWorkbook.Sheets.Add
#    Err.Clear
#  End If
#
#  Cells.Select
#  Selection.Clear
#
#  'add a header for the moves sheet(s)
#  Range("a1").Select
#  ActiveCell.Offset(0, 0).Value = "game_nbr"
#  ActiveCell.Offset(0, 1).Value = "move_nbr"
#  ActiveCell.Offset(0, 2).Value = "round_nbr"
#  ActiveCell.Offset(0, 3).Value = "player_color"
#  ActiveCell.Offset(0, 4).Value = "spin"
#  ActiveCell.Offset(0, 5).Value = "landing_space"
#  ActiveCell.Offset(0, 6).Value = "cats_player1"
#  ActiveCell.Offset(0, 7).Value = "cats_player2"
#  ActiveCell.Offset(0, 8).Value = "cats_player3"
#  ActiveCell.Offset(0, 9).Value = "cats_player4"
#  ActiveCell.Offset(0, 10).Value = "cats_tray"
#  ActiveCell.Offset(0, 11).Value = "cats_shelter"
#  ActiveCell.Offset(0, 12).Value = "location_player1"
#  ActiveCell.Offset(0, 13).Value = "location_player2"
#  ActiveCell.Offset(0, 14).Value = "location_player3"
#  ActiveCell.Offset(0, 15).Value = "location_player4"
#  ActiveCell.Offset(0, 16).Value = "previous_move_nbr"
#  ActiveCell.Offset(0, 17).Value = "previous_location"
#  Range("a1").Select
#
#  For i = 1 To total_moves - moves_break
#    For j = 1 To 18
#      ActiveCell.Offset(i, j - 1).Value = moves(j, i)
#    Next j
#  Next i
#  
#  Sheets("moves" & file_count).Select
#  Sheets("moves" & file_count).Copy
#  ChDir curr_path
#  Application.DisplayAlerts = False
#  ActiveWorkbook.SaveAs Filename:= _
#      curr_path & "\ccl_simulation_output_moves" & file_count & ".csv" _
#      , FileFormat:=xlCSV, CreateBackup:=False
#  ActiveWorkbook.Save
#  ActiveWindow.Close
#  Application.DisplayAlerts = True
#  
#  Workbooks(curr_file).Activate
#  moves_break = total_moves
#End If
#   
#  Next game_nbr    'game
#
#
#  'simulated games complete.
#  
#  'output the ending status for each player
#  Sheets("end_player_status").Select
#  Cells.Select
#  Selection.Clear
#  Range("a1").Select
#  ActiveCell.Offset(0, 0).Value = "player_nbr"
#  ActiveCell.Offset(0, 1).Value = "player_color"
#  ActiveCell.Offset(0, 2).Value = "initial_spin"
#  ActiveCell.Offset(0, 3).Value = "initial_spin_tie_break"
#  ActiveCell.Offset(0, 4).Value = "last_space"
#  ActiveCell.Offset(0, 5).Value = "skip_next_turn"
#  ActiveCell.Offset(0, 6).Value = "cats"
#  ActiveCell.Offset(0, 7).Value = "win"
#  ActiveCell.Offset(0, 8).Value = "previous_move_nbr"
#  ActiveCell.Offset(0, 9).Value = "game_nbr"
#  
#  For i = 1 To (game_nbr - 1) * 4
#For j = 1 To 10
#  ActiveCell.Offset(i, j - 1).Value = end_player_status(j, i)
#Next j
#  Next i
#
#  Sheets("end_player_status").Select
#  Sheets("end_player_status").Copy
#  ChDir curr_path
#  Application.DisplayAlerts = False
#  ActiveWorkbook.SaveAs Filename:= _
#  curr_path & "\ccl_simulation_output_end_status.csv" _
#  , FileFormat:=xlCSV, CreateBackup:=False
#  ActiveWorkbook.Save
#  ActiveWindow.Close
#  Application.DisplayAlerts = True
#  
#  Workbooks(curr_file).Activate
#  
#  
#  Application.ScreenUpdating = True
#  
#  MsgBox "Completed in " & Round(DateDiff("s", start_time, Now()) / 60, 1) & " minutes."
#
#End Sub
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#    
#    
#    
#
#class Enemy():
#def __init__(self,ancestry,gear):
#    self.enemy=ancestry
#    self.weapon=gear
#    self.hp=random.randrange(10,20)
#    self.ac=random.randrange(12,20)
#    self.alive=True
#
#def fight(self,tgt):
#    print("You take a swing at the " + self.enemy + ".")
#    hit=random.randrange(0,20)
#
#    if self.alive and hit > self.ac:
#        print("You hit the " + self.enemy + " for " + str(hit) + " damage!")
#        self.hp = self.hp - hit
#        print("The " + self.enemy + " has " + str(self.hp) + " HP remaining")
#    else:
#        print("You missed.")
#
#    if self.hp < 1:
#        self.alive=False
#        
#        
## game start
#foe=Enemy("troll","great axe")
#print("You meet a " + foe.enemy + " wielding a " + foe.weapon)
#
## main loop
#while True:
#   
#print("Type the a key and then RETURN to attack.")
#    
#action=input()
#
#if action.lower() == "a":
#    foe.fight(foe)
#            
#if foe.alive == False:
#    print("You have won...this time.")
#    exit()