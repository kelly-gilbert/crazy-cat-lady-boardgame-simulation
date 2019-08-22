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
        self.game_nbr = 0
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


def attr_list(list_name, attr_name):
    """
    For a list of objects, return a list of the specified attribute
    """
    attr_list = []
    for i in range(len(list_name)):
        attr_list.append(getattr(list_name[i], attr_name))
        
    return attr_list


  
#------------------------------------------------------------------------------    
# initialize variables
#------------------------------------------------------------------------------
player_count = 4
total_games = 10000       # number of games to simulate
path_th = 10             # threshold for entering the branched path
choose_highest = True    # when given the option to take from/give to a player, 
                         # choose the player with the most/fewest) cats
allow_tray_runout = True       # allow the tray to run out
allow_shelter_runout = True    # allow the animal shelter to run out
color_list = ['pink', 'blue', 'yellow', 'orange']   # clockwise order of colors  


#------------------------------------------------------------------------------    
#  cycle through simulated games
#------------------------------------------------------------------------------
    
start_time = time.time()
  

#for game_nbr in range(total_games):
    
#------------------------------------------------------------------------------    
#  spin to see which player goes first
#------------------------------------------------------------------------------
initial_spins = []
tie_break_spins = {}
for p in range(player_count):
    initial_spins.append(spin())
    tie_break_spins[p] = initial_spins[p]    # duplicate the spins

# tie break the initial spin, if necessary    
tie_break_loops = 0    
while sum(v > 0 for v in tie_break_spins.values()) > 1:
    tied = False
    max_spin = max(v for v in tie_break_spins.values())
    
    if sum(v == max_spin for v in tie_break_spins.values()) > 1:
        tied = True

    if tied == True:
        for k, v in tie_break_spins.items():
            if v == max_spin:
                tie_break_spins[k] = spin()    # spin again
            else:
                tie_break_spins[k] = 0    
                
    else:    # not tied
        for k, v in tie_break_spins.items():
            if tie_break_loops == 0:
                tie_break_spins[k] = 0    # set all to zero
            else:
               initial_spins[k] = v
        break

    tie_break_loops += 1

    
#------------------------------------------------------------------------------    
# initialize the players, starting with the highest spin in element 0
#------------------------------------------------------------------------------
    
# spin order offset
if tie_break_loops == 0:    # initial spin not tied
    n = initial_spins.index(max_spin)
else:
    n = tie_break_spins.index(max_spin)

# color offset
c = randrange(0, player_count)    

players = []
for p in range(player_count):
    players.append(player())

    # assign a color, in clockwise order
    players[p].color = color_list[(p+c) % 4]

    players[p].initial_spin = initial_spins[(p+n) % player_count]
    players[p].tie_break_spin = tie_break_spins[(p+n) % player_count]
            
    players[p].cats = 2
    players[p].location = 1


#------------------------------------------------------------------------------    
#  play the game
#------------------------------------------------------------------------------
# all values are zero based until export
g = 0    
r = -1   # round
m = -1    # move
game_over = False

moves = []
while game_over != True:
    r += 1
  
    for p in range(player_count):
        # does this player skip a turn?
        if players[p].skip_next_turn == True:
            players[p].skip_next_turn = False    # reset the flag
            continue    # skip turn
        
        m += 1
        
        moves.append(move())
        moves[m].game_nbr = g
        moves[m].round_nbr = r
        moves[m].move_nbr = m
        moves[m].player_nbr = p
        moves[m].spin_value = spin()
        moves[m].player_prev_move_nbr = players[p].prev_move_nbr
        moves[m].player_prev_location = players[p].location
    
    
        # find the landing space
        if players[p].location + moves[m].spin_value <= 28:
            # before the split
            moves[m].landing_space = players[p].location + moves[m].spin_value
                                              
        elif (players[p].location <= 28 and players[p].cats < path_th) \
             or (players[p].location > 28 and players[p].location <= 33):
            # player doesn't have enough cats for lower path OR
            # player is already on the upper path --> take upper path
            moves[m].landing_space = (players[p].location + moves[m].spin_value - 1) \
                                     % 33 + 1
                                              
        else:    # enough cats for lower path OR already on lower path
            moves[m].landing_space = players[p].location + moves[m].spin_value
            if player[p].location <= 28:
                moves[m].landing_space += 5
            
            if moves[m].landing_space > 40:
                moves[m].landing_space = 40

        # update the player location and move
        players[p].location = moves[m].landing_space
        players[p].prev_move_nbr = m

     
        # initialize cat counts based on the prior move         
        if m == 0:    # first move
            moves[m].game_tray_cats = 50 - 2*player_count
            moves[m].animal_shelter_cats = 0
        else:
            moves[m].game_tray_cats = moves[m-1].game_tray_cats
            moves[m].animal_shelter_cats = moves[m-1].animal_shelter_cats


        # check for player(s) on the same space (take one of their cats)
        for i in range(player_count):
            if i != p \
               and players[i].location == players[p].location \
               and players[i].cats >= 0:
                   
                players[i].cats -= 1
                players[p].cats += 1
      
        
        # take action based on the space
