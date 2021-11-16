# -*- coding: utf-8 -*-
"""

"""


from numpy import nan, where
from os import chdir, listdir
from pandas import concat, read_csv


# read in the moves detail
chdir(r'C:\projects\ccl')


# read in the space data
df_spaces = read_csv('board_spaces_info.csv', sep='|')


# --------------------------------------------------------------------------------------------------
# cycle through the output files, and generate summary dataframes
# --------------------------------------------------------------------------------------------------

df_spaces_all = None
df_games_all = None
df_psc_all = None

for f in [f for f in listdir() if 'moves_output_' in f]:
    
    # read in the moves file (add the win column from the players file)
    df = read_csv(f).assign(scenario_name=f)\
         .rename(columns={'player_prev_location' : 'prev_space'})\
         .merge(read_csv(f.replace('moves', 'player'), usecols=[0, 1, 5, 8]), 
                on=['game_nbr', 'player_nbr'], how='left')                                   


    # flag times a player passed the decision point
    df['passed_split'] = where( (df['prev_space'] <= 28) & (df['prev_space'] > 23)
                                & ((df['landing_space'] > 28) | (df['landing_space'] == 1)), 1, 0)
    
    # flag times a player passed to the left branch
    df['passed_split_left'] = where( (df['passed_split'] == 1) & (df['landing_space'] >= 34), 1, 0)
    
    
    # number of cats at time of decision point
    df['split_cats'] = where(df['passed_split'] == 1, df['player_prev_cats'], nan)
    df['split_left_cats'] = where(df['passed_split_left'] == 1, df['player_prev_cats'], nan)
    df['split_right_cats'] = where((df['passed_split'] == 1) & (df['passed_split_left'] == 0), 
                                    df['player_prev_cats'], nan)
        
                                  
    # landed on the space as a redirct or based on a spin
    df['redirect'] = where(df['spin_value'].isna(), 1, 0)
        
    
    # the player that landed on home won (or tied)
    df['home_player_won'] = where((df['landing_space'] == 40) & (df['win'] == 1), 1, 0)
    
 
    
    
    # append to the summary dataframes

    # create columns for the passed split cats histogram
    df_psc_all = concat([df_psc_all, 
                         df[df['passed_split'] == 1]\
                         .groupby(['scenario_name', 'landing_space', 'split_cats'])\
                         .agg(move_count=('move_nbr', 'count'))\
                         .reset_index()])

    
    # summary by landing space
    df_spaces_all = concat([df_spaces_all, 
                            df.groupby(['scenario_name', 'landing_space'])\
                              .agg(move_count=('move_nbr', 'count'),
                                   passed_split=('passed_split', 'sum'),
                                   passed_split_left=('passed_split_left', 'sum'),
                                   split_right_cats=('split_right_cats', 'sum'),\
                                   split_left_cats=('split_left_cats', 'sum'),
                                   redirect_count=('redirect', 'sum'),
                                   home_player_won=('home_player_won', 'sum'))\
                              .reset_index()])
    
    # summary by game
    df_games_all = concat([df_games_all, 
                           df.groupby(['scenario_name', 'game_nbr'])\
                             .agg(passed_split=('passed_split', 'sum'),
                                  passed_split_left=('passed_split_left', 'sum'),
                                  split_right_cats=('split_right_cats', 'sum'),\
                                  split_left_cats=('split_left_cats', 'sum'),
                                  redirect_count=('redirect', 'sum'),
                                  home_player_won=('home_player_won', 'sum'))\
                             .reset_index()])    
        
    print(f)


# --------------------------------------------------------------------------------------------------
# summary by space
# --------------------------------------------------------------------------------------------------

df_spaces_all.to_csv('summary_by_space.csv', index=False)


# --------------------------------------------------------------------------------------------------
# histogram output
# --------------------------------------------------------------------------------------------------

df_psc_all.to_csv('summary_passed_split_cats_for_histogram.csv', index=False)


# --------------------------------------------------------------------------------------------------
# summary by game
# --------------------------------------------------------------------------------------------------

# read in the players and games files
df_tie = concat([read_csv(f, usecols=[0, 1, 8]).assign(scenario_name=f)
                 for f in listdir() if 'player_' in f and 'zip' not in f])\
         .groupby(['scenario_name', 'game_nbr'])['win'].sum().reset_index()
df_games = concat([read_csv(f) for f in listdir() if 'games_output_' in f and 'zip' not in f])

# count ties    
df_tie['tied'] = where(df_tie['win'] > 1, 1, 0)

# normalize the scenario name
df_tie['scenario_name'] = df_tie['scenario_name'].str.extract('player_output_(.*)\.csv')
df_games_all['scenario_name'] = df_games_all['scenario_name'].str.extract('moves_output_(.*)\.csv')


# add tie info and summary info to the game data
df_games = df_games.merge(df_tie, on=['scenario_name', 'game_nbr'], how='inner')\
                   .merge(df_games_all, on=['scenario_name', 'game_nbr'], how='inner')
df_games.drop(columns=['win'], inplace=True)

# output the summary file
df_games.to_csv('summary_by_game.csv', index=False)







# f = 'moves_output_01_original_rules.csv'
#     df = read_csv(f).assign(scenario_name=f)\
#          .rename(columns={'player_prev_location' : 'prev_space'})\
#          .merge(read_csv(f.replace('moves', 'player'), usecols=[0, 1, 5, 8]), 
#                 on=['game_nbr', 'player_nbr'], how='left')                                   



# df[(df['passed_split'] == 1) & (df['passed_split_left'] == 0) & (df['player_prev_cats'] == 10)]

# df.iloc[1553]



# df['split_cats'].sum()
# df[df['split_cats']  < 0]
