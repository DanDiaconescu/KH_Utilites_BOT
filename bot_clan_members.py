import discord
import find_players
from datetime import datetime


async def init(bot, _role_call, interaction):
    member_dict = {}
    guilds = bot.guilds
    members = bot.get_all_members()
    for server in guilds:
        if server == 'Karpathian Horsemen':
            # print(server)
            role_call = _role_call  # (' '.join(args))
            # role_id = server.roles[0]
            for role in server.roles:
                if role_call.name == role.name:
                    role_id = role
                    break
            else:
                # await ctx.send(content="Role doesn't exist", ephemeral=True)
                return
    for member in members:
        # print(member, end='')
        if _role_call in member.roles:
            # await ctx.send(f"{member.display_name} - {member.id}")
            member_dict[member.display_name] = member.id
    # else:
    #     await ctx.send(content=f"No member in role: {role_call.name}", ephemeral=True)
    #     return
    # print(member_dict)
    out_list = compare_dicts(member_dict=member_dict, _role_call_name=_role_call.name)
    out_string = '\n'.join(out_list)
    # await ctx.send(out_string)
    print(f'Finish \n{"—"*10}')
    await interaction.response.send_message(embed=CustomEmbed(_role_call, out_string))

def compare_dicts(member_dict, _role_call_name):
    letter = str(_role_call_name.split(' ')[-1])
    # print(letter)
    out_list = []
    clan_members = find_players.get_destiny_clan_memebrs_by_letter(letter)
    member_list = [member[:-5] if member.find('#') > 1 else member for member in member_dict]
    for clan_member_name in clan_members:
        if clan_member_name in member_list:
            if days_between(clan_members[clan_member_name]) >= 90:
                out_list.append(f'🕒 {clan_member_name} inactiv {days_between(clan_members[clan_member_name])} zile')
                # print('overdue', clan_member_name)
            else:
                pass
        else:
            out_list.append(f'❔ {clan_member_name}')
            # print('not_found', clan_member_name)
    return out_list


def days_between(date):
    current_time = datetime.now()
    delta = current_time - date
    return delta.days


class CustomEmbed(discord.Embed):
    def __init__(self, role_id, out_string):
        super().__init__(title=f"Curatenie", color=0x309c8b)

        self.add_field(name=f'',
                       value=f'{role_id.mention} \n \n {out_string}',
                       inline=False)