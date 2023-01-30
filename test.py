import find_players
from datetime import datetime

players = find_players.get_destiny_clan_memebrs_by_letter('A')


def days_between(date):
    current_time = datetime.now()
    delta = current_time - date
    return delta.days

for player in players:
    time = players[player]
    if days_between(time) >= 90:
        print(days_between(time) , player)
