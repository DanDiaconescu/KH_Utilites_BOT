import discord
import contact_destiny_api
from datetime import datetime


async def init(bot, _role_call, interaction):
    member_dict = {}
    guilds = bot.guilds
    members = bot.get_all_members()
    for server in guilds:
        if server == 'Karpathian Horsemen':
            role_call = _role_call  # (' '.join(args))
            for role in server.roles:
                if role_call.name == role.name:
                    break
            else:
                return
    for member in members:
        if _role_call in member.roles:
            member_dict[member.display_name] = member.id
    overdue_list, not_found_list = compare_dicts(member_dict=member_dict, _role_call_name=_role_call.name)
    overdue_str = '\n'.join(overdue_list)
    not_found_str = '\n'.join(not_found_list)

    print(f'Finish \n{"—" * 10}')
    await interaction.response.send_message(embed=CustomEmbed(_role_call, overdue_str, not_found_str))


def compare_dicts(member_dict, _role_call_name):
    letter = str(_role_call_name.split(' ')[-1])
    overdue_list = []
    not_found_list = []

    clan_members = contact_destiny_api.get_destiny_clan_memebrs_by_letter(letter)
    member_list = [member for member in member_dict]
    for clan_member_name in clan_members:
        if clan_member_name in member_list or clan_member_name[:-5] in member_list:
            if days_between(clan_members[clan_member_name]) >= 90:
                overdue_list.append(f'🕒 {clan_member_name} inactiv {days_between(clan_members[clan_member_name])} zile')
            else:
                pass
        else:
            not_found_list.append(f'❔ {clan_member_name}')
    return overdue_list, not_found_list


def days_between(date):
    current_time = datetime.now()
    delta = current_time - date
    return delta.days


class CustomEmbed(discord.Embed):
    def __init__(self, role_id, overdue_str, not_found_str):
        super().__init__(title=f"Curatenie", color=0x309c8b)

        self.add_field(name=f'',
                       value=f'{role_id.mention}',
                       inline=False)
        if overdue_str:
            self.add_field(name=f'{"—" * 5} Overdue {"—" * 5} ',
                           value=f'{overdue_str}',
                           inline=False)

        if not_found_str:
            self.add_field(name=f'{"—" * 5} Not Found {"—" * 5} ',
                           value=f'{not_found_str}',
                           inline=False)
