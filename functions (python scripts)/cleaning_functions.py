## CLEANING DATAFRAME TO GAME DATA FUNCTION
def clean_df_to_games(df):
    team_stats = df.loc[df['TEAM_STATS_OR_NOT'] == 1].copy() # GETTING JUST THE TOTAL TEAM BOX SCORE STATS
    team_stats.drop(columns=['TEAM', 'TIME', 'DATE+TIME', 'B_+/-', 'USG_PCT', '+/-', 'TEAM_STATS_OR_NOT'], inplace=True) #DROPING IRRELEVANT COLUMNS FOR LATER IN THE SCRAPE
    home = team_stats.loc[team_stats['HOME'] == 1] # GETTING THE HOME DATAFRAME
    away = team_stats.loc[team_stats['HOME'] == 0] # GETTING THE AWAY DATAFRAME
    games = pd.merge(home,away, how='outer', on='GAMEID').copy() # MERGING THE TWO AND CREATING A DATAFRAME COPY
    new_col_names = []
    for n in games.columns: # FOR LOOP MEANT TO LABEL WHICH COLUMN IS HOME AND WHICH IS AWAY
        if '_x' in n:
            n = n.replace('_x','_HOME')
            new_col_names.append(n)
        elif '_y' in n:
            n = n.replace('_y','_AWAY')
            new_col_names.append(n)
        else:
            new_col_names.append(n)
    new_col_names
    games.columns = new_col_names # INSERTING THE COLUMN LABELS
    games['PLAYER_HOME'] = games['PLAYER_HOME'].map(lambda x:x[13:16]) # GETTING JUST THE TEAM NAMES
    games['PLAYER_AWAY'] = games['PLAYER_AWAY'].map(lambda x:x[13:16])
    games.rename(columns={'PLAYER_HOME':'TEAM_HOME','PLAYER_AWAY':'TEAM_AWAY','DATE_HOME':'DATE'}, inplace=True)
    games['TEAM_AWAY'] = ['CHA' if i == 'CHO' else i for i in games['TEAM_AWAY']] # REPLACING 'CHO' WITH 'CHA' SINCE THEY ARE THE SAME TEAM, JUST UNDERWENT A NAME-CHANGE
    games['TEAM_HOME'] = ['CHA' if i == 'CHO' else i for i in games['TEAM_HOME']]
    games['DATE'] = pd.to_datetime(games['DATE']) # TURNING THE DATE COLUMN INTO DATETIME DATA TYPE
    games.drop(columns = ['OPPONENT_AWAY', 'OPPONENT_HOME', 'SEASON_AWAY'], inplace=True) # DROPPING UNNECCESSARY OPPONENT COLUMNS
    games['OTs'] = games['MP_HOME'].map(lambda x:int((x-240)/25)) # MAKING OT'S COLUMN FROM MP_HOME
    games.drop(columns = ['MP_HOME', 'MP_AWAY'], inplace=True) # DROPPING IRRELEVANT MP HOME COLUMNS
    games.drop(columns=['HOME_HOME','HOME_AWAY','AWAY_HOME','AWAY_AWAY'], inplace=True) # DROPPING ADDITIONAL USELESS COLUMNS PREVIOUSLY INDICATING HOME AND AWAY
    games.rename(columns={'SEASON_HOME':'SEASON'}, inplace=True) # RENAMING THE SEASON_HOME COLUMN JUST SEASON
    games.drop('DATE_AWAY', axis=1,inplace=True) # DROPPING SECOND DATE COLUMN
    games['FG(3)_MISSED_HOME'] = games['FGA(3)_HOME'] - games['FG(3)_HOME'] # MAKING NEW FG(3) MISSED FEATURE
    games['FG(3)_MISSED_AWAY'] = games['FGA(3)_AWAY'] - games['FG(3)_AWAY'] 
    games['FG_MISSED_HOME'] = games['FGA_HOME'] - games['FG_HOME'] # MAKING NEW FG MISSED FEATURE
    games['FG_MISSED_AWAY'] = games['FGA_AWAY'] - games['FG_AWAY']
    games['BLOCKED_ATTEMPTS_HOME'] = games['BLK_AWAY'] # MAKING NEW BLOCKED ATTEMPTS FEATURE
    games['BLOCKED_ATTEMPTS_AWAY'] = games['BLK_HOME']
    games['TOV_FORCED_HOME'] = games['TOV_AWAY'] # MAKING NEW TURNOVERS FORCED FEATURE
    games['TOV_FORCED_AWAY'] = games['TOV_HOME']
    games['FG(2)_HOME'] = games['FG_HOME']-games['FG(3)_HOME'] # MAKING NEW FG(2) MAKES FEATURE
    games['FG(2)_AWAY'] = games['FG_AWAY']-games['FG(3)_AWAY']
    games['FGA(2)_HOME'] = games['FGA_HOME']-games['FGA(3)_HOME'] # MAKING NEW FG(2) ATTEMPTS FEATURE
    games['FGA(2)_AWAY'] = games['FGA_AWAY']-games['FGA(3)_AWAY']
    games['FG(2)_MISSED_HOME'] = games['FG_MISSED_HOME']-games['FG(3)_MISSED_HOME'] # MAKING NEW FG(2) MISSED FEATURE
    games['FG(2)_MISSED_AWAY'] = games['FG_MISSED_AWAY']-games['FG(3)_MISSED_AWAY']
    games.rename(columns={'WINS_AWAY':'WINS_RECORD_AWAY', 'LOSSES_AWAY':'LOSSES_RECORD_AWAY', 'WINS_HOME':'WINS_RECORD_HOME',
                           'LOSSES_HOME':'LOSSES_RECORD_HOME'}, inplace=True) # RENAMING TOTAL WINS AND TOTAL LOSSES COLUMNS FOR CLARITY
    team_cols = []
    for col in games.columns: # GETTING COLUMN NAMES WITHOUT HOME AWAY LABELS
        if '_HOME' in col:
            col = col.replace('_HOME', '') # GETTING  COLUMN NAMES
            team_cols.append(col)
    gen_cols = []
    for col in games.columns:
        if '_HOME' not in col:
            if '_AWAY' not in col:
                gen_cols.append(col) # GETTING THE GENERAL COLUMNS WITHOUT AWAY OR HOME
    team_cols_each = [] # GETTING BOTH HOME AWAY COLUMNS IN THE SAME LIST
    for col in team_cols:
        home = col+'_HOME'
        away = col+'_AWAY'
        team_cols_each.append(home)
        team_cols_each.append(away)
    games = games[team_cols_each+gen_cols]
    return games

def clean_to_player(df):
    games = clean_df_to_games(df)
    players = df.loc[df['TEAM_STATS_OR_NOT'] == 0].copy()
    players.fillna(0)
    players['FG(3)_MISSED'] = players['FGA(3)'] - players['FG(3)']
    players['FG_MISSED'] = players['FGA'] - players['FG']
    players['FG(2)'] = players['FG']-players['FG(3)']
    players['FGA(2)'] = players['FGA']-players['FGA(3)']
    players['FG(2)_MISSED'] = players['FG_MISSED']-players['FG(3)_MISSED']
    players.drop(columns=['TIME', 'DATE+TIME', 'TEAM_STATS_OR_NOT'], inplace=True)
    ots = games[['GAMEID','OTs']]
    players = pd.merge(players,ots, how='inner', on='GAMEID').copy()
    gen_cols = ['OTs','GAMEID', 'SEASON']
    stat_cols = []
    for col in players.columns:
        if col not in gen_cols:
            stat_cols.append(col)
    players = players[stat_cols + gen_cols].copy()
    return players