import urllib.request
from bs4 import BeautifulSoup
import json
import time

formats = ['ppr', 'half-ppr', 'standard']
teams = [8, 10, 12, 14]
data = {}

for fmt in formats:
    data[fmt] = {}
    for team in teams:
        data[fmt][team] = {}
        for spot in range(1, team + 1):
            url = f"https://fantasyfootballcalculator.com/draft-strategy/{fmt}/{team}-team/{spot}-spot"
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                html = urllib.request.urlopen(req).read()
                soup = BeautifulSoup(html, 'html.parser')
                
                # Find the table
                table = soup.find('table', {'class': 'draft-strategy'})
                if not table:
                    continue
                    
                rows = table.find_all('tr')[1:] # skip header
                strategies = []
                for r in rows:
                    cols = r.find_all('td')
                    if len(cols) >= 4:
                        rd1 = cols[0].text.strip()
                        rd2 = cols[1].text.strip()
                        rd3 = cols[2].text.strip()
                        fp = cols[3].text.strip()
                        strategies.append({
                            'rd1': rd1,
                            'rd2': rd2,
                            'rd3': rd3,
                            'fp': fp
                        })
                
                data[fmt][team][spot] = strategies
                print(f"Scraped {fmt} {team}-team {spot}-spot, got {len(strategies)} strats")
            except Exception as e:
                print(f"Error {fmt} {team}-team {spot}-spot: {e}")
            
            time.sleep(0.5)

with open('strategy_data.json', 'w') as f:
    json.dump(data, f)
