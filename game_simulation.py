#!/usr/bin/env python3

"""
Simulate game play for the Crazy Cat Lady board game
https://www.amazon.com/Accoutrements-11893-Crazy-Lady-Game/dp/B001J7AIAU

-- Author: Kelly Gilbert
-- Date: 2019-08-19
-- Requirements: none
"""

from datetime import datetime as dt
from datetime import timedelta
from pandas import DataFrame, merge
from random import choice, randrange


# -------------------------------------------------------------------------------------------------
# class definitions
# -------------------------------------------------------------------------------------------------

# player class
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


# move class
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
        self.player_prev_cats = 0


# -------------------------------------------------------------------------------------------------
# functions
# -------------------------------------------------------------------------------------------------

def spin():
    """ return a number between 1 and 6 """
    return randrange(1, 7)


def create_player_list(game_nbr, player_count):
    """
    generate a list of player objects to start a new game
    """

    color_list = ['pink', 'blue', 'yellow', 'orange']   # clockwise order of colors
    players = []


    # spin to see which player goes first
    # this isn't absolutely necessary (a starting player could be chosen at random), however,
    # I wanted to simulate actual game play, including tracking how many times the initial spin
    # was tied

    initial_spins = [spin() for p in range(0, player_count)]

    # tie break the initial spin, if necessary
    tie_break_spins = initial_spins.copy()
    tie_break_loops = 0

    while sum(v == max(tie_break_spins) for v in tie_break_spins) > 1:
        tie_break_spins = [spin() if v == max(tie_break_spins) else 0 for v in tie_break_spins]
        tie_break_loops += 1


    # offset the player order, based on the initial spin
    if tie_break_loops == 0:    # initial spin not tied
        n = initial_spins.index(max(initial_spins))
    else:
        n = tie_break_spins.index(max(tie_break_spins))


    # color offset
    c = randrange(0, player_count)

    for p in range(player_count):
        players.append(player())

        # assign a color, in clockwise order
        players[p].game_nbr = game_nbr
        players[p].color = color_list[(p+c) % len(color_list)]

        players[p].initial_spin = initial_spins[(p+n) % player_count]
        players[p].tie_break_spin = tie_break_spins[(p+n) % player_count]

        players[p].cats = starting_cat_count
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
    if find_highest:
        max_cats = max(v for v in curr_cats.values())
    else:
        max_cats = min(v for v in curr_cats.values())

    # return a dictionary of players that match
    max_dict = {k:v for (k, v) in curr_cats.items() if v == max_cats}

    return max_dict


def end_move(move, players):
    """
    record the player locations and cat counts at the end of a move
    """

    for p in range(len(players)):
        setattr(move, f'player_{p+1}_location', players[p].location)
        setattr(move, f'player_{p+1}_cats', players[p].cats)


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


def find_landing_space(current_space, spin, cats, path_th):
    """
    Determine the player's landing space after a spin
    """

    if current_space + spin <= 28:
        # before the split
        landing_space = current_space + spin

    elif (current_space <= 28 and cats < path_th) \
         or (current_space > 28 and current_space <= 33):
        # player doesn't have enough cats for lower path OR
        # player is already on the upper path --> take upper path
        # (this could loop back to start)
        landing_space = (current_space + spin - 1) % 33 + 1

    else:    # enough cats for lower path OR already on lower path
        landing_space = current_space + spin + (5 if current_space < 34 else 0)

        if landing_space > 40:
            landing_space = 40

    return landing_space


# --------------------------------------------------------------------------------------------------
# simulation settings
# --------------------------------------------------------------------------------------------------

scenario_name = '01_original_rules'             # scenario name for this run (added to filename)
game_count = 100000             # number of games to simulate
progress_frequency = 5000      # print progress every n games
player_count = 4               # number of players in the game (2-4)
choose_highest = True          # always take from the player with the most cats (or give to the
                               #     player with the fewest cats); if false, choose at random

allow_tray_runout = True       # allow the tray to run out (default = True)
allow_shelter_runout = True    # allow the animal shelter to run out (default = True)

