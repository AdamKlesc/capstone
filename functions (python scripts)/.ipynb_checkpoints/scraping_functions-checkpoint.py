import pandas as pd
from requests import get
import requests
from bs4 import BeautifulSoup
import time

# SCRAPING BOX SCORES FUNCTION
def get_box_scores(date, team1, team2):
    teams = [team1,team2]
    url = f"https://www.basketball-reference.com/boxscores/{str(date)}0{team1}.html"
    res = requests.get(url)
    if res.status_code != 200:
        print('UNABLE TO GET REQUESTS')
    soup = BeautifulSoup(res.content, 'lxml')
    dfs = []
    for team in teams:
        table = soup.find('table', {'id':f"box-{team}-game-basic"})
        body = table.find('tbody').find_all('tr')
        foot = table.find('tfoot').find_all('tr')
        label = soup.find('div', {'id':f"box-{team}-game-basic_sh"})
        h2 = (label.find('h2').text).split(' ')
        record = h2[(len(h2)-1)].lstrip('(').rstrip(')')
        wins_and_losses = record.split('-')
        wins = int(wins_and_losses[0])
        losses = int(wins_and_losses[1])
        box_score_rows = []
        for tr in body:
            try:
                tr.find()
                row = {}
                #print(tr)
                try:
                    row['PLAYER'] = tr.find('th', {'data-stat':'player'}).attrs['csk']                
                    row['MP'] = int(tr.find('td', {'data-stat':'mp'}).attrs['csk'])/60
                    row['FG'] = tr.find('td', {'data-stat':'fg'}).text
                    row['FGA'] = tr.find('td', {'data-stat':'fga'}).text
                    row['FG_PCT'] = tr.find('td', {'data-stat':'fg_pct'}).text
                    row['FG(3)'] = tr.find('td', {'data-stat':'fg3'}).text
                    row['FGA(3)'] = tr.find('td', {'data-stat':'fg3a'}).text
                    row['FG_PCT(3)'] = tr.find('td', {'data-stat':'fg3_pct'}).text
                    row['FT'] = tr.find('td', {'data-stat':'ft'}).text
                    row['FTA'] = tr.find('td', {'data-stat':'fta'}).text
                    row['FT_PCT'] = tr.find('td', {'data-stat':'ft_pct'}).text
                    row['ORB'] = tr.find('td', {'data-stat':'orb'}).text
                    row['DRB'] = tr.find('td', {'data-stat':'drb'}).text
                    row['TRB'] = tr.find('td', {'data-stat':'trb'}).text
                    row['AST'] = tr.find('td', {'data-stat':'ast'}).text
                    row['STL'] = tr.find('td', {'data-stat':'stl'}).text
                    row['BLK'] = tr.find('td', {'data-stat':'blk'}).text
                    row['TOV'] = tr.find('td', {'data-stat':'tov'}).text
                    row['PF'] = tr.find('td', {'data-stat':'pf'}).text
                    row['PTS'] = tr.find('td', {'data-stat':'pts'}).text
                    row['+/-'] = tr.find('td', {'data-stat':'plus_minus'}).text
                except AttributeError:
                    pass
                box_score_rows.append(row)  
            except KeyError:
                pass

            
        #print(label)
        for tr in foot:
            row={}
            row['PLAYER'] = tr.find('th', {'data-stat':'player'}).text + f', {team}'
            row['MP'] = tr.find('td', {'data-stat':'mp'}).text
            row['FG'] = tr.find('td', {'data-stat':'fg'}).text
            row['FGA'] = tr.find('td', {'data-stat':'fga'}).text
            row['FG_PCT'] = tr.find('td', {'data-stat':'fg_pct'}).text
            row['FG(3)'] = tr.find('td', {'data-stat':'fg3'}).text
            row['FGA(3)'] = tr.find('td', {'data-stat':'fg3a'}).text
            row['FG_PCT(3)'] = tr.find('td', {'data-stat':'fg3_pct'}).text
            row['FT'] = tr.find('td', {'data-stat':'ft'}).text
            row['FTA'] = tr.find('td', {'data-stat':'fta'}).text
            row['FT_PCT'] = tr.find('td', {'data-stat':'ft_pct'}).text
            row['ORB'] = tr.find('td', {'data-stat':'orb'}).text
            row['DRB'] = tr.find('td', {'data-stat':'drb'}).text
            row['TRB'] = tr.find('td', {'data-stat':'trb'}).text
            row['AST'] = tr.find('td', {'data-stat':'ast'}).text
            row['STL'] = tr.find('td', {'data-stat':'stl'}).text
            row['BLK'] = tr.find('td', {'data-stat':'blk'}).text
            row['TOV'] = tr.find('td', {'data-stat':'tov'}).text
            row['PF'] = tr.find('td', {'data-stat':'pf'}).text
            row['PTS'] = tr.find('td', {'data-stat':'pts'}).text
            row['+/-'] = tr.find('td', {'data-stat':'plus_minus'}).text
            box_score_rows.append(row)

        box_df = pd.DataFrame(box_score_rows)
        
        advtable = soup.find('table', {'id':f"box-{team}-game-advanced"})
        advbody = advtable.find('tbody').find_all('tr')
        advfoot = advtable.find('tfoot').find_all('tr')
        adv_score_rows = []
        for tr in advbody:
            try:
                tr.find()
                row = {}
                #print(tr)
                try:
                    row['PLAYER'] = tr.find('th', {'data-stat':'player'}).attrs['csk']
                    row['MP'] = int(tr.find('td', {'data-stat':'mp'}).attrs['csk'])/60
                    row['TS_PCT'] = tr.find('td', {'data-stat':'ts_pct'}).text
                    row['EFG_PCT'] = tr.find('td', {'data-stat':'efg_pct'}).text
                    row['3PA_R'] = tr.find('td', {'data-stat':'fg3a_per_fga_pct'}).text
                    row['FT_R'] = tr.find('td', {'data-stat':'fta_per_fga_pct'}).text
                    row['ORB_PCT'] = tr.find('td', {'data-stat':'orb_pct'}).text
                    row['DRB_PCT'] = tr.find('td', {'data-stat':'drb_pct'}).text
                    row['TRB_PCT'] = tr.find('td', {'data-stat':'trb_pct'}).text
                    row['AST_PCT'] = tr.find('td', {'data-stat':'ast_pct'}).text
                    row['STL_PCT'] = tr.find('td', {'data-stat':'stl_pct'}).text
                    row['BLK_PCT'] = tr.find('td', {'data-stat':'blk_pct'}).text
                    row['TOV_PCT'] = tr.find('td', {'data-stat':'tov_pct'}).text
                    row['USG_PCT'] = tr.find('td', {'data-stat':'usg_pct'}).text
                    row['O_RTG'] = tr.find('td', {'data-stat':'off_rtg'}).text
                    row['D_RTG'] = tr.find('td', {'data-stat':'def_rtg'}).text
                    row['B_+/-'] = tr.find('td', {'data-stat':'bpm'}).text
                    row['GAMEID'] = f'{str(date)}0{team1}'
                    row['TEAM'] = team
                    if team == team1:
                        row['HOME'] = 1
                        row['AWAY'] = 0
                        row['OPPONENT'] = team2
                    elif team == team2:
                        row['HOME'] = 0
                        row['AWAY'] = 1
                        row['OPPONENT'] = team1
                    row['DATE'] = date
                    row['WINS'] = wins
                    row['LOSSES'] = losses
                    row['WIN_PCT'] = wins/(losses+wins)
                    row['GAME_NO'] = losses+wins
                except AttributeError:
                    pass
                adv_score_rows.append(row)  
            except KeyError:
                pass
        for tr in advfoot:
            row = {}
            row['PLAYER'] = tr.find('th', {'data-stat':'player'}).text + f', {team}'
            row['MP'] = tr.find('td', {'data-stat':'mp'}).text
            row['TS_PCT'] = tr.find('td', {'data-stat':'ts_pct'}).text
            row['EFG_PCT'] = tr.find('td', {'data-stat':'efg_pct'}).text
            row['3PA_R'] = tr.find('td', {'data-stat':'fg3a_per_fga_pct'}).text
            row['FT_R'] = tr.find('td', {'data-stat':'fta_per_fga_pct'}).text
            row['ORB_PCT'] = tr.find('td', {'data-stat':'orb_pct'}).text
            row['DRB_PCT'] = tr.find('td', {'data-stat':'drb_pct'}).text
            row['TRB_PCT'] = tr.find('td', {'data-stat':'trb_pct'}).text
            row['AST_PCT'] = tr.find('td', {'data-stat':'ast_pct'}).text
            row['STL_PCT'] = tr.find('td', {'data-stat':'stl_pct'}).text
            row['BLK_PCT'] = tr.find('td', {'data-stat':'blk_pct'}).text
            row['TOV_PCT'] = tr.find('td', {'data-stat':'tov_pct'}).text
            row['USG_PCT'] = tr.find('td', {'data-stat':'usg_pct'}).text
            row['O_RTG'] = tr.find('td', {'data-stat':'off_rtg'}).text
            row['D_RTG'] = tr.find('td', {'data-stat':'def_rtg'}).text
            row['B_+/-'] = tr.find('td', {'data-stat':'bpm'}).text
            row['GAMEID'] = f'{str(date)}0{team1}'
            row['TEAM'] = team
            if team == team1:
                row['HOME'] = 1
                row['AWAY'] = 0
                row['OPPONENT'] = team2
            elif team == team2:
                row['HOME'] = 0
                row['AWAY'] = 1
                row['OPPONENT'] = team1
            row['DATE'] = date
            row['WINS'] = wins
            row['LOSSES'] = losses
            row['WIN_PCT'] = wins/(losses+wins)
            row['GAME_NO'] = losses+wins
            adv_score_rows.append(row)  
    
        adv_df = pd.DataFrame(adv_score_rows)
    
        df = pd.merge(box_df, adv_df, how='left')
        for k,v in dict(df['MP'].isna()).items():
            if v == True:
                df.drop(k, inplace=True)
    
        dfs.append(df)
    df = pd.concat(dfs)
    
    return df

