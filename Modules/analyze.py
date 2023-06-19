from matplotlib import tight_layout
from numpy import NaN
from statsbombpy import sb
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from mplsoccer.pitch import Pitch
import plotly.express as px
pd.set_option('display.max_columns', 100)


#data = sb.competitions()
@st.cache(allow_output_mutation=True)
def fetch_data():
    """Fetch available statsbomb data from API"""
    data = sb.events(match_id=18245)
    return data

def get_team_in_match(data):
    """Get the team name involved in the match"""
    Team = data.team.unique().tolist()
    return [name for name in Team if name != None]
#----------------- Passes------------------------------------------------#
def generate_liverpool_player_pass_stats(data):
    """Get the success passes of a selected team in the match"""
    event = data[['team', 'type', 'minute', 'location', 'player', 'pass_end_location', 'pass_recipient', 'pass_length',
    'pass_outcome', 'pass_height']]
    liverpool_pass = event[(event['team'] == 'Liverpool') & (event['type']=='Pass')].sort_values('minute').reset_index()
    liverpool_pass['pass_outcome'] = liverpool_pass['pass_outcome'].fillna('Success')
    liverpool_pass[['x','y']] = liverpool_pass['location'].apply(pd.Series)
    liverpool_pass[['end_x','end_y']] = liverpool_pass['pass_end_location'].apply(pd.Series)
    return liverpool_pass
  

def get_player(liverpool_pass):
    """Function that returns the players that participated in the team passes """
    Player = liverpool_pass.player.unique().tolist()
    return [Name for Name in Player if Name != NaN]

def visualize_players_passes(liverpool_pass):
    """This function visualizes the pass successes and failures of each player in the game"""
    fig, ax = plt.subplots(figsize=(12.5,8))
    fig.set_facecolor('#22312b')
    ax.patch.set_facecolor('#22312b')
    pitch = Pitch(pitch_type='statsbomb', orientation='horizontal', pitch_color='#22312b', line_color='#c7d5cc',
    figsize=(16, 11), constrained_layout=True, tight_layout=True)
    pitch.draw(ax=ax)
    plt.gca().invert_yaxis()
    return fig
    # player_pass = liverpool_pass[(liverpool_pass['player']== get_player) & (liverpool_pass['minute'] < 91)].reset_index()
    # for i in range(len(player_pass)):
    #     if player_pass['pass_outcome'][i] == 'Success':
    #         ax.plot((player_pass['x'][i],player_pass['end_x'][i]),(player_pass['y'][i],player_pass['end_y'][i]), color='green')
    #         ax.scatter(player_pass['x'][i], player_pass['y'][i],color='green')
    #     if (player_pass['pass_outcome'][i]=='Success') & (player_pass['pass_height'][i] =='High Pass'):
    #         ax.plot((player_pass['x'][i],player_pass['end_x'][i]),(player_pass['y'][i],player_pass['end_y'][i]),ls = '--',color='green')
    #         ax.scatter(player_pass['x'][i],player_pass['y'][i],color='green')
    #     if player_pass['pass_outcome'][i] == 'Incomplete':
    #         ax.plot((player_pass['x'][i],player_pass['end_x'][i]),(player_pass['y'][i],player_pass['end_y'][i]),color='red')
    #         ax.scatter(player_pass['x'][i],player_pass['y'][i],color ='red')

    #return fig

# def get_shots_data(data):
#     """This function returns all the shot events that happened in a game"""
#     shots = data[data['type'] =='Shot']
#     shots = shots[['team', 'player', 'location', 'shot_aerial_won', 'shot_body_part',
#             'shot_end_location', 'shot_first_time', 'shot_freeze_frame','shot_key_pass_id', 'shot_one_on_one',
#             'shot_outcome',' shot_redirect', 'shot_statsbomb_xg', 'shot_technique', 'shot_type', 'minute']]
#     return shots

def generate_real_madrid_pass_stats(data):
    """Get the success passes of a selected team in the match"""
    event = data[['team', 'type', 'minute', 'location', 'player', 'pass_end_location', 'pass_recipient', 'pass_length',
    'pass_outcome', 'pass_height']]
    real_madrid_pass = event[(event['team'] == 'Real Madrid') & (event['type']=='Pass')].sort_values('minute').reset_index()
    real_madrid_pass['pass_outcome'] = real_madrid_pass['pass_outcome'].fillna('Success')
    real_madrid_pass[['x','y']] = real_madrid_pass['location'].apply(pd.Series)
    real_madrid_pass[['end_x','end_y']] = real_madrid_pass['pass_end_location'].apply(pd.Series)
    return real_madrid_pass

def get_player(real_madrid_pass):
    """Function that returns the players that participated in the team passes """
    Player = real_madrid_pass.player.unique().tolist()
    return [Name for Name in Player if Name != NaN]

#------------------- ---shots------------------------------------#

