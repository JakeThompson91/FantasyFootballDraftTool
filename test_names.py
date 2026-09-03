import re

tests = [
    "Bo Nix, Broncos",
    "Justin Jefferson, WR, Vikings",
    "Breece Hall, RB, Jets",
    "QB Bo Nix, Broncos",
    "Jahmyr Gibbs, Lions",
    "Puka Nacua, Rams",
    "De'Von Achane, RB, Dolphins"
]

for t in tests:
    clean = re.sub(r'^(QB|RB|WR|TE)\s+', '', t, flags=re.IGNORECASE)
    clean = clean.split(',')[0].strip().lower()
    print(f"'{t}' -> '{clean}'")

