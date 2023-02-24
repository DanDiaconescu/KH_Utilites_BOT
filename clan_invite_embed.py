import discord
import contact_destiny_api
from discord.ext import tasks


class ClanEmbed(discord.Embed):
    def __init__(self, clan_numbers):
        super().__init__(title="CLAN LINKS", color=0xc75450)

        self.url_dict = {
            'A': 'http://destiny2.ro/clana',
            'B': 'http://destiny2.ro/clanb',
            'C': 'http://destiny2.ro/clanc',
            'F': 'http://destiny2.ro/clanf',
            'X': 'http://destiny2.ro/clanx'
        }

        self.clan_admin = {
            'A': [160472069606342656, 492731788079267840, 489214493503520778],
            'B': [614544813530021920, 273722496212008960],
            'C': [527863507270631445],
            'F': [264069820633448448, 477846486403645454],
            'X': [740857014439247902, 249290472189591554, 335821679953707019]
        }

        self.set_author(name='Karpathian Horsemen',
                        icon_url='https://cdn.discordapp.com/icons/710809754057834496/c1e14b8c875da15ad7f84409c5559c79.jpg')
        self.set_thumbnail(url='https://www.pngitem.com/pimgs/m/63-636562_join-us-won-t-you-hd-png-download.png')

        for clan in clan_numbers:
            ping_str = ' '.join([f'<@{user}>' for user in self.clan_admin[clan]])
            if clan_numbers[clan] > 5:
                locuri_clan = f"{clan_numbers[clan]} locuri libere"
            elif clan_numbers[clan] <5:
                locuri_clan = f"{clan_numbers[clan]} locuri rezervate"
            else:
                locuri_clan = "CLAN PLIN"
            self.add_field(name='',
                           value=f'Clan {"<:steam:886894682389508136>" if clan != "X" else "<:xbox:896241390005145651>"} [Karpathian Horsemen #{clan}]({self.url_dict[clan]}) **{locuri_clan}** \n Contact: {ping_str} \n {"—" * 30} \n',
                           inline=False)

        self.set_footer(text='© Karpathian Horsemen',
                        icon_url='https://cdn.discordapp.com/icons/710809754057834496/c1e14b8c875da15ad7f84409c5559c79.jpg')


async def init(interaction, bot):
    global msg_id

    await interaction.response.send_message(content='Asteapta', ephemeral=True)
    channel = interaction.channel

    clan_numbers = get_clan_stats()

    # await interaction.followup.send(content='', embed=ClanEmbed(clan_numbers))
    # message_ = await interaction.original_response()

    massage = await channel.send(content='', embed=ClanEmbed(clan_numbers))
    with open('embed_msg.txt', 'w') as f:
        f.write(str(massage.id))

    # do_refresh_embed.start(massage)

    print(f'Finish \n{"—" * 10}')


def get_clan_stats():
    clan_numbers = {}
    letters = ['A', 'B', 'C', 'F', 'X']

    for letter in letters:
        clan_dict = contact_destiny_api.get_destiny_clan_memebrs_by_letter(letter)
        clan_numbers[letter] = (100 - len(clan_dict))
    return clan_numbers


# @tasks.loop(minutes=60)
# async def do_refresh_embed(message):
#     print(f'{"—" * 5} Refresh embed clan link {"—" * 5}')
#     clan_numbers = get_clan_stats()
#     await message.edit(content='', embed=ClanEmbed(clan_numbers))





