#from markdown import markdown
import streamlit as st
from Modules.analyze import *
from Modules.sonalysis import *
from statsbombpy import sb
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer.pitch import Pitch
#from Modules import analyze as fx
#pd.set_option('display.max_columns', 100)

import warnings
warnings.filterwarnings('ignore')

st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_option('deprecation.showfileUploaderEncoding', False)

st.sidebar.title('Menu')
Choice = st.sidebar.selectbox(
    '', ['Home', 'Select a team to analyze their Passes stats', 
        'Analyze Both Teams Expected Goals', 
        'Analyze Expected Goals by Player',
        'Players Heatmap', 'Both Teams Expected Goals by Minutes Played',
        'Test with Sonalysis dataset'], index=0
)

# load dataset
dataset = fetch_data()  

if Choice == "Home":
    st.markdown("""<h1 style='text-align: center; white;font-size:60px;margin-top:-50x;'>SONALYSIS</h1><h1 style='text-align: center; color: white;font-size:30px;margin-top:-30px;'>Research Methods on Football Analytics Modelling<br></h1>""", unsafe_allow_html=True)


if Choice == "Select a team to analyze their Passes stats":
    #dataset = fetch_data()

    names = get_team_in_match(dataset)
    Team_name = st.sidebar.selectbox("Team Name", names, key='1')
    if Team_name == 'Liverpool':
        st.markdown("# Visualize each Player passing stats with their successive passes and failures")
        st.subheader("")
        Liverpool_pass = generate_liverpool_player_pass_stats(dataset)
        if st.sidebar.checkbox('View the Processed dataset I used for this Player Pass modelling', False):
            st.write(Liverpool_pass)
        players = get_player(Liverpool_pass)
        Player_Name = st.sidebar.selectbox('Player Name to Analyze', players, key='2')
        # #st.sidebar.selectbox('Name of Player to Analyze', )
        player_pass_data = Liverpool_pass[Liverpool_pass['player']== Player_Name]
        st.markdown('#### Analyze {} passes'.format(Player_Name))
        # display the pass plot
        fig, ax = plt.subplots(figsize=(12.5,8))
        fig.set_facecolor('#22312b')
        ax.patch.set_facecolor('#22312b')
        pitch = Pitch(pitch_type='statsbomb', orientation='horizontal', pitch_color='#22312b', line_color='#c7d5cc',
        figsize=(16, 11), constrained_layout=True, tight_layout=True)
        pitch.draw(ax=ax)
        plt.gca().invert_yaxis()
        player_pass = Liverpool_pass[(Liverpool_pass['player']== Player_Name) & (Liverpool_pass['minute'] < 91)].reset_index()
        for i in range(len(player_pass)):
            if player_pass['pass_outcome'][i] == 'Success':
                ax.plot((player_pass['x'][i],player_pass['end_x'][i]),(player_pass['y'][i],player_pass['end_y'][i]), color='green')
                ax.scatter(player_pass['x'][i], player_pass['y'][i],color='green')
            if (player_pass['pass_outcome'][i]=='Success') & (player_pass['pass_height'][i] =='High Pass'):
                ax.plot((player_pass['x'][i],player_pass['end_x'][i]),(player_pass['y'][i],player_pass['end_y'][i]),ls = '--',color='green')
                ax.scatter(player_pass['x'][i],player_pass['y'][i],color='green')
            if player_pass['pass_outcome'][i] == 'Incomplete':
                ax.plot((player_pass['x'][i],player_pass['end_x'][i]),(player_pass['y'][i],player_pass['end_y'][i]),color='red')
                ax.scatter(player_pass['x'][i],player_pass['y'][i],color ='red')
        st.pyplot(fig)

    if Team_name == 'Real Madrid':
        st.markdown("# Visualize each Player passing stats with their successive passes and failures")
        st.subheader("")
        Real_pass = generate_real_madrid_pass_stats(dataset)
        if st.sidebar.checkbox('View the dataset I processed for this Player Pass modelling', False):
            st.write(Real_pass)
        players = get_player(Real_pass)
        Player_Name = st.sidebar.selectbox('Player Name to Analyze', players, key='2')
        # #st.sidebar.selectbox('Name of Player to Analyze', )
        player_pass_data = Real_pass[Real_pass['player']== Player_Name]
        st.markdown('#### Analyze {} passes'.format(Player_Name))
        # display the pass plot
        fig, ax = plt.subplots(figsize=(12.5,8))
        fig.set_facecolor('#22312b')
        ax.patch.set_facecolor('#22312b')
        pitch = Pitch(pitch_type='statsbomb', orientation='horizontal', pitch_color='#22312b', line_color='#c7d5cc',
        figsize=(16, 11), constrained_layout=True, tight_layout=True)
        pitch.draw(ax=ax)
        plt.gca().invert_yaxis()
        player_pass = Real_pass[(Real_pass['player']== Player_Name) & (Real_pass['minute'] < 91)].reset_index()
        for i in range(len(player_pass)):
            if player_pass['pass_outcome'][i] == 'Success':
                ax.plot((player_pass['x'][i],player_pass['end_x'][i]),(player_pass['y'][i],player_pass['end_y'][i]), color='green')
                ax.scatter(player_pass['x'][i], player_pass['y'][i],color='green')
            if (player_pass['pass_outcome'][i]=='Success') & (player_pass['pass_height'][i] =='High Pass'):
                ax.plot((player_pass['x'][i],player_pass['end_x'][i]),(player_pass['y'][i],player_pass['end_y'][i]),ls = '--',color='green')
                ax.scatter(player_pass['x'][i],player_pass['y'][i],color='green')
            if player_pass['pass_outcome'][i] == 'Incomplete':
                ax.plot((player_pass['x'][i],player_pass['end_x'][i]),(player_pass['y'][i],player_pass['end_y'][i]),color='red')
                ax.scatter(player_pass['x'][i],player_pass['y'][i],color ='red')
        st.pyplot(fig)


