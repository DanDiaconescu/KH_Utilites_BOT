import datetime
import json

from api import bungie_api
import pytz


def get_nighfalls(player_info, _comp_time):
    global dest_api
    nightfalls = {}
    act_best_time = ''
    count = 0

    for char in player_info['characterIds']:
        try:
            _temp = dest_api.get_activity_history(player_info['membershipType'], player_info['membershipId'], char, 46)
            print(_temp)
            _temp = _temp['Response']['activities']

        except:
            continue

        for activity in _temp:
            activity_details = activity['activityDetails']
            activity_values = activity['values']
            ref_id = activity_details['referenceId']

            if activity_values['playerCount']['basic']['value'] > 1:
                continue
            # if activity_values['completed']['basic']['value'] != 1:
            #     continue
            # print(activity_values['activityDurationSeconds']['basic']['value'])
            # if not activity_values['activityDurationSeconds']['basic']['value']:
            #     continue

            act_period = activity['period']
            act_period_format = datetime.datetime.fromisoformat(act_period)
            # comp_time = datetime.datetime(2023,2,21,19,0,0)
            comp_time = _comp_time
            eet_timezone = pytz.timezone('Europe/Bucharest')
            act_period_format = act_period_format.astimezone(eet_timezone)
            comp_time = comp_time.astimezone(eet_timezone)

            if act_period_format < comp_time:
                continue

            count += 1

    print(count)
    #         act_time = activity_values['activityDurationSeconds']['basic']['value']
    #
    #         if not act_best_time:
    #             act_best_time = player_info.get('nightfalls', {}).get('time', 0)
    #
    #         try:
    #             act_type = dest_api.get_activity_definitions('DestinyActivityDefinition', ref_id)
    #         except:
    #             continue
    #         if act_type['Response']['displayProperties']['name'] != 'Nightfall: Legend':
    #             continue
    #
    #         if act_best_time and act_time > act_best_time:
    #             continue
    #         else:
    #             act_best_time = act_time
    #             act_score = activity_values['score']['basic']['value']
    #             act_kills = activity_values['kills']['basic']['value']
    #             act_deaths = activity_values['deaths']['basic']['value']
    #
    #             nightfalls = {'ref': ref_id,
    #                           'period': act_period,
    #                           'time': act_time,
    #                           'score': act_score,
    #                           'kills': act_kills,
    #                           'deaths': act_deaths,
    #                           }
    #
    # if nightfalls:
    #     player_info['nightfalls'] = nightfalls
    # else:
    #     player_info['nightfalls'] = {}
    # return player_info


def get_top_players(api_handler, _comp_time):
    global dest_api
    dest_api = api_handler

    all_players = []

    with open('./api/competitie.json', 'r') as file:
        #  escape in cazul in care e deja inscris
        file_data = json.load(file)
        index_max_print = len(file_data["comp"])
        index_print = 1
        for player_dict in file_data["comp"]:
            all_players.append(get_nighfalls(player_dict, _comp_time))
            print(f'{"—" * 3} working on it... {round((index_print / index_max_print) * 100)}%')
            index_print += 1
    #
    # with open('./api/competitie.json', 'w') as file:
    #     file_data = {}
    #     file_data["comp"] = all_players
    #     file.seek(0)
    #     json.dump(file_data, file, indent=4)

    all_players = [player for player in all_players if player['nightfalls']]
    all_players = sorted(all_players, key=lambda x: x['nightfalls']['time'])

    top_players = []
    if all_players:
        top_players = all_players[:4] if len(all_players) > 4 else all_players
    return top_players


def init_1(api_handler):
    top_players = get_top_players(api_handler, datetime.datetime(2023, 2, 21, 19, 0, 0))
    return top_players

dest_api = bungie_api.DestinyAPI()
print('a')
print(init_1(dest_api))

