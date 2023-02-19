import datetime

import pydest
import asyncio


# https://github.com/jgayfer/pydest/blob/master/examples/find_user.py
# https://bungie-net.github.io/multi/operation_get_GroupV2-GetMembersOfGroup.html#operation_get_GroupV2-GetMembersOfGroup
# https://github.com/jgayfer/pydest

#
# async def main():
#     destiny = pydest.Pydest('9d6a3967b68d44baa53f9238a8229689')
#
#     clan_dict = await destiny.api.get_members_of_group(4231275)
#     print(clan_dict)
#
#     player_dict = {}
#
#     for player in clan_dict['Response']['results']:
#         if player.get('bungieNetUserInfo', ''):
#             player_dict[player['bungieNetUserInfo']['supplementalDisplayName']] = datetime.datetime.fromtimestamp(
#                 int(player['lastOnlineStatusChange']))
#         else:
#             player_dict[(player.get('destinyUserInfo', '').get('displayName', ''))] = datetime.datetime.fromtimestamp(
#                 int(player['lastOnlineStatusChange']))
#
#     print(player_dict)
#     # print(len(plyer_dict))
#
#     # print(await destiny.api.get_bungie_net_user_by_id(23652611))  - nu e buna
#     # print(await destiny.api.get_profile(3, 4611686018493903636, [100]))
#
#     await destiny.close()
#
#
# def get_clan_data():
#     loop = asyncio.new_event_loop()
#     loop.run_until_complete(main())
#     loop.close()
#
#
# get_clan_data()