elif Choice == "Analyze Both Teams Expected Goals":
    st.markdown('# Analyze Expected Goals by team')
   # shots_data = fetch_data()
    viz = get_both_teams_shots(dataset)
    st.pyplot(viz)


elif Choice == "Both Teams Expected Goals by Minutes Played":
    st.markdown('# Analyze Both Teams Expected Goal by Minutes played')  
    st.plotly_chart(plot_XG_per_min(dataset))

# ----------Heatmap------------------------------------------------------#   
elif Choice == "Players Heatmap":
    st.markdown("# View area positions controlled by players in the form of heatmap")
    st.subheader("")
    st.subheader("")
    Player_Loc = get_player_location(dataset)
    if st.sidebar.checkbox('View the dataset I processed for the Heatmap modelling', False):
        st.write(Player_Loc)
    players = get_all_player(Player_Loc)
    Players_Name = st.sidebar.selectbox('Player Name to Analyze their Location', players, key='3')
    player_select = Player_Loc[Player_Loc['player']== Players_Name]
    st.markdown('#### Analyze {} heatmap'.format(Players_Name))
    player_select[['x','y']] = player_select['location'].apply(pd.Series)
    
    # plot heatmap
    pitch = Pitch(orientation='vertical', pitch_color="#22312b", line_color='#c7d5cc', figsize=(16, 11))
    fig,ax = pitch.draw()
    fig.set_facecolor('#22312b')
    sns.kdeplot(player_select['x'], player_select['y'], cmap='coolwarm', shade=True,shade_lowest=False,alpha=0.7, thresh=0.4,levels=100,vertical=True,linewidth=0)
    plt.xlim(0,80)
    plt.ylim(0,120)
    st.pyplot(fig)
#---------------------------------------------------------------------------------------#
elif Choice == "Analyze Expected Goals by Player":
    st.markdown('# Analyze Players Shooting Stats')
    xp = st.sidebar.radio(label='Analyze expected goals by player', options=('','Real Madrid', 'Liverpool'))
    if xp == 'Real Madrid':
        # get madrid shots
        team_shots = get_RealM_shots(dataset)
        #st.write(team_shots)
        # get only the list of players that had shots in the game
        players_shot = get_RMplayers_that_took_shots(team_shots)
        Players_Name = st.sidebar.selectbox('Player Name to Analyze', players_shot, key='4')
        player_select = team_shots[team_shots['player']== Players_Name]
        st.markdown('#### Analyze {} shooting stats'.format(Players_Name))
        pitch = Pitch(orientation='vertical', pitch_color='#22312b', line_color='#c7d5cc',
        figsize=(16, 11))
        fig, ax = pitch.draw()
        sns.scatterplot(player_select['y'], player_select['x'], color='red', alpha=0.7,s=80,hue=team_shots['shot_outcome'], data=team_shots)      
        st.pyplot(fig)
    
    else:
        if xp == 'Liverpool':
            # get liverpool shots
            team_shots = get_liverpool_shots(dataset)
            liv_players_shot = get_LVplayers_that_took_shots(team_shots)
            Players_Name = st.sidebar.selectbox('Player Name to Analyze', liv_players_shot, key='5')
            player_select = team_shots[team_shots['player']== Players_Name]
            st.markdown('#### Analyze {} shooting stats'.format(Players_Name))
            pitch = Pitch(orientation='vertical', pitch_color='#22312b', line_color='#c7d5cc',
            figsize=(16, 11))
            fig, ax = pitch.draw()
            sns.scatterplot(player_select['y'], player_select['x'], color='red', alpha=0.7,s=80,hue=team_shots['shot_outcome'], data=team_shots)      
            st.pyplot(fig) 

