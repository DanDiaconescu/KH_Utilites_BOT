import pydest
import asyncio


# https://github.com/jgayfer/pydest/blob/master/examples/find_user.py
# https://bungie-net.github.io/multi/operation_get_GroupV2-GetMembersOfGroup.html#operation_get_GroupV2-GetMembersOfGroup
# https://github.com/jgayfer/pydest


async def main(display_name):
    destiny = pydest.Pydest('9d6a3967b68d44baa53f9238a8229689')

    res = await destiny.api.search_destiny_player(-1, display_name)
    print(res)

    if res['ErrorCode'] == 1 and len(res['Response']) > 0:
        print("---")
        print("Player found!")
        print("Display Name: {}".format(res['Response'][0]['displayName']))
        print("Membership ID: {}".format(res['Response'][0]['membershipId']))
    else:
        print("Could not locate player.")
        return 0, 0


    player_id = {
        'name': res['Response'][0]['displayName'],
        'mem_id': res['Response'][0]['membershipId'],
    }

    platforms = res['Response'][0]['applicableMembershipTypes']

    if len(platforms) > 1:
        for platform in platforms:
            if platform == 3 or platform == 6:
                player_id['mem_type'] = 'pc'
            elif platform == 2:
                player_id['mem_type'] = 'ps'
            elif platform == 1:
                player_id['mem_type'] = 'xb'
    else:
        platform = platforms[0]
        if platform == 3 or platform == 6:
            player_id['mem_type'] = 'pc'
        elif platform == 2:
            player_id['mem_type'] = 'ps'
        elif platform == 1:
            player_id['mem_type'] = 'xb'

    # player_data = await destiny.api.get_historical_stats_for_account(platform, player_id['mem_id'], [104])

    # player_profile = await destiny.api.get_profile(platform, player_id['mem_id'], [100])
    # if int(player_profile['ErrorCode']) == 1:
    #     player_profile = player_profile['Response']
    #     player_profile = player_profile['profile']
    # else:
    #     return

    player_data = await destiny.api.get_historical_stats(-1, player_id['mem_id'], 0 , [1], [4])
    player_data = {
        'total_raids': player_data['Response']['raid']['allTime']['activitiesCleared']['basic']['displayValue'],
        'kda': player_data['Response']['raid']['allTime']['efficiency']['basic']['displayValue']
    }

    # with open('dan1.json', 'w') as f:
    #     f.write(str(res))
    #
    # with open('dan2.json', 'w') as f:
    #     f.write(str(player_data))

    await destiny.close()
    return player_id, player_data


def get_member_data(display_name):
    loop = asyncio.new_event_loop()
    result1, result2 = loop.run_until_complete(main(display_name))
    loop.close()
    return result1, result2


# test1, test2 = get_member_data("Dan Diaconescu#8727")
# print(test2)
# print(type(test1['mem_type']))