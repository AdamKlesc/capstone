## GET PREVIOUS N GAMES AVERAGE STATS FUNCTION
def get_avg_stats_last_n_games(year,team,date,n):
    away_cols = []
    home_cols = []
    for col in df.columns:
        if '_AWAY' in col:
            away_cols.append(col)
        if '_HOME' in col:
            home_cols.append(col)
    df_year = df.loc[df['SEASON'] == year].copy()
    df_year_date = df_year.loc[(df_year['TEAM_HOME'] == team) | (df_year['TEAM_AWAY'] == team)].loc[df_year['DATE'] < date].copy()
    df_year_date.reset_index(inplace=True)
    df_year_date.drop('index',axis=1,inplace=True)
    final_ten = df_year_date.tail(n).copy()
    home = final_ten[final_ten['TEAM_HOME'] == team]
    away = final_ten[final_ten['TEAM_AWAY'] == team]
    home = home[home_cols].copy()
    away = away[away_cols].copy()
    home_wins = home['WIN_HOME'].sum()
    away_wins = away['WIN_AWAY'].sum()
    home_games = home_wins + (home['LOSS_HOME'].sum())
    away_games = away_wins + (away['LOSS_AWAY'].sum())
    home_win_pct = home['WIN_HOME'].mean()
    away_win_pct = away['WIN_AWAY'].mean()
    home.columns = [x.replace('_HOME', '') for x in home.columns]
    away.columns = [x.replace('_AWAY','') for x in away.columns]
    total = pd.concat([home,away])
    last = total.tail(1)
    elo = list(last['TEAM_ELO_AFTER'])[0]
    wins_amount = list(last['WINS_RECORD'])[0]
    losses_amount = list(last['LOSSES_RECORD'])[0]
    last_home = home.tail(1)
    home_wins_amount = list(last_home['H_TEAM_WINS_AT'])[0]
    home_losses_amount = list(last_home['H_TEAM_LOSSES_AT'])[0]
    last_away = total.tail(1)
    away_wins_amount = list(last_away['A_TEAM_WINS_AT'])[0]
    away_losses_amount = list(last_away['A_TEAM_LOSSES_AT'])[0]
    total.drop(columns=['TEAM', 'LOSS', 'WINS_RECORD', 'LOSSES_RECORD', 'GAME_NO', 'WIN_PCT','H_TEAM_WINS_AT', 'H_TEAM_LOSSES_AT',
       'HOME_GAMES_TEAM', 'HOME_GAME_WIN_RATE', 'A_TEAM_WINS_AT','A_TEAM_LOSSES_AT', 'AWAY_GAMES_TEAM', 'AWAY_GAME_WIN_RATE','TEAM_ELO_BEFORE','TEAM_ELO_AFTER', 'ODDS', 'PROBS'], inplace=True)
    total.rename(columns={'WIN':'WIN_PCT'}, inplace=True)
    total.columns = [x+f'_LAST_{n}_GAMES' for x in total.columns]
    total = total.mean()
    total[f'WINS_LAST_{n}_GAMES'] = total[f'WIN_PCT_LAST_{n}_GAMES'] * n
    total[f'LOSSES_LAST_{n}_GAMES'] = n - total[f'WINS_LAST_{n}_GAMES']
    total[f'HOME_WINS_LAST_{n}_GAMES'] = home_wins
    total[f'AWAY_WINS_LAST_{n}_GAMES'] = away_wins
    total[f'HOME_GAMES_IN_LAST_{n}_GAMES'] = home_games
    total[f'AWAY_GAMES_IN_LAST_{n}_GAMES'] = away_games
    total[f'HOME_WIN_PCT_IN_LAST_{n}_GAMES'] = home_win_pct
    total[f'AWAY_WIN_PCT_IN_LAST_{n}_GAMES'] = away_win_pct
    total['CURRENT_TOTAL_WINS'] = wins_amount
    total['CURRENT_TOTAL_LOSSES'] = losses_amount
    total['CURRENT_TOTAL_AWAY_WINS'] = away_wins_amount
    total['CURRENT_TOTAL_AWAY_LOSSES'] = away_losses_amount
    total['CURRENT_TOTAL_HOME_WINS'] = home_wins_amount
    total['CURRENT_TOTAL_HOME_LOSSES'] = home_losses_amount
    total['ELO'] = elo 
    total['TEAM'] = team
    return total




# FOLLOWING FUNCTIONS MADE BY JOSH WEINER

#Home and road team win probabilities implied by Elo ratings and home court adjustment
def win_probs(home_elo, away_elo, home_court_advantage) :
    h = math.pow(10, home_elo/400)
    r = math.pow(10, away_elo/400)
    a = math.pow(10, home_court_advantage/400) 

    denom = r + a*h
    home_prob = a*h / denom
    away_prob = r / denom 

    return home_prob, away_prob

    #odds the home team will win based on elo ratings and home court advantage

def home_odds_on(home_elo, away_elo, home_court_advantage) :
    h = math.pow(10, home_elo/400)
    r = math.pow(10, away_elo/400)
    a = math.pow(10, home_court_advantage/400)
    return a*h/r

    #this function determines the constant used in the elo rating, based on margin of victory and difference in elo ratings
def elo_k(MOV, elo_diff):
    k = 20
    if MOV>0:
        multiplier=(MOV+3)**(0.8)/(7.5+0.006*(elo_diff))
    else:
        multiplier=(-MOV+3)**(0.8)/(7.5+0.006*(-elo_diff))
    return k*multiplier


    #updates the home and away teams elo ratings after a game 

def update_elo(home_score, away_score, home_elo, away_elo, home_court_advantage) :
    home_prob, away_prob = win_probs(home_elo, away_elo, home_court_advantage) 

    if (home_score - away_score > 0) :
        home_win = 1 
        away_win = 0 
    else :
        home_win = 0 
        away_win = 1 

    k = elo_k(home_score - away_score, home_elo - away_elo)

    updated_home_elo = home_elo + k * (home_win - home_prob) 
    updated_away_elo = away_elo + k * (away_win - away_prob)

    return updated_home_elo, updated_away_elo


    #takes into account prev season elo
def get_prev_elo(team, date, season, df, elo_df) :
    prev_game = df[df['DATE'] < game_date][(df['TEAM_HOME'] == team) | (df['TEAM_AWAY'] == team)].sort_values(by = 'DATE').tail(1).iloc[0] 

    if team == prev_game['TEAM_HOME'] :
        elo_rating = elo_df[elo_df['GAMEID'] == prev_game['GAMEID']]['TEAM_ELO_AFTER_HOME'].values[0]
    else :
        elo_rating = elo_df[elo_df['GAMEID'] == prev_game['GAMEID']]['TEAM_ELO_AFTER_AWAY'].values[0]

    if prev_game['SEASON'] != season :
        return (0.75 * elo_rating) + (0.25 * 1505)
    else :
        return elo_rating