# multipliers for house rules (to play with official rules, set all factors to 1)
tray_factor = 1                # cats gained from/lost to the main tray
shelter_factor = 1             # cats gained from/lost to the shelter
player_factor = 1              # cats gained from/lost to another player

starting_cat_count = 2         # starting cat count for each player (default=2)

path_th = 10                   # threshold # cats for entering the branched path (default=10)


# --------------------------------------------------------------------------------------------------
#  cycle through simulated games
# --------------------------------------------------------------------------------------------------

overall_start_time = dt.now()
games_list = []
players_list = []
moves_list = []

for g in range(game_count):

    start_time = dt.now()

    # all values are zero based until export
    r = 0    # round
    m = 0    # move
    p = 0    # player
    game_over = False
    continue_turn = False

    # generate a list of players for this game
    players = create_player_list(g, player_count)

    # play the game
    moves = []

    while not game_over:

        if not continue_turn:
            # if it is not a redirect, initialize the move and get the landing space

            # advance to the next player
            if m == 0:
                p = 0
            else:
                p = (p + 1) % player_count

            # advance the round number
            if m > 0 and p == 0 and moves[m-1].player_nbr != p:
                r += 1

            # does this player skip a turn?
            if players[p].skip_next_turn:
                players[p].skip_next_turn = False    # reset the flag
                continue    # skip turn

            # create a new move
            moves.append(move())
            moves[m].game_nbr = g
            moves[m].round_nbr = r
            moves[m].move_nbr = m
            moves[m].player_nbr = p
            moves[m].spin_value = spin()
            moves[m].player_prev_move_nbr = players[p].prev_move_nbr
            moves[m].player_prev_location = players[p].location
            moves[m].player_prev_cats = players[p].cats

            players[p].prev_move_nbr = m


            # find the new landing space
            moves[m].landing_space = find_landing_space(players[p].location, moves[m].spin_value,
                                                        players[p].cats, path_th)

        else:
            continue_turn = False    # reset the flag


        # update the player's current location
        players[p].location = moves[m].landing_space


        # initialize cat counts based on the prior move
        if m == 0:    # first move
            moves[m].game_tray_cats = 50 - starting_cat_count*player_count
            moves[m].animal_shelter_cats = 0
        else:
            moves[m].game_tray_cats = moves[m-1].game_tray_cats
            moves[m].animal_shelter_cats = moves[m-1].animal_shelter_cats


        # check for player(s) on the same space (take one of their cats)
        for i in range(player_count):
            if i != p \
               and moves != 0 \
               and players[i].location == players[p].location \
               and players[i].cats > 0:
                   
                c = min(players[i].cats, 1 * player_factor)

                players[i].cats -= c
                players[p].cats += c


