import requests
import pandas as pd

url = "https://stats.nba.com/stats/leagueLeaders"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Referer': 'https://www.nba.com/',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Origin': 'https://www.nba.com',
    'Connection': 'keep-alive',
}

params = {
    'LeagueID': '00',
    'PerMode': 'PerGame',
    'Scope': 'S',
    'Season': '2024-25',
    'SeasonType': 'Regular Season',
    'StatCategory': 'PTS'
}

response = requests.get(url, headers=headers, params=params, timeout=15)
response.raise_for_status()

data = response.json()

# Extract the column headers and player data
headers = data['resultSet']['headers']
rows = data['resultSet']['rowSet']

# Create DataFrame
df = pd.DataFrame(rows, columns=headers)
df.to_csv('nba_league_leaders.csv', index=False)

print("CSV saved successfully: nba_league_leaders.csv")
