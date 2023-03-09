import json
import discord
from discord.utils import get


async def init(bot, interaction):
    await interaction.response.defer()
    donator_dict = {}
    delete_donator = {}
    guilds = bot.guilds
    members = bot.get_all_members()
    for server in guilds:
        if server.name == 'Karpathian Horsemen':
            server_booster = server.get_role(728638426672529510)
            donator_role = server.get_role(790921054419681280)

    update_channel = await bot.fetch_channel(1078798703902597252)

    for member in members:
        if server_booster in member.roles:
            donator_dict[member.display_name] = member.id
        elif donator_role in member.roles and not server_booster in member.roles:
            delete_donator[member.display_name] = member.id

    with open('./utilities/donator_db.json') as f:
        donator_manual = json.load(f)
        donator_list = donator_manual['data']

    for donator in donator_list:
        from datetime import datetime

        if donator['name'] in delete_donator and datetime.now() < datetime.strptime(donator['time'], '%d/%m/%Y'):
            delete_donator.pop(donator['name'])
        else:
            # aici pus await scos rol
            donator_manual['data'].remove(donator)

    with open('./utilities/donator_db.json', 'w') as f:
        json.dump(donator_manual, f, indent=4)

    print(f'Finish \n{"—" * 10}')
    await interaction.followup.send(embed=CustomEmbed_1(delete_donator))
    await interaction.followup.send(embed=CustomEmbed_2(donator_dict))
    await interaction.followup.send(embed=CustomEmbed_3(donator_manual['data']))


class CustomEmbed_1(discord.Embed):
    def __init__(self, delete_donator):
        super().__init__(title=f"Lista de donatori care trebuie stersi", color=0xc8192b)

        for not_don in delete_donator:
            self.add_field(name=f'',
                           value=f'<@{delete_donator[not_don]}>',
                           inline=False)


class CustomEmbed_2(discord.Embed):
    def __init__(self, donator_dict):
        super().__init__(title=f"Lista Boosteri", color=0xf47fff)

        for booster in donator_dict:
            self.add_field(name=f'',
                           value=f'<@{donator_dict[booster]}>',
                           inline=False)


class CustomEmbed_3(discord.Embed):
    def __init__(self, donator_manual):
        super().__init__(title=f"Lista de donatori concursuri", color=0xffc83d)

        for donator in donator_manual:
            self.add_field(name=f'',
                           value=f'<@{donator["id"]}> pana la data de __**{donator["time"]}**__',
                           inline=False)


'''

—————————————————————————————————————————————————————————————————————————————————————————————————
                    Adauga
—————————————————————————————————————————————————————————————————————————————————————————————————

'''


async def add_donator(interaction, member, time):
    await interaction.response.defer()

    new_donator_dict = {'name': member.display_name,
                        'id': member.id,
                        'time': time}

    with open('./utilities/donator_db.json', 'r+') as f:
        donator_manual = json.load(f)
        donator_manual['data'].append(new_donator_dict)
        f.seek(0)
        json.dump(donator_manual, f, indent=4)

    await interaction.followup.send(content=f'Adaugat la lista de donatori {member.mention} pana pe data de **{time}**')