# --------------------------------------------------------------------------------------------------
#       take action based on the landing space
# --------------------------------------------------------------------------------------------------

        # start space or branch point (do nothing)
        if moves[m].landing_space in [1, 28]:
            pass


        # spin again
        elif moves[m].landing_space in [6, 13, 24, 31]:
            # re-use the current player number (when the loop restarts, it will increment
            # the player number)
            p -= 1


        # lose next turn
        elif moves[m].landing_space in [8, 22, 37]:
            # 8 pick catnip
            # 22 stop to pet a cat
            # 37 hairball

            players[p].skip_next_turn = True


        # redirect to another space
        elif moves[m].landing_space in [12, 16, 18, 21, 29, 34]:
            # 12 kitty litter emergency (supermarket)
            # 16 forgot cat food coupons (return to start)
            # 18 pursue a mangy cat (park)
            # 21 sick cat (vet)
            # 29 hear the mews of caged cats (animal shelter)
            # 34 forgot flea collars (vet)

            # end the current move and initialize the next one
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
            moves[m].player_prev_cats = players[p].cats

            players[p].prev_move_nbr = m

            # set the new location
            redirects = {12:20, 16:1, 18:9, 21:26, 29:33, 34:26}
            # 20 = supermarket
            #  1 = start
            #  9 = park
            # 26 = vet
            # 33 = animal shelter
            # 26 = vet

            moves[m].landing_space = redirects[moves[m-1].landing_space]
            continue_turn = True

            continue



        # --- GAINS ---

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
                c = spin() * tray_factor
            else:
                c = 1 * tray_factor

            # adjust number of cats based on tray runout setting
            if c > moves[m].game_tray_cats and allow_tray_runout:
                c = moves[m].game_tray_cats

            # increment/decrement the player/tray counts
            players[p].cats += c
            moves[m].game_tray_cats -= c


        # take one from any player
        elif moves[m].landing_space in [11, 17]:
            # 11 catsit
            # 17 fall in love with neighborhood cat

            # choose player
            if choose_highest:
                max_dict = find_highest_player(players, True, p)
                take_from_player = choice(list(max_dict.items()))[0]
            else:    # choose a random player
                player_nbrs = list(range(player_count))
                del player_nbrs[p]
                take_from_player = choice(player_nbrs)

            # number of cats
            c = 1 * player_factor

            # adjust for source player's current cat count
            if players[take_from_player].cats < c:
                c = players[take_from_player].cats

            # increment/decrement cat counts
            players[p].cats += c
            players[take_from_player].cats -= c
            
            
        # take one cat from each player
        elif moves[m].landing_space == 30:
            # 30 catnip in your pocket lures cats

            c = 1 * player_factor

            for i in range(player_count):
                if i != p:
                    if players[i].cats < c:
                        players[p].cats += players[i].cats
                        players[i].cats = 0
                    else:
                        players[p].cats += c
                        players[i].cats -= c


        # spaces where the player gains from the animal shelter
        elif moves[m].landing_space in [32, 33]:
            # 32 - rescue a grumpy old cat from the pound
            # 33 - rescue all cats from the shelter

            if moves[m].landing_space == 33:
                c = max(0, moves[m].animal_shelter_cats)
            else:
                c = 1 * shelter_factor

            if c > moves[m].animal_shelter_cats and allow_shelter_runout:
                c = moves[m].animal_shelter_cats

            players[p].cats += c
            moves[m].animal_shelter_cats -= c



        # --- LOSSES ---

        # spaces where the player loses to the animal shelter
        elif moves[m].landing_space in [4, 9, 10, 15, 19, 35]:
            # 4 = beware of dog
            # 9 = park - cat chases butterfly
            # 10 = cat more interested in cardboard box
            # 15 = kitten distracted by bit of fluff
            # 19 = milk truck spill
            # 35 = cat fight

            # number of cats
            if moves[m].landing_space == 19:
                c = 3 * shelter_factor
            elif moves[m].landing_space == 35:
                c = 2 * shelter_factor
            else:
                c = 1 * player_factor

            # adjust for players current cat count                
            if players[p].cats < c:
                c = players[p].cats

            # increment/decrement the player/shelter cats
            players[p].cats -= c
            moves[m].animal_shelter_cats += c


        # spaces where the player loses to the game tray
        elif moves[m].landing_space == 26:
            # 26 = veterinarian

            c = spin() * player_factor

            if c > players[p].cats:
                c = players[p].cats

            players[p].cats -= c
            moves[m].game_tray_cats += c


        # animal control confiscates half your cats, then go to start
        # note: since this space already has a factor, the player_factor
        # is not applied
        elif moves[m].landing_space == 38:
            
            c = players[p].cats // 2    # if an odd number, round down

            players[p].cats -= c
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
            moves[m].player_prev_cats = players[p].cats
            moves[m].landing_space = 1

            players[p].prev_move_nbr = m
            continue_turn = True

            continue


        # wildcat card
        elif moves[m].landing_space == 25:

            # select a card at random (they are shuffled prior to each use)
            # NOTE: these were the cards included in the game that I played. The cards may be
            #       be different from box to box

            n = randrange(0, 4)

            if n == 0:
                # Your great aunt passes away, leaving you eight cats and a box of yarn.
                # No factor is applied

                c = 8

                if moves[m].game_tray_cats < c and allow_tray_runout:
                    c = moves[m].game_tray_cats

                players[p].cats += c
                moves[m].game_tray_cats -= c

            elif n == 1:
                # You are overcome with the intese desire to own every cat you see. Each player
                # spins, then gives you that many of their cats.

                for i in range(player_count):
                    if i != p:
                        c = spin() * player_factor

                        if players[i].cats < c:
                            c = players[i].cats

                    players[p].cats += c
                    players[i].cats -= c

            else:
                # there are two copies of this card
                # You feel sorry for a friend who doesn't have enough cats. Choose a player, spin,
                # then give them that many of your cats.

                # choose player
                if choose_highest:
                    min_dict = find_highest_player(players, False, p)
                    give_to_player = choice(list(min_dict.items()))[0]
                else:    # choose a random player
                    player_nbrs = list(range(player_count))
                    del player_nbrs[p]
                    give_to_player = randrange(len(player_nbrs))

                c = spin() * player_factor

                if c > players[p].cats:
                    c = players[p].cats

                players[p].cats -= c
                players[give_to_player].cats += c


        # home space - end game
        elif moves[m].landing_space == 40:

            # find highest player(s)
            max_dict = find_highest_player(players, True)

            # mark the winner(s)
            for k in max_dict.keys():
                players[k].win = 1

            game_over = True


        # end the move
        end_move(moves[m], players)
        m += 1