# SCRAPING SCHEDULE DATA FUNCTION
def get_games(year):
    url = f'https://www.basketball-reference.com/leagues/NBA_{year}_games.html'
    res = requests.get(url)
    if res.status_code != 200:
        print('UNABLE TO GET REQUESTS')
    soup = BeautifulSoup(res.content, 'lxml')
    filt = soup.find('div', {'class':'filter'})
    header1 = soup.find('h1', {'itemprop':'name'})
    spans = header1.find_all('span')
    season = spans[0].text
    anchors = filt.find_all('a')
    months = [(anchor.text).lower() for anchor in anchors]
    time.sleep(10)
    full_schedule = []
    in_playoffs = False
    for month in months:
        url = f'https://www.basketball-reference.com/leagues/NBA_{year}_games-{month}.html'
        res = requests.get(url)
        if res.status_code != 200:
            print('UNABLE TO GET REQUESTS')
        soup = BeautifulSoup(res.content, 'lxml')
        table = soup.find('table', {'id':'schedule'})
        body = table.find('tbody').find_all('tr')
        if in_playoffs == True:
            continue
        for tr in body:
            try:
                playoff_header = tr.find('th',{'colspan':10}).text
                if playoff_header == 'Playoffs':
                    in_playoffs = True
                    break
            except AttributeError:
                try:
                    row = {}
                    row['DATE'] = (tr.find('th', {'data-stat':'date_game'}).attrs['csk'])[0:8]
                    row['START_TIME'] = tr.find('td', {'data-stat':'game_start_time'}).text
                    row['HOME_TEAM'] = (tr.find('td', {'data-stat':'home_team_name'}).attrs['csk'])[0:3]
                    row['HOME_PTS'] = tr.find('td', {'data-stat':'home_pts'}).text
                    row['AWAY_TEAM'] = (tr.find('td', {'data-stat':'visitor_team_name'}).attrs['csk'])[0:3]
                    row['AWAY_PTS'] = tr.find('td', {'data-stat':'visitor_pts'}).text
                    row['OTs'] = tr.find('td', {'data-stat':'overtimes'}).text
                    row['ATTENDANCE'] = tr.find('td', {'data-stat':'attendance'}).text
                    row['HOME_WIN'] = 1 if row['HOME_PTS'] > row['AWAY_PTS'] else 0
                    row['AWAY_WIN'] = 0 if row['HOME_PTS'] > row['AWAY_PTS'] else 1
                    full_schedule.append(row)
                except AttributeError:
                    pass        
        
        time.sleep(10)
    
    df = pd.DataFrame(full_schedule)
    df['SEASON'] = year
    return df

# MASS SCRAPE BOX SCORES
def get_full_box(years):
    box_scores = []
    for year in years:
        schedule = get_games(year)
        for index_sched,v in schedule.iterrows():
            date = v['DATE']
            start_time = v['START_TIME']
            team1 = v['HOME_TEAM']
            team2 = v['AWAY_TEAM']
            team1result = v['HOME_WIN']
            team2result = v['AWAY_WIN']
            df = get_box_scores(date,team1,team2)
            df['TIME'] = start_time
            df['DATE'] = df['DATE'].map(lambda x:str(x)[:4]+'-'+str(x)[4:6]+'-'+str(x)[6:8])
            df['DATE+TIME'] = df['DATE'] + ' ' + df['TIME']
            df['DATE+TIME'] = pd.to_datetime(df['DATE+TIME'])
            df['WIN'] = df['TEAM'].map(lambda x:team1result if x == team1 else team2result)
            df['LOSS'] = df['WIN'].map(lambda x:0 if x == 1 else 1)
            df['TEAM_STATS_OR_NOT'] = df['PLAYER'].map(lambda x:1 if x[0:11] == 'Team Totals' else 0)
            df['SEASON'] = year
            box_scores.append(df)
            time.sleep(10)
    print(year)
    return box_scores

