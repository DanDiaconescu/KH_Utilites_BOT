import datetime
import pydest
import asyncio
import nest_asyncio

nest_asyncio.apply()


# https://github.com/jgayfer/pydest/blob/master/examples/find_user.py
# https://bungie-net.github.io/multi/operation_get_GroupV2-GetMembersOfGroup.html#operation_get_GroupV2-GetMembersOfGroup
# https://github.com/jgayfer/pydest


async def main(clan_id):
    destiny = pydest.Pydest('9d6a3967b68d44baa53f9238a8229689')

    clan_dict = await destiny.api.get_members_of_group(clan_id)

    player_dict = {}

    for player in clan_dict['Response']['results']:
        player_code = player['destinyUserInfo']['bungieGlobalDisplayNameCode']
        if len(str(player_code)) == 3:
            player_code = f'0{player_code}'
        player_name = f"{player['destinyUserInfo']['bungieGlobalDisplayName']}#{player_code}"
        player_dict[player_name] = datetime.datetime.fromtimestamp(int(player['lastOnlineStatusChange']))

    await destiny.close()
    return player_dict


def get_clan_data(clan_id):
    loop = asyncio.new_event_loop()  # new_event_loop()
    loop_result = loop.run_until_complete(main(clan_id))
    loop.close()
    return loop_result


def get_destiny_clan_memebrs_by_letter(letter='A'):
    grou_id_dict = {
        'A': 4066018,
        'B': 4231275,
        'C': 4397838,
        'F': 4422836,
        'X': 4613286
    }
    group_id = grou_id_dict[letter]
    clan_info_dict = get_clan_data(group_id)
    return clan_info_dict
