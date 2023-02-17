import datetime
import json
import pytz
import discord


# dest_api = bungie_api.DestinyAPI()


def get_nighfalls(player_info):
    global dest_api
    nightfalls = {}
    act_best_time = ''
    for char in player_info['characterIds']:
        try:
            _temp = dest_api.get_activity_history(player_info['membershipType'], player_info['membershipId'], char, 46)
            _temp = _temp['Response']['activities']
        except:
            continue

        for activity in _temp:
            activity_details = activity['activityDetails']
            activity_values = activity['values']
            ref_id = activity_details['referenceId']

            if activity_values['playerCount']['basic']['value'] > 1:
                continue
            if activity_values['completed']['basic']['value'] != 1:
                continue
            if activity_values['activityDurationSeconds']['basic']['value']:
                continue

            act_period = activity['period']
            act_period_format = datetime.datetime.fromisoformat('2023-02-11T22:17:02Z')
            comp_time = datetime.datetime(2023,2,21,19,0,0)
            eet_timezone = pytz.timezone('Europe/Bucharest')
            act_period_format = act_period_format.astimezone(eet_timezone)
            comp_time = comp_time.astimezone(eet_timezone)
            if act_period_format < comp_time:
                continue
            act_type = dest_api.get_activity_definitions('DestinyActivityDefinition', ref_id)
            if act_type['Response']['displayProperties']['name'] != 'Nightfall: Legend':
                continue


            act_time = activity_values['activityDurationSeconds']['basic']['value']

            if act_best_time and act_time > act_best_time:
                continue
            elif not act_best_time:
                act_best_time = act_time

            act_score = activity_values['score']['basic']['value']
            act_kills = activity_values['kills']['basic']['value']
            act_deaths = activity_values['deaths']['basic']['value']

            nightfalls = {'ref': ref_id,
                          'period': act_period,
                          'time': act_time,
                          'score': act_score,
                          'kills': act_kills,
                          'deaths': act_deaths,
                          }

    if nightfalls:
        player_info['nightfalls'] = nightfalls
    else:
        player_info['nightfalls'] = []
    return player_info


def get_top_players(api_handler):
    global dest_api
    dest_api = api_handler

    all_players = []

    with open('./api/competitie.json', 'r') as file:
        #  escape in cazul in care e deja inscris
        file_data = json.load(file)
        for player_dict in file_data["comp"]:
            all_players.append(get_nighfalls(player_dict))
    try:
        all_players = sorted(all_players, key=lambda x: x['nightfalls']['time'])
    except:
        all_players = []
    top_players = []
    if all_players:
        top_players = all_players[:4] if len(all_players) > 4 else all_players
    return top_players


async def init(channel, api_handler):
    top_players = get_top_players(api_handler)
    channel.send(embed=EmbedLeaderboard(top_players))
    with open('./api/setup.txt', 'w') as f:
        f.write(channel.last_message_id)

async def refresh_leaderboar(channel, api_handler):
    try:
        with open('./api/setup.txt') as f:
            msg_id = str(f.readline())
    except:
        print('[INIT] Nu exista log al leaderboard-ului')
        return

    if not msg_id:
        print('[INIT] Nu exista message_id al leaderboard-ului')
        return

    top_players = get_top_players(api_handler)

    try:
        message = await channel.fetch_message(msg_id)
    except:
        print('[INIT] Mesajul cu embed nu mai exista!')
        return
    await message.edit(content='', embed=EmbedLeaderboard(top_players))

class EmbedLeaderboard(discord.Embed):
    def __init__(self, top_players):
        super().__init__(title='Leaderboards — Speedrun', color=0x499c54)

        self.add_field(name='Eveniment sponsorizat de:',
                       value=f"<@534063567943499776>",
                       inline=False)
        if top_players:
            for player in top_players:
                self.add_field(name=f'{"—"*5}',
                               value=f"[{player['displayName']}]({'https://destinytracker.com/destiny-2/profile/bungie/{}/sessions'.format(player['membershipId'])})",
                               inline=False)
        else:
            self.add_field(name=f'{"—"*5}',
                           value=f"Reveniti pe data de 21/02",
                           inline=False)

        self.set_footer(text='Organizat de comunitatea Karpathian Horsemen')