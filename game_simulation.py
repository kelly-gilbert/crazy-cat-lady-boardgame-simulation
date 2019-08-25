#!/usr/bin/env python3

"""

"""

from time import time
from random import randrange
from random import choice
import pandas as pd


# Player class
class player():
    def __init__(self):
        self.game_nbr = 0
        self.color = ''
        self.initial_spin = 0
        self.tie_break_spin = 0
        self.location = 0
        self.skip_next_turn = False
        self.cats = 0
        self.win = 0
        self.prev_move_nbr = 0
        

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
        self.player_prev_move_nbr = 0
        self.player_prev_location = 0


def spin():
    """ return a number between 1 and 6 """
    return randrange(1,7)


def create_player_list(game_nbr, player_count):
    """
    generate a list of player objects to start a new game
    """
    
    color_list = ['pink', 'blue', 'yellow', 'orange']   # clockwise order of colors  
    players = []
    
    # spin to see which player goes first
    # this isn't absolutely necessary (a starting player could be chosen at
    # random), however, I wanted to simulate actual game play, including 
    # tracking how many times the initial spin was tied
    
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
    
        
    # offset the player order, based on the initial spin
    if tie_break_loops == 0:    # initial spin not tied
        n = initial_spins.index(max_spin)
    else:
        n = [k for (k,v) in tie_break_spins.items() if v == max_spin][0]
    
    
    # color offset
    c = randrange(0, player_count)    
    
    for p in range(player_count):
        players.append(player())
    
        # assign a color, in clockwise order
        players[p].game_nbr = game_nbr
        players[p].color = color_list[(p+c) % 4]
    
        players[p].initial_spin = initial_spins[(p+n) % player_count]
        players[p].tie_break_spin = tie_break_spins[(p+n) % player_count]
                
        players[p].cats = 2
        players[p].location = 1

    return players


def find_highest_player(players, find_highest, current_player=None):
    """
    returns a dictionary of player(s) with the highest/lowest cat count
    
    players = list of player objects
    find_highest = boolean (True = find highest, False = find lowest)
    optional argument = the current player's number
    """

    curr_cats = attr_dict(players, 'cats')
    
    # if specified, ignore the current player
    if current_player is not None:
        del curr_cats[p]    
    
    # find the min or max number of cats
    if find_highest == True:
        max_cats = max(v for v in curr_cats.values())
    else:
        max_cats = min(v for v in curr_cats.values())
    
    # return a dictionary of players that match
    max_dict = {k:v for (k,v) in curr_cats.items() if v == max_cats}

    return max_dict


def end_move(move, players):
    """
    record the player locations and cat counts at the end of a move
    """
    
    for p in range(len(players)):
        setattr(move, 'player_' + str(p+1) + '_location', players[p].location)
        setattr(move, 'player_' + str(p+1) + '_cats', players[p].cats)
        

def end_game():
    pass  


def attr_list(list_name, attr_name):
    """
    For a list of objects, return a list of the specified attribute
    """
    attr_list = []
    for i in range(len(list_name)):
        attr_list.append(getattr(list_name[i], attr_name))
        
    return attr_list


def attr_dict(list_name, attr_name):
    """
    For a list of objects, return a dictionary of the specified attribute,
    where the key is the position in the list, and the value is the attribute
    """
    attr_dict = {}
    for i in range(len(list_name)):
        attr_dict[i] = getattr(list_name[i], attr_name)
        
    return attr_dict



  
#------------------------------------------------------------------------------    
# simulation settings
#------------------------------------------------------------------------------
game_count = 10         # number of games to simulate
progress_frequency = 100    # print progress every n games
player_count = 4
allow_ties = False       # allow ties at the end of the game
choose_highest = True    # when given the option to take from/give to a player, 
                         # choose the player with the most/fewest) cats
allow_tray_runout = True       # allow the tray to run out
allow_shelter_runout = True    # allow the animal shelter to run out

path_th = 10             # threshold for entering the branched path


#------------------------------------------------------------------------------    
#  cycle through simulated games
#------------------------------------------------------------------------------
    
start_time = time()
  