#------------- Sonalysis real data --------------------------------------#
elif Choice == "Test with Sonalysis dataset":
    st.markdown('### Analyze Sonalysis Game')
    features = st.sidebar.radio(label='Select any feature to analyze', options=('','Both Team Expected Goals', 'Player Heatmap', 'Player Passes', 'Expected Goals by Player'))
    uploaded_file = st.file_uploader('upload your file here', type=['csv'])
    try:
        data = pd.read_csv(uploaded_file)
        #st.write(data)
    except ValueError as e:
        print(e)

    if uploaded_file is not None:
        if features == "Both Team Expected Goals":
               viz = get_sona_both_teams_shots(data)
               st.pyplot(viz)
    
################################# Passes #########################################
        if features == "Player Passes":
           names = get_team_in_match(data)
           Team_name = st.sidebar.selectbox("Team Name", names, key='6')
           if Team_name == 'fcb':
                st.markdown("# Visualize each Player passing stats with their successive passes and failures")
                st.subheader("")
                Barca_pass = generate_barca_player_pass_stats(data)
                # if st.sidebar.checkbox('View the Processed dataset I used for this Player Pass modelling', False):
                #   st.write(Barca_pass)
                players = get_sona_player(Barca_pass)
                Player_Name = st.sidebar.selectbox('Player Name to Analyze', players, key='7')
                # #st.sidebar.selectbox('Name of Player to Analyze', )
                player_pass_data = Barca_pass[Barca_pass['players']== Player_Name]
                st.markdown('#### Analyze {} passes'.format(Player_Name))
                # display the pass plot
                fig, ax = plt.subplots(figsize=(12.5,8))
                fig.set_facecolor('#22312b')
                ax.patch.set_facecolor('#22312b')
                pitch = Pitch(pitch_type='statsbomb', orientation='horizontal', pitch_color='#22312b', line_color='#c7d5cc',
                figsize=(16, 11), constrained_layout=True, tight_layout=True)
                pitch.draw(ax=ax)
                plt.gca().invert_yaxis()
                player_pass = Barca_pass[(Barca_pass['players']== Player_Name)].reset_index()
    
                for i in range(len(player_pass)):
                    if player_pass['pass_outcome'][i] == 'Success':
                        ax.plot((player_pass['x'][i],player_pass['end_x'][i]),(player_pass['y'][i],player_pass['end_y'][i]), color='green')
                        ax.scatter(player_pass['x'][i], player_pass['y'][i],color='green')
                    # if (player_pass['pass_outcome'][i]=='Success') & (player_pass['pass_height'][i] =='High Pass'):
                    #     ax.plot((player_pass['x'][i],player_pass['end_x'][i]),(player_pass['y'][i],player_pass['end_y'][i]),ls = '--',color='green')
                    #     ax.scatter(player_pass['x'][i],player_pass['y'][i],color='green')
                    if player_pass['pass_outcome'][i] == 'Incomplete':
                        ax.plot((player_pass['x'][i],player_pass['end_x'][i]),(player_pass['y'][i],player_pass['end_y'][i]),color='red')
                        ax.scatter(player_pass['x'][i],player_pass['y'][i],color ='red')
                st.pyplot(fig)


           elif Team_name == "rma":
                st.markdown("# Visualize each Player passing stats with their successive passes and failures")
                st.subheader("")
                Real_pass = generate_realMadrid_player_pass_stats(data)
                # if st.sidebar.checkbox('View the dataset I processed for this Player Pass modelling', False):
                #     st.write(Real_pass)
                players = get_sona_player(Real_pass)
                Player_Name = st.sidebar.selectbox('Player Name to Analyze', players, key='2')
                # #st.sidebar.selectbox('Name of Player to Analyze', )
                player_pass_data = Real_pass[Real_pass['players']== Player_Name]
                st.markdown('#### Analyze {} passes'.format(Player_Name))
                # display the pass plot
                fig, ax = plt.subplots(figsize=(12.5,8))
                fig.set_facecolor('#22312b')
                ax.patch.set_facecolor('#22312b')
                pitch = Pitch(pitch_type='statsbomb', orientation='horizontal', pitch_color='#22312b', line_color='#c7d5cc',
                figsize=(16, 11), constrained_layout=True, tight_layout=True)
                pitch.draw(ax=ax)
                plt.gca().invert_yaxis()
                player_pass = Real_pass[(Real_pass['players']== Player_Name)].reset_index()
                #st.write(player_pass)
                for i in range(len(player_pass)):
                    if player_pass['pass_outcome'][i] == 'Success':
                        ax.plot((player_pass['x'][i],player_pass['end_x'][i]),(player_pass['y'][i],player_pass['end_y'][i]), color='green')
                        ax.scatter(player_pass['x'][i], player_pass['y'][i],color='green')
                    # if (player_pass['pass_outcome'][i]=='Success') & (player_pass['pass_height'][i] =='High Pass'):
                    #     ax.plot((player_pass['x'][i],player_pass['end_x'][i]),(player_pass['y'][i],player_pass['end_y'][i]),ls = '--',color='green')
                    #     ax.scatter(player_pass['x'][i],player_pass['y'][i],color='green')
                    if player_pass['pass_outcome'][i] == 'Incomplete':
                        ax.plot((player_pass['x'][i],player_pass['end_x'][i]),(player_pass['y'][i],player_pass['end_y'][i]),color='red')
                        ax.scatter(player_pass['x'][i],player_pass['y'][i],color ='red')
                st.pyplot(fig)




        if features == "Player Heatmap":
            st.markdown("# View area positions controlled by players in the form of heatmap")
            st.subheader("")
            st.subheader("")
            Player_Loc = get_sonaplayer_location(data)
            #st.write(Player_Loc)
            # if st.sidebar.checkbox('View the dataset I processed for the Heatmap modelling', False):
            #     st.write(Player_Loc)
            players = get_all_sona_player(Player_Loc)
            Players_Name = st.sidebar.selectbox('Player Name to Analyze their Location', players, key='9')
            player_select = Player_Loc[Player_Loc['players']== Players_Name]
            st.markdown('#### Analyze {} heatmap'.format(Players_Name))
           # player_select[['x','y']] = player_select['location'].apply(pd.Series)
            
            # plot heatmap
            pitch = Pitch(orientation='vertical', pitch_color="#22312b", line_color='#c7d5cc', figsize=(16, 11))
            fig,ax = pitch.draw()
            fig.set_facecolor('#22312b')
            sns.kdeplot(player_select['x'], player_select['y'], cmap='coolwarm', shade=True,shade_lowest=False,alpha=0.7, thresh=0.4,levels=100,vertical=True,linewidth=0)
            plt.xlim(0,80)
            plt.ylim(0,120)
            st.pyplot(fig)

        if features == "Expected Goals by Player":
            name = get_team_in_match(data)
            Team_name = st.sidebar.selectbox('Select a team',name, key='10')
            if Team_name == "rma": 
              # get madrid shots
                team_shots = get_rma_shots(data)
                #st.write(team_shots)
                # get only the list of players that had shots in the game
                players_shot = get_rma_players_that_took_shots(team_shots)
                Players_Name = st.sidebar.selectbox('Player Name to Analyze', players_shot, key='4')
                player_select = team_shots[team_shots['players']== Players_Name]
                st.markdown('#### Analyze {} shooting stats'.format(Players_Name))
                pitch = Pitch(orientation='vertical', pitch_color='#22312b', line_color='#c7d5cc',
                figsize=(16, 11))
                fig, ax = pitch.draw()
                sns.scatterplot(player_select['y'], player_select['x'], color='red', alpha=0.7,s=80,hue=team_shots['shot_outcome'], data=team_shots)      
                st.pyplot(fig)
            
            else:
                team_shots = get_fcb_shots(data)
                Fcb_shot = get_fcb_players_that_took_shots(team_shots)
                Players_Name = st.sidebar.selectbox('Player Name to Analyze', Fcb_shot, key='12')
                player_select = team_shots[team_shots['players']== Players_Name]
                st.markdown('#### Analyze {} shooting stats'.format(Players_Name))
                pitch = Pitch(orientation='vertical', pitch_color='#22312b', line_color='#c7d5cc',
                figsize=(16, 11))
                fig, ax = pitch.draw()
                sns.scatterplot(player_select['y'], player_select['x'], color='red', alpha=0.7,s=80,hue=team_shots['shot_outcome'], data=team_shots)      
                st.pyplot(fig) 


