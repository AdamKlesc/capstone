# ![](https://ga-dash.s3.amazonaws.com/production/assets/logo-9f88ae6c9c3871690e33280fcf557f33.png) Project 6: Predicting NBA Games

## Problem Statement

Can I predict the results of NBA games from the back-half of a season from the opening half of the season?

Most NBA ML predictors use a plethora of data to predict on a limited test set, I wanted to see if I could create a predictor that could eclipse the baseline and reach an r2 score of 60+ percent.

Most NBA ML predictors use a variation of ELO rankings to judge team performance, I want to include that in my data as well and judge it's correlation with team performance both offensively and defensively.

### Project Goal:

1. Create a model that successfully predicts NBA games above 0.6 r2 score when given a variety of statistical features. 

2. From the data and these models, what differences can we infer between the first-half of a given NBA season and the second-half?

3. Find out the effects of ELO on NBA statistical performance

4. Attach an ELO column to the dataframe

### Project Hypothesis:

Using features such as ELO and home/away records, I should be able to capture the data above the baseline and near the 0.60 mark. I don't suspect my project to come anywhere close to prediction levels of similar models that had more training data, but if I could get a model that consistently predicts upwards of >0.5 on a model for each of the six seasons. 

I believe that the information gathered on the first half of the season should be enough to decide which team performs well and which team doesn't. The changes from injuries and fluctuations in roster through trades should be accounted for because I would not be using seasonal data up to that point but rather average data from the last 10 games which should account for any dips or bumps in form. I hypothesize that throughout the EDA process and modeling that the features and key variables will be distributed normally and not have any severe differences.


## Executive Summary:

For this project, the main dataset was created by parsing HTML pages from basketball-reference.com. I created two functions, one that scraped box-scores of individual game pages and one that scraped schedule pages, these two functions used together were able to gather 6 seasons of box score data of each individual game. After scraping and cleaning this data, I added numerous features in an effort to improve the available feature set which were comprised of columns from the box score and advanced box score pages, one of these features being ELO which was then used to create home odds and probabilities. After this stage, we started using models and performing EDA simultaneously, trying to figure out what the first half of the season was telling us relative to second half performance and if we even can model it. Alongside this, I wanted to test the correlation of ELO and prominent box score features such as defensive rating, offensive rating, points scored, and opponent points scored. I found that all four of those features are highly correlated to ELO using joint-plots and teams that were offensively successful generally had higher ELOs. The distributions for prominent featurs such as ELO, offensive rating, defensive rating, points scored, and points conceded were normal and in no way skewed to either direction, ELO was the feature that had the most variance when looking at the features during modeling. The modeling stage has been disappointing. Both using PCA and not using PCA to limit features, it has consistently produced low scores. It is likely in this case, that in order for a good NBA model to work, the training data size has to be larger even when only predicting for a half season. The evidence for this is other NBA predictors using similar features and getting better results due to larger training data size. 

## Data Sources

### Basketball Reference

