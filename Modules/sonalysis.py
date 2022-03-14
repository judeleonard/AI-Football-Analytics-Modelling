from matplotlib import tight_layout
from numpy import NaN
from statsbombpy import sb
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mplsoccer.pitch import Pitch

def get_team_in_match(data):
    """Get the team name involved in the match"""
    Team = data.team.unique().tolist()
    return [name for name in Team if name != None]


################## Pass #################################
def generate_barca_player_pass_stats(data):
    """Get the success passes of a selected team in the match"""
    Pass = data[['team', 'action', 'players', 'pass_end_location', 'x', 'y', 'pass_length',
    'pass_outcome', 'end_x', 'end_y']]
    barca_pass = Pass[(Pass['team'] == 'fcb') & (Pass['action']=='pass')]
    barca_pass['pass_outcome'] = barca_pass['pass_outcome'].fillna('Success')
   # barca_pass[['x','y']] = barca_pass['location'].apply(pd.Series)
    #liverpool_pass[['end_x','end_y']] = liverpool_pass['pass_end_location'].apply(pd.Series)
    return barca_pass

def _get_player(barca_pass):
    """Function that returns the players that participated in the team passes """
    Player = barca_pass.players.unique().tolist()
    return [Name for Name in Player if Name != NaN]


def generate_realMadrid_player_pass_stats(data):
    """Get the success passes of a selected team in the match"""
    Pass = data[['team', 'action', 'players', 'pass_end_location', 'x', 'y', 'pass_length',
    'pass_outcome', 'end_x', 'end_y']]
    rma_pass = Pass[(Pass['team'] == 'rma') & (Pass['action']=='pass')]
    rma_pass['pass_outcome'] = rma_pass['pass_outcome'].fillna('Success')
    #rma_pass[['x','y']] = rma_pass['location'].apply(pd.Series)
    #liverpool_pass[['end_x','end_y']] = liverpool_pass['pass_end_location'].apply(pd.Series)
    return rma_pass

############################# shots ######################################

def _get_both_teams_shots(data):  
    shots = data[data['action'] =='shot'][['team', 'players', 'x', 'y', 'shot_outcome']] 
    fcb_shots = shots[shots['team']=='fcb']
    #liverpool_shots[['x','y']] = liverpool_shots['location'].apply(pd.Series)
    real_madrid_shots = shots[shots['team']=='rma']
    #real_madrid_shots[['x','y']] = real_madrid_shots['location'].apply(pd.Series)
    # plot shots
    #fig, ax = plt.subplots(1,2,figsize=(12.5,8))
    #fig.set_facecolor('#22312b')
    #ax.patch.set_facecolor('#22312b')
    pitch = Pitch(layout=(1,2),view='half', orientation='vertical', pitch_color='#22312b', line_color='#c7d5cc',
    figsize=(20, 15))
    fig, ax = pitch.draw()
    sns.scatterplot(fcb_shots['y'], fcb_shots['x'], color='red', alpha=0.7,s=80,hue=fcb_shots['shot_outcome'], data=fcb_shots, ax=ax[0])
    sns.scatterplot(real_madrid_shots['y'], real_madrid_shots['x'], color='red',alpha=0.7,s=80,hue=real_madrid_shots['shot_outcome'], data=real_madrid_shots, ax=ax[1])
    ax[0].set_title("Barcelona FC", fontsize=50, fontfamily='serif')
    ax[1].set_title('Real Madrid', fontsize=50, fontfamily='serif')
    return fig



def get_fcb_shots(data):
    """This function returns all the shot events taken in the Real Madrid team"""
    shots = data[data['action'] =='shot'][['team', 'players', 'location', 'x', 'y', 'shot_outcome']]
    fcb_shots = shots[shots['team']=='fcb']
    #liverpool_shots[['x','y']] = liverpool_shots['location'].apply(pd.Series)
    return fcb_shots

def get_fcb_players_that_took_shots(fcb_shots):
    """This function returns a list of players that took shot in the game"""
    shots_players = fcb_shots.players.unique().tolist()
    return [name for name in shots_players]

def get_rma_shots(data):
    event = data[['team', 'action', 'players', 'location', 'x', 'y', 'shot_outcome']]
    real_madrid_shots = event[(event['team'] == 'rma') & (event['action']=='shot')].reset_index()
   # real_madrid_pass['pass_outcome'] = real_madrid_pass['pass_outcome'].fillna('Success')
    #real_madrid_shots[['x','y']] = real_madrid_shots['location'].apply(pd.Series)
    return real_madrid_shots

def get_rma_players_that_took_shots(real_madrid_shots):
    """This function returns a list of players that took shot in the game"""
    shots_players = real_madrid_shots.players.unique().tolist()
    return [name for name in shots_players]



 ###################################  Heat map ############################
def get_sonaplayer_location(data):
    """function that returns the location of players events"""
    player_location = data[['players', 'x', 'y', 'team']].dropna(subset=['players', 'x', 'y'])
    return player_location

def get_all_sona_player(player_location):
    """aggregateb all the players together in a list for their heatmap"""
    all_player = player_location.players.unique().tolist()
    return [player for player in all_player]