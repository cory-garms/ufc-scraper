import pandas as pd

oddsdf1 = pd.read_csv('./aggregate_odds.csv')
print(len(oddsdf1))
oddsdf1_2 = pd.read_csv('./aggregate_odds2.csv')
print(len(oddsdf1_2))

oddsdf1 = pd.concat([oddsdf1, oddsdf1_2])

oddsdf1.to_csv('aggregate_odds_merged.csv')