for game_nbr in range(game_count):
    
    # all values are zero based until export
    g = 0    
    r = 0    # round
    m = 0    # move
    p = 0    # player
    game_over = False
    continue_turn = False
    
    # generate a list of players for this game
    players = create_player_list(g, player_count)
   
    # play the game
    moves = []
    
    while game_over != True:
        
        if continue_turn == False:
            # if it is not a redirect, initialize the move and get the
            # landing space
            
            # move to the next player
            if m == 0:
                p = 0
            else:
                p = (p + 1) % 4
            
            # advance the round number
            if m > 0:
                if p == 0 and moves[m-1].player_nbr != p:
                    r += 1
                
            # does this player skip a turn?
            if players[p].skip_next_turn == True:
                players[p].skip_next_turn = False    # reset the flag
                continue    # skip turn
                    
            moves.append(move())
            moves[m].game_nbr = g
            moves[m].round_nbr = r
            moves[m].move_nbr = m
            moves[m].player_nbr = p
            moves[m].spin_value = spin()
            moves[m].player_prev_move_nbr = players[p].prev_move_nbr
            moves[m].player_prev_location = players[p].location
        
            players[p].prev_move_nbr = m
            print(moves[m].spin_value)
        
        else:
            continue_turn = False
                
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


        # update the player location
        players[p].location = moves[m].landing_space
        print(players[p].location)

                 
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
               and moves != 0 \
               and players[i].location == players[p].location \
               and players[i].cats >= 0:
                   
                players[i].cats -= 1
                players[p].cats += 1
      
        
        # -- take action based on the space -----------------------------------
        
        # start space or branch point (do nothing)
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
            
            # number of cats
            if moves[m].landing_space in [20, 23, 39]:
                c = spin()
            else:
                c = 1
                
            if c > moves[m].game_tray_cats and allow_tray_runout == True:
                c = moves[m].game_tray_cats
            
            players[p].cats += c
            moves[m].game_tray_cats -= c
            print(attr_list(players, 'cats'))
            print(moves[m].game_tray_cats)
 
        # spaces where the player loses to the game tray
        elif moves[m].landing_space == 26:
            # 26 = veterinarial

            c = spin
            if c > players[p].cats:
                c = players[p].cats
                
            players[p].cats -= c
            moves[m].game_tray_cats += c


        # spaces where the player gains from the animal shelter 
        elif moves[m].landing_space in [32, 33]:
            # 32 - rescue a grumpy old cat from the pound
            # 33 - rescue all cats from the shelter
    
            if moves[m].landing_space == 33:
                c = moves[m].animal_shelter_cats
            elif moves[m].animal_shelter_cats >= 1 or allow_shelter_runout == False:
                c = 1
            else: 
                c = 0
           
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
            
            #add new move
            end_move(moves[m], players)
            m += 1
                        
            moves.append(move())
            moves[m].game_nbr = g
            moves[m].round_nbr = r
            moves[m].move_nbr = m
            moves[m].player_nbr = p
            moves[m].spin_value = ''
            moves[m].player_prev_move_nbr = players[p].prev_move_nbr
            moves[m].player_prev_location = players[p].location
            moves[m].landing_space = 1
            
            players[p].prev_move_nbr = m
            continue_turn = True   
            continue
        

        # spin again
        elif moves[m].landing_space in [6, 13, 24, 31]:
            # re-use the current player number (when the loop restarts, it 
            # will add one to the player number)
            p -= 1
    
    
        # lose next turn
        elif moves[m].landing_space in [8, 22, 37]:
            # 8 pick catnip
            # 22 stop to pet a cat
            # 37 hairball
        
            players[p].skip_next_turn = True

    
        # take one from any player
        elif moves[m].landing_space in [11, 17]:
            # 11 catsit
            # 17 fall in love with neighborhood cat
    
            # choose player
            if choose_highest == True:
                max_dict = find_highest_player(players, True, p)                
                take_from_player = choice(list(max_dict.items()))[0]
            else:    # choose a random player
                player_nbrs = list(range(player_count))
                del player_nbrs[p]
                take_from_player = randrange(len(player_nbrs))
              
            if players[take_from_player].cats > 0:
                players[p].cats += 1
                players[take_from_player].cats -= 1
              
        
        # take one cat from each player
        elif moves[m].landing_space == 30:
            # 30 catnip in your pocket lures cats

            for i in range(player_count):
                if i != p and players[i].cats > 0:
                    player[p].cats += 1
                    players[i].cats =- 1
     
      
        # redirect to another space
        elif moves[m].landing_space in [12, 16, 18, 21, 29, 34]:
            # 12 kitty litter emergency (supermarket)
            # 16 forgot cat food coupons (return to start)
            # 18 pursue a mangy cat (park)
            # 21 sick cat (vet)
            # 29 hear the mews of caged cats (animal shelter)
            # 34 forgot flea collars (vet)
    
            end_move(moves[m], players)
            m += 1
            
            # add new move
            moves.append(move())
            moves[m].game_nbr = g
            moves[m].round_nbr = r
            moves[m].move_nbr = m
            moves[m].player_nbr = p
            moves[m].spin_value = ''
            moves[m].player_prev_move_nbr = players[p].prev_move_nbr
            moves[m].player_prev_location = players[p].location
            
            players[p].prev_move_nbr = m
            
            # set the new location
            if moves[m-1].landing_space == 12:
                moves[m].landing_space = 20    # supermarket
            elif moves[m-1].landing_space == 16:
                moves[m].landing_space = 1     #start
            elif moves[m-1].landing_space == 18:
                moves[m].landing_space == 9    # park
            elif moves[m-1].landing_space == 21:
                moves[m].landing_space == 26    # vet                
            elif moves[m-1].landing_space == 29:
                moves[m].landing_space == 33    # animal shelter
            elif moves[m-1].landing_space == 34:
                moves[m].landing_space == 26    # vet
        
            continue_turn = True 
            continue
       

        # wildcat card
        elif moves[m].landing_space == 25:
            
            # select a card at random (they are shuffled prior to each use)
            n = randrange(0,4)
          
            if n == 0:
                # Your great aunt passes away, leaving you eight cats 
                # and a box of yarn.
          
                c = 8  
                if moves[m].game_tray_cats < 8 and allow_tray_runout == True:
                    c = moves[m].game_tray_cats
                    
                players[p] += c
                moves[m].game_tray_cats -= c
            
            elif n == 1:
                # You are overcome with the intese desire to own 
                # every cat you see.
                # Each player spins, then gives you that many of their cats.
          
                for i in range(player_count):
                    if i != p:
                        c = spin()
                        if players[i].cats < c:
                            c = players[i].cats
                    
                    players[p] += c
                    players[i] -= c
    
            else: 
                # there are two copies of this card
                # You feel sorry for a friend who doesn't have enough cats.
                # Choose a player, spin, then give them that many of your cats.
    
                # choose player
                if choose_highest == True:
                    min_dict = find_highest_player(players, False, p)                
                    give_to_player = choice(list(min_dict.items()))[0]
                else:    # choose a random player
                    player_nbrs = list(range(player_count))
                    del player_nbrs[p]
                    give_to_player = randrange(len(player_nbrs))
                  
                if player[p].cats > 0:
                    player[p].cats -= 1
                    player[give_to_player].cats += 1
                  
    
        # home space - end game
        elif moves[m].landing_space == 40:
            
            # find highest player
            max_dict = find_highest_player(players, True)
            
            # if tied
            if allow_ties == True and len(max_dict) > 1:
                pass
            
            # mark the winner(s)
            for k in range(max_dict.keys()):
                players[k].win = 1
            
            game_over = True  
            break


        # end the move
        end_move(moves[m], players)
        m += 1


    # append the simulation results      
    players_df = pd.DataFrame([vars(i) for i in players])
    players_df.to_csv(path_or_buf='player_output.csv', mode='a')
    
    games_df = pd.DataFrame([vars(i) for i in moves])
    games_df.to_csv(path_or_buf='games_output.csv', mode='a')

    # print progress
    if (g+1) % progress_frequency == 0:
        print(str(g) + ' games completed...')
     
# simulation complete
print('Done.')