#select_move_action:
        
        # start space or branch point
        if moves[m].landing_space in [1, 28]:
            pass
        
        # spaces where the player gains from the game tray
        elif moves[m].landing_space in [2, 3, 5, 7, 14, 20, 23, 27, 36, 39]:
            # gain 1:
            # 2 = find a cat curled up in a wheelbarrow
            # 3 = bribe a skittish cat with tuna treats
            # 5 = pick up stray
            # 7 = save a cat stuck in a tree
            # 14 = find a stray by the railroad tracks
            # 27 = kitten falls from sky into your pocket
            # 36 = find a feral cat in a dumpster
            
            # spin and gain:
            # 20 = supermarket
            # 23 = pet store
            # 39 = home
            
            if moves[m].landing_space in [20, 23, 39]:
                c = spin()
            else:
                c = 1
                
            if c > moves[m].game_tray_cats and allow_tray_runout == True:
                c = moves[m].game_tray_cats
            
            players[p].cats += c
            moves[m].game_tray_cats -= c


        # spaces where the player gains from the animal shelter 
        elif moves[m].landing_space in [32, 33]:
            # 32 - rescue a grumpy old cat from the pound
            # 33 - rescue all cats from the shelter
    
            if moves[m].landing_space == 33:
                c = moves[m].animal_shelter_cats
            elif moves[m].animal_shelter_cats >= 1 or allow_shelter_runout == False:
                c = 1
           
            players[p].cats += c
            moves[m].animal_shelter_cats -= c
        
        # spaces where the player loses to the animal shelter
        elif moves[m].landing_space in [4, 9, 10, 15, 19, 35]:
            # 4 = beware of dog
            # 9 = park - cat chases butterfly
            # 10 = cat more interested in cardboard box
            # 15 = kitten distracted by bit of fluff
            # 19 = milk truck spill
            # 35 = cat fight
            
            if moves[m].landing_space == 19:
                c = 3
            elif moves[m].landing_space == 35:
                c = 2
            else:
                c = 1
                
            if players[p].cats < c:
                c = players[p].cats
      
            players[p].cats -= c
            moves[m].animal_shelter_cats += c
            
        # animal control confiscates half your cats, then go to start
        elif moves[m].landing_space == 38: 
            c = player[p].cats // 2    # if an odd number, round down
            
            player[p].cats -= c
            moves[m].animal_shelter_cats += c
            
            # remember to record the other player locations and player cat counts at the end of each move
            
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

        # initialize locations from the prior move and update the current player
        for i in range(player_count):
            if i == p:    # current player
                setattr(moves[m], 'player_' + str(i+1) + '_location', \
                        moves[m].location)
            else:
                setattr(moves[m], 'player_' + str(i+1) + '_location', \
                        getattr(moves[m-1], 'player_' + str(i+1) + '_location'))
                
                # if another player is on the space, take one of their cats
                if getattr(moves[m], 'player_' + str(i+1) + '_location') == \
                   moves[m].location:
                    
                    # decrement other player
                    setattr(moves[m], 'player_')
  





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
#    exit()