# --------------------------------------------------------------------------------------------------
#   output the results
# --------------------------------------------------------------------------------------------------

    # add the game, person, and move data to temporary lists
    games_list.append( {'scenario_name' : scenario_name, \
                        'game_nbr' : g, \
                        'player_count' : player_count, \
                        'choose_highest' : choose_highest, \
                        'allow_tray_runout' : allow_tray_runout, \
                        'allow_shelter_runout' : allow_shelter_runout, \
                        'tray_factor' : tray_factor, \
                        'shelter_factor' : shelter_factor, \
                        'player_factor' : player_factor, \
                        'starting_cat_count' : starting_cat_count, \
                        'path_th' : path_th, \
                        'run_time_s':(dt.now() - start_time).microseconds / 1000 / 1000
                       })
        
    players_list += [{**{ 'player_nbr' : i + 1}, **vars(p)} for i, p in enumerate(players)]
    moves_list += [vars(i) for i in moves]


    # if a breakpoint, output the data
    if (g + 1) % progress_frequency == 0 or g == game_count - 1:

        # if it is the first checkpoint, output the headers
        if g == progress_frequency - 1:
            output_headers = True
            output_mode = 'w'
        else:
            output_headers = False
            output_mode = 'a'


        # output the player data
        players_df = DataFrame(players_list)
        players_df.to_csv(path_or_buf=f'player_output_{scenario_name}.csv', \
                         mode=output_mode, index=False, header=output_headers)
    
        # output the moves history
        moves_df = DataFrame(moves_list)
        moves_df['player_nbr'] += 1    # change from zero to one-based
        moves_df.to_csv(path_or_buf=f'moves_output_{scenario_name}.csv', \
                        mode=output_mode, index=False, header=output_headers)
            
    
        # output the game attributes
        games_df = DataFrame.from_dict(games_list)
        games_df = games_df.merge(moves_df.groupby('game_nbr').agg(rounds=('round_nbr', 'nunique'),
                                                                   moves=('move_nbr', 'count')),
                                  left_on='game_nbr', right_index=True)    
        games_df.to_csv(path_or_buf=f'games_output_{scenario_name}.csv', \
                        mode=output_mode, \
                        index=False, header=output_headers)
            
        # reset the lists    
        games_list = []
        players_list = []
        moves_list = []
    

        # print status message
        print(f'{g+1} games completed...')


# simulation complete
print(f'Completed {game_count} games in {(dt.now() - overall_start_time).seconds} seconds')
