import bungie_api

# dest_api = bungie_api.DestinyAPI()


def build_profile(player_info):  # display_name,
    # player_info = {'displayName': display_name}
    # player_general_info_call = dest_api.get_destiny_player(display_name)
    # player_info['membershipType'] = player_general_info_call['Response'][0]['membershipType']
    # player_info['membershipId'] = player_general_info_call['Response'][0]['membershipId']

    player_profile_call = dest_api.get_player_profile(player_info['membershipType'], player_info['membershipId'], [100])
    player_info['characterIds'] = player_profile_call['Response']['profile']['data']['characterIds']
    return player_info


def get_nighfalls(player_info):
    player_info = build_profile(player_info)
    nightfalls = {}
    nf_id = 1
    for char in player_info['characterIds']:
        _temp = dest_api.get_activity_history(player_info['membershipType'], player_info['membershipId'], char, 46)
        _temp = _temp['Response']['activities']

        for activity in _temp:
            activity_details = activity['activityDetails']
            activity_values = activity['values']
            ref_id = activity_details['referenceId']

            if activity_values['playerCount']['basic']['value'] > 1:
                continue
            if activity_values['completed']['basic']['value'] != 1:
                continue
            act_type = dest_api.get_activity_definitions('DestinyActivityDefinition', ref_id)
            if act_type['Response']['displayProperties']['name'] != 'Nightfall: Legend':
                continue

            act_period = activity['period']
            act_time = activity_values['activityDurationSeconds']['basic']['value']
            act_score = activity_values['score']['basic']['value']
            act_kills = activity_values['kills']['basic']['value']
            act_deaths = activity_values['deaths']['basic']['value']

            nightfalls[nf_id] = {'ref': ref_id,
                                 'period': act_period,
                                 'time': act_time,
                                 'score': act_score,
                                 'kills': act_kills,
                                 'deaths': act_deaths,
                                 }
            nf_id += 1
    if nightfalls:
        player_info['nightfalls'] = nightfalls
    else:
        player_info['nightfalls'] = 'Noob'
    return player_info


def get_raids(display_name):
    player_info = build_profile(display_name)
    raid_completions = {}
    raids_stats = {}
    for char in player_info['characterIds']:
        _temp = dest_api.get_activity_history(player_info['membershipType'], player_info['membershipId'], char, 4)
        _temp = _temp['Response']['activities']

        for activity in _temp:
            activity_details = activity['activityDetails']
            activity_values = activity['values']
            ref_id = activity_details['referenceId']

            if activity_values['completed']['basic']['value'] != 1:
                continue

            if raid_completions.get(ref_id, 0):
                raid_completions[ref_id] += 1
            else:
                raid_completions[ref_id] = 1

    for raid_id in raid_completions:
        act_type = dest_api.get_activity_definitions('DestinyActivityDefinition', raid_id)
        raid_name = act_type['Response']['displayProperties']['name']

        raids_stats[raid_name] = raid_completions[raid_id]

    if raids_stats:
        player_info['raids'] = raids_stats
    else:
        player_info['raids'] = 'Noob'
    return player_info


def get_all_nf(api_handler, player_info):
    global dest_api

    dest_api = api_handler
    player_info = get_nighfalls(player_info)
    return player_info

def get_all_raid(api_handler, player_info):
    global dest_api

    dest_api = api_handler
    player_info = get_raids(player_info)
    return player_info


# print(get_nighfalls('Dan Diaconescu#8727'))

# print(get_nighfalls('EMI#8597'))

# print(get_raids('Dan Diaconescu#8727'))
