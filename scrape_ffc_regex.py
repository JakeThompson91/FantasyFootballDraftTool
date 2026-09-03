import urllib.request
import re
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
                html = urllib.request.urlopen(req).read().decode('utf-8')
                
                # Extract rows between <tr> and </tr> using regex
                # <table class="table draft-strategy">
                table_match = re.search(r'<table class="table draft-strategy">(.*?)</table>', html, re.DOTALL)
                if not table_match:
                    print("no table")
                    continue
                    
                table_html = table_match.group(1)
                rows = re.findall(r'<tr>(.*?)</tr>', table_html, re.DOTALL)
                
                strategies = []
                for r in rows[1:]: # skip header
                    cols = re.findall(r'<td[^>]*>(.*?)</td>', r, re.DOTALL)
                    if len(cols) >= 4:
                        rd1 = cols[0].strip()
                        rd2 = cols[1].strip()
                        rd3 = cols[2].strip()
                        fp = cols[3].strip()
                        strategies.append({
                            'rd1': rd1,
                            'rd2': rd2,
                            'rd3': rd3,
                            'fp': fp
                        })
                
                data[fmt][team][spot] = strategies
            except Exception as e:
                print(f"Error {fmt} {team}-team {spot}-spot: {e}")
            
            time.sleep(0.3)

with open('strategy_data.json', 'w') as f:
    json.dump(data, f)
print("Done")