Our dataset was parsed using [basketball-reference.com](https://www.basketball-reference.com/). The dataset is comprised of all games spanning a six season period between the 2013-2014 season to the 2018-2019 season. 

The individual schedule links where you can directly get all the games I scraped from will be linked here.

- [2019 Season](https://www.basketball-reference.com/leagues/NBA_2019_games.html)

- [2018 Season](https://www.basketball-reference.com/leagues/NBA_2018_games.html)

- [2017 Season](https://www.basketball-reference.com/leagues/NBA_2017_games.html)

- [2016 Season](https://www.basketball-reference.com/leagues/NBA_2016_games.html)

- [2015 Season](https://www.basketball-reference.com/leagues/NBA_2015_games.html)

- [2014 Season](https://www.basketball-reference.com/leagues/NBA_2014_games.html)



## Web Scraping

I gathered all the raw data from basketball-reference as I mentioned previously. I used the BeautifulSoup, Time, and Requests packages to create the functions necessary to scrape the data directly from basketball reference. From these packages, I was able to create three functions, one for scraping the schedule data which got each individual game that happened in a given season, one for scraping the box score and advanced score data from that game for both teams, and the final function utilized both to get all the game data from just inputting the year you want to scrape for. These three functions can be found in the folder labeled functions under the scraping functions python script, you can import it into your jupyter notebook and test the functions yourself to see it's capability.

I scraped game data from the six season period between the 2013-2014 season to the 2018-2019 season, these six seasons were scraped two at a time due to scrape issues during the long-term google cloud scrape. After realizing that I couldn't scrape all six seasons at one time and just wait a day, I had to manually input individual scrapes for two seasons at a time. This took a little longer but still got the results necessary even if it mean't cleaning the data was more difficult due to the fact that the raw data was spread out between three dataframes.

All of the scraping functions I made are available on the scraping_functions.py script located in the functions folder.

## Data Cleaning

After gathering all the data, I looked to cleaning the raw data which primarily mean't separating player data from team data and then cleaning both individually. The raw data was given in two season formats due to scrape issues, while I could have combined the three dataframes together and completed the scrape in one-go, I wanted to test myself and create two cleaning functions for player and team data, which I would then apply to the three dataframes. The two functions I created, were dedicated to cleaning game data and player data, these functions can be seen in the cleaning functions script in the functions (python scripts) folder.

The data cleaning process was incredibly rigorous for team data in particular, for the modelling, I had to put the home and away teams for each game on the same column which mean't creating a dataframe with 100+ columns and trimming down the unnecessary columns that were essentially duplicates. This process had me analyzing the individual data columns and their purpose to see whether or not they would serve a purpose later on in the modeling or feature engineering process. Along with getting rid of columns, I also had to rename each column to indicate whether or not it was the away team or the home team, luckily, the game-id column made the merge and the subsequent renaming of columns very simple to execute in the grand scheme of the function.

The data cleaning process was more lax for player data, since I didn't have to merge the away and home halves of the dataframe, it was just a matter of adding some features that I added for the team data dataframe that weren't included in the player data dataframe. I created a function for this as well and had to impute some values that were missing when creating the added features, luckily, they were easily explainable and a simple fix.

All of the cleaning functions I made are available directly on the cleaning_functions.py script located in the functions folder.

## Feature Engineering

During the process of data cleaning, I added additional features not initially included in the box score or advanced box scores that were in the box score game web page. These columns were FG(3)_MISSED, FG_MISSED, BLOCKED_ATTEMPTS, TOV_FORCED, FG(2), FGA(2), and FG(2)_MISSED. All of these columns were made for both home and away teams, which is why they show up twice in the data dictionary column with _AWAY and _HOME attached respectively. This same format is used for the other added columns during the feature engineering process as well, as a way to make which column belonged to the away team and home team clear.

During feature engineering, I wanted to get the dataframe model ready which mean't absolutely no future data. In order to do that, I had to make a function that got the previous n amount of games to model on, initially I was thinking about utilizing season stats up to that game but that wouldn't accurately take into account current form as well. I wanted to capture the previous 10 or so games to capture how well the team is doing at that point, this is my attempt at trying to take into account a major injury or new trade as the bump or dip in a key stat would surely be noticeable when looking at the base stats.

Along with the N games function I created for modelling, I also created columns dedicated to presenting performance home and away. These columns are H_TEAM_WINS_AT_HOME, H_TEAM_LOSSES_AT_HOME, A_TEAM_WINS_AT_AWAY, A_TEAM_LOSSES_AT_AWAY, HOME_GAMES_TEAM_HOME, AWAY_GAMES_TEAM_AWAY, HOME_GAME_WIN_RATE_HOME, and AWAY_GAME_WIN_RATE_AWAY. They are self-explanatory from their column names, they are mean't to capture performance on a team's home-court and how they perform outside of home. The final set of features I created were based on ELO.

The ELO functions were made by Josh Weiner whose NBA predictor was one of the first I saw and is a concise repository that goes into detail on each step. The [repository](https://github.com/JoshWeiner/NBA_Game_Prediction/blob/main/CIS_545_Final_Project.ipynb) has a set of ELO functions that I used in the for loop which made the ELO columns, odds columns, and probabilities columns. Before I get into odds and probabilities, let me get into what exactly ELO is. The ELO rating system is a system used to assign a mathematical value to a player's skill, the base ELO value is 1500 and win probabilities and odds are calculated using the ELO values of both competitors. A team's given ELO value can lower or heighten depending on the result of a game, the severity of which is dependent on win/loss margin and the quality of the opponent. The odds and probabilities are included in the cleaned dataframe but only the odds column is included in the classification model dataframe, this is because odds have more favorability in a classification model than probabilities do, at least in the context of a logistic regression model. The rationale behind this decision is explored more in depth in this [article](https://www.theanalysisfactor.com/why-use-odds-ratios/) by Karen Grace-Martin. If you want to learn more about the specific ELO functions used and how I decided on a number to use when implementing home-court advantage into the model, you can check out this [article](https://fivethirtyeight.com/methodology/how-our-nba-predictions-work/) from FiveThirtyEight and this [article](https://medium.com/purple-theory/what-is-elo-rating-c4eb7a9061e0) that explains ELO ratings in larger detail.

All of the functions used in the notebook are available directly on the feature_engineering_functions.py script located in the functions folder.

### Data Dictionary for Added Columns
DISCLAIMER(THIS IS NOT THE DATA USED TO MODEL, THIS IS THE CLEANED DATA WHICH HAS FUTURE DATA FOR THE GAME ROW)

|                           | Type    | Description                                 | Example      |
|---------------------------|---------|---------------------------------------------|--------------|
| FG(3)_MISSED_HOME         | float64 | Three-point field goals missed (home team)  |       4.0    |
| FG(3)_MISSED_AWAY         | float64 | Three-point field goals missed (away team)  |       4.0    |
| FG_MISSED_HOME            | float64 | Field goals missed by home team             |      36.0    |
| FG_MISSED_AWAY            | float64 | Field goals missed by away team             |      38.0    |
| BLOCKED_ATTEMPTS_HOME     | float64 | Shots blocked by home team                  |       5.0    |
| BLOCKED_ATTEMPTS_AWAY     | float64 | Shots blocked by away team                  |       6.0    |
| TOV_FORCED_HOME           | float64 | Turnovers created by home team              |       8.0    |
| TOV_FORCED_AWAY           | float64 | Turnovers created by away team              |       8.0    |
| FG(2)_HOME                | float64 | Two-point field goals made (home team)      |      26.0    |
| FG(2)_AWAY                | float64 | Two-point field goals made (away team)      |      24.0    |
| FGA(2)_HOME               | float64 | Two-point field goals attempted (home team) |      48.0    |
| FGA(2)_AWAY               | float64 | Two-point field goals attempted (away team) |      56.0    |
| FG(2)_MISSED_HOME         | float64 | Two-point field goals missed (home team)    |      28.0    |
| FG(2)_MISSED_AWAY         | float64 | Two-point field goals missed (away team)    |      24.0    |
| H_TEAM_WINS_AT_HOME       | float64 | Home team wins when playing at home         |      24.0    |
| H_TEAM_LOSSES_AT_HOME     | float64 | Home team losses when playing at home       |      26.0    |
| A_TEAM_WINS_AT_AWAY       | float64 | Away team wins when playing away            |      21.0    |
| A_TEAM_LOSSES_AT_AWAY     | float64 | Away team losses when playing away          |      21.0    |
| HOME_GAMES_TEAM_HOME      | float64 | Home games played by home team              |      40.0    |
| AWAY_GAMES_TEAM_AWAY      | float64 | Away games played by away team              |      41.0    |
| HOME_GAME_WIN_RATE_HOME   | float64 | Home team win rate when playing at home     |      0.61    |
| AWAY_GAME_WIN_RATE_AWAY   | float64 | Away team win rate when playing away        |      0.50    |
| TEAM_ELO_BEFORE_HOME      | float64 | Home team ELO before result                 |      1500    |
| TEAM_ELO_BEFORE_AWAY      | float64 | Away team ELO before result                 |      1500    |
| TEAM_ELO_AFTER_HOME       | float64 | Home team ELO after result                  |     1595.67  |
| TEAM_ELO_AFTER_AWAY       | float64 | Away team ELO after result                  |     1420.67  |
| ODDS_HOME                 | float64 | Odds home team wins                         |      1.64    |
| PROBS_HOME                | float64 | Probability home team wins                  |      0.64    |
| PROBS_AWAY                | float64 | Probability away team wins                  |      0.36    |

## EDA

The EDA for this project was fairly minimal and focused on finding the correlation between engineered features (most notably ELO) with other box score features most notably, offensive rating, defensive rating, opponent score, and team score. There are a plethora of features and columns that exploring each in depth would require further time that under the current general assembly constraints I am unable to do. The charts created and the data explored in the EDA notebook primarily focus on ELO and it's relation to the features mentioned previously, these ideas were borrowed from the EDA done by Josh Weiner and his team when working on a similar NBA predictor that also used ELO. The reason why I went in this direction is because of ELO's prevalence in notable NBA game predictors, most notably FiveThirtyEight's CARM-ELO system used for predicting NBA games and this was also the primary reason why the home court advantage was set at 95, to match FiveThirtyEight's number used.

The initial visualizations were to see if there was any real difference between away elo and home elo for teams, that chart gave me typical results as there were no drastic differences particularly between away elo and home elo. After that proved to have fairly typical results, I wanted to see how ELO correlates with offensive rating, defensive rating, and score using jointplots on a random team. The charts will vary from team to team of course but the results are promising and from the box plots made later it seems as if all of the stats mentioned are correlated with one another. After constructing the jointplots, I remained focused on using seaborn plots as a means to show the variation between teams and the stats mentioned previous. This was done using violin plots and box-whisker plots.

After using seaborn to create the plots mentioned previously, I wanted to use matplotlib to illustrate the means of points scored and ELO using bar-plots. These charts weren't as detailed and refined as the previous graphs but are relevant to mention regardless. The final graphs created, I wanted to plot two histograms looking at the distribution of the columns mentioned previously but split into the two halves of a season. The histograms showed that there were differences between the two halves in terms of distribution though minimal. The most apparent finding from these histograms is the fact that ELO in the second half of the season is skewed to the right, this is likely due to the fact that teams that are bad want to lose more to help their offseason draft lottery odds (this is known as tanking) which then leads to an imbalance as the already good teams consistently heighten their ELO scores further by beating up on losing teams or teams dealing with fatigue/injury.

## MODELING PERFORMANCE

The modeling performance has been very lackluster, this is likely due to a minimal amount of time spent modeling compared to EDA, cleaning, and feature engineering. I'm confident that there is a feature-set in what already exists in the data that is ideal, it's just a matter of finding that feature-set and seeing the results of that model and tuning the hyperparameters and tweaking the model. The likely answer to this sadly, might be that it's dificult to produce good results with a training dataset thats only less than the size of the first half of the season when you take into account that the dataframe ignores the first ten games of the season due to the function used during data engineering.

The best model was a kNN model using unscaled data, I didn't adjust the hyperparameters throughout the process only experimenting with feature selection. Further modeling down the road, will require hyper-parameter selection via both random-search and grid-search. Logistic Regression and Random Forest models also showed promise using different datasets, the margins between kNN, Logistic Regression, and Random Forest were all miniscule and it warrants further investigation into modeling.

## RESULTS

1. I was unable to create a model that reached 0.6 r2 score, while I was above the baseline of 0.5, considering the fact that the team with the best record wins 68% of the time, it makes my model far below par. This could be attributed to the fact that one half season of data is not enough to create an accurate model but additionally, there are intangible factors at play in the second half of the season that aren't detected in any model. Those intangible factors are primarily due to player personnel, management, and roster construction. If a team suffers a harsh plateau at the end of the season due to injuries, it might take a while for the model to catch up from that fact just from detecting team stats or it could bethe opposite where in the second half, the roster of a team gets healthier. Roster injuries and additions via trade or free agency are what this model overlooks because it can't account for that just from team stats alone. Depelted and added rosters are hard to reasonably predict on and with the ongoing shuffling of NBA rosters, this only compounds further and further.

2. Offensive and defensive performance generally don't change too drastically over the course of the season in totality, further research could be done looking at individual teams but generally speaking point totals and league-wide performance does not change from half to half.

3. ELO is tied heavily to point totals, this is due to the fact that the formula accounts for margin of win and loss so its natural that higher point totals are similarily correlated. Offensive and defensive performance as well are heavily correlated. The nature of ELO makes it a great predictor and is why numerous models use it alongside the most esteemed of which being fivethirtyeight's model.

4. Great success, used Josh Weiner's functions to create the ELO columns but did modify the for loop to account for my dataframe and added additional features such as ELO that doesn't continue from season to season.

## NEXT STEPS

The model so far has been lackluster, I will continue to update the function used to get n games in an effort to take advantage of the entire dataset, see whether using the additional ten games at the beginning leads to better results. It is most likely, that in order to actually create a model that predicts the back-half of a season. We would need a plethora more training data. I doubt more features would be the solution given the sheer amount of features already in the model at it's disposal. Perhaps, a new project can be spun off from this using the same data that takes into account previous season performance + first half season performacne in order to predict wins in the second half. A similar project was done by Gregory Jean-Baptiste, Xuejiao Liu, and Dionny Santiago ([project link](http://dionny.github.io/NBAPredictions/website/)) where they train numerous ml models on the previous season's data + beginning of the season they were modeling on.

Further EDA could be done to perform more plots illustrating potential differences on the second and first halves of a given NBA season. Some ideas potentially could be creating a for loop that creates histograms of each column in both the first half and second half dataframes in the EDA notebook.

Further feature engineering could be done, most notably improving the function that takes previous n games and make it account for potential index errors by using try and except clauses in the function. Additional data such as player data could be incorporated into the dataframe to improve the model's selection of features but it's a lot more viable to spin off the existing data and features into a new project that looks at a new problem entirely and uses ML NBA game prediction from there.

## SOFTWARE REQUIREMENTS
### Programming language used: 

#### Python

### Cloud software used:

#### Google Cloud (Majority of work done on cloud)

### Packages prominently used:

- Pandas: For data structures and operations for manipulating numerical tables

- Numpy: For work on large, multi-dimensional arrays, mathematical functions, and matrices.

- Seaborn: Data visualization built on top of Matplotlib and integrates well with Pandas.

- Matplotlib: The base data visualization and plotting library for Python, seaborn is built on top of this package

- BeautifulSoup4: For work on parsing HTML pages and extracting elements from them specifically used for basketball-reference.com.

- Time: Python module used for various operations but specifically to delay loops while scraping.

- Requests: To help the web scrape go smoother by making HTTP requests simpler and readable.

- Statistics: Python module used for various operations made to calculate specific statistical equations.

- Scikit-Learn: Scikit-learn is a free software machine learning library for the Python programming language. Specific Scikit-Learn libraries used are neighbors, ensemble, pipeline, model selection, metrics, linear model, and pre-processing

## RESOURCES USED
[Josh Weinder: NBA ML github repository](https://github.com/JoshWeiner/NBA_Game_Prediction/blob/main/CIS_545_Final_Project.ipynb)

[Analysis Factor: Why use odds ratios](https://www.theanalysisfactor.com/why-use-odds-ratios/)

[Fivethirtyeight: How our predictions work](https://fivethirtyeight.com/methodology/how-our-nba-predictions-work/)

[What is ELO?](https://medium.com/purple-theory/what-is-elo-rating-c4eb7a9061e0)

[Eric Scot Jones: Predicting NBA Outcomes](https://library.ndsu.edu/ir/bitstream/handle/10365/28084/Predicting%20Outcomes%20of%20NBA%20Basketball%20Games.pdf?sequence=1&isAllowed=y)

[Jaak Udmae: Predicting NBA Outcomes](http://cs229.stanford.edu/proj2017/final-reports/5231214.pdf)