def get_both_teams_shots(data):  
    shots = data[data['type'] =='Shot'][['team', 'player', 'location', 'shot_aerial_won', 'shot_body_part',
            'shot_end_location', 'shot_first_time', 'shot_freeze_frame','shot_key_pass_id', 'shot_one_on_one',
            'shot_outcome', 'shot_redirect', 'shot_statsbomb_xg', 'shot_technique', 'shot_type', 'minute']] 
    liverpool_shots = shots[shots['team']=='Liverpool']
    liverpool_shots[['x','y']] = liverpool_shots['location'].apply(pd.Series)
    real_madrid_shots = shots[shots['team']=='Real Madrid']
    real_madrid_shots[['x','y']] = real_madrid_shots['location'].apply(pd.Series)
    # plot shots
    #fig, ax = plt.subplots(1,2,figsize=(12.5,8))
    #fig.set_facecolor('#22312b')
    #ax.patch.set_facecolor('#22312b')
    pitch = Pitch(layout=(1,2),view='half', orientation='vertical', pitch_color='#22312b', line_color='#c7d5cc',
    figsize=(20, 15))
    fig, ax = pitch.draw()
    sns.scatterplot(liverpool_shots['y'], liverpool_shots['x'], color='red', alpha=0.7,s=80,hue=liverpool_shots['shot_outcome'], data=liverpool_shots, ax=ax[0])
    sns.scatterplot(real_madrid_shots['y'], real_madrid_shots['x'], color='red',alpha=0.7,s=80,hue=real_madrid_shots['shot_outcome'], data=real_madrid_shots, ax=ax[1])
    ax[0].set_title("LiverPool", fontsize=50, fontfamily='serif')
    ax[1].set_title('Real Madrid', fontsize=50, fontfamily='serif')
    return fig
 
def get_RealM_shots(data):
    event = data[['team', 'type', 'minute', 'location', 'player', 'shot_aerial_won', 'shot_body_part', 'shot_end_location',
    'shot_first_time', 'shot_freeze_frame','shot_key_pass_id','shot_one_on_one','shot_outcome','shot_redirect','shot_statsbomb_xg','shot_technique','shot_type']]
    real_madrid_shots = event[(event['team'] == 'Real Madrid') & (event['type']=='Shot')].sort_values('minute').reset_index()
   # real_madrid_pass['pass_outcome'] = real_madrid_pass['pass_outcome'].fillna('Success')
    real_madrid_shots[['x','y']] = real_madrid_shots['location'].apply(pd.Series)
    return real_madrid_shots

def get_RMplayers_that_took_shots(real_madrid_shots):
    """This function returns a list of players that took shot in the game"""
    shots_players = real_madrid_shots.player.unique().tolist()
    return [name for name in shots_players]


def get_liverpool_shots(data):
    """This function returns all the shot events taken in the Real Madrid team"""
    shots = data[data['type'] =='Shot'][['team', 'player', 'location', 'shot_aerial_won', 'shot_body_part',
            'shot_end_location', 'shot_first_time', 'shot_freeze_frame','shot_key_pass_id', 'shot_one_on_one',
            'shot_outcome','shot_redirect', 'shot_statsbomb_xg', 'shot_technique', 'shot_type', 'minute']]
    liverpool_shots = shots[shots['team']=='Liverpool']
    liverpool_shots[['x','y']] = liverpool_shots['location'].apply(pd.Series)
    return liverpool_shots


def plot_XG_per_min(data):
    shots = data[data['type'] =='Shot'][['team', 'player','shot_outcome', 'shot_statsbomb_xg', 'minute']]
    av_xg = shots[['team', 'player', 'minute', 'shot_outcome', 'shot_statsbomb_xg']]
    av_xg.rename(columns={'shot_statsbomb_xg': 'XG'}, inplace=True)
    fig = px.line(av_xg, x="minute", y="XG", color='team', markers=True, 
              width=1200, height=600)
    return fig


def get_LVplayers_that_took_shots(liverpool_shots):
    """This function returns a list of players that took shot in the game"""
    shots_players = liverpool_shots.player.unique().tolist()
    return [name for name in shots_players]


def plot_liverpool_shots(liverpool_shots):
    pitch = Pitch(layout=(1,2), orientation='vertical', view='half', pitch_color='#22312b', line_color='#c7d5cc', figsize=(16, 11))
    fig, ax = pitch.draw()
    fig.set_facecolor('#22312b')
    sns.scatterplot(liverpool_shots['y'], liverpool_shots['x'], color='red', alpha=0.7,s=80,hue=liverpool_shots['shot_outcome'], data=liverpool_shots, ax=ax)

def plot_madrid_shots(real_madrid_shots):
    pitch = Pitch(orientation='vertical', view='half', pitch_color='#22312b', line_color='#c7d5cc', figsize=(16, 11))
    fig, ax = pitch.draw()
    fig.set_facecolor('#22312b')
    ax = sns.scatterplot(real_madrid_shots['y'], real_madrid_shots['x'], color='red', alpha=0.7,s=80,hue=real_madrid_shots['shot_outcome'], data=real_madrid_shots,ax=ax)
    return fig

#------- ------------------Heatmap-------------------------------------------------------------#
def get_player_location(data):
    """function that returns the location of players events"""
    player_location = data[['player', 'location', 'minute', 'timestamp', 'team']].dropna(subset=['player', 'location']).reset_index().sort_values('minute')
    return player_location

def get_all_player(player_location):
    """aggregateb all the players together in a list for their heatmap"""
    all_player = player_location.player.unique().tolist()
    return [player for player in all_player]
    
