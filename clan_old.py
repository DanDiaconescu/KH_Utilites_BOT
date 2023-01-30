import discord
import find_players


class ClanEmbed(discord.Embed):
    def __init__(self, clan_numbers):
        super().__init__(title="CLAN LINKS", color=0xc75450 )

        self.url_dict = {
            'A': 'https://www.bungie.net/en/ClanV2?groupid=4066018',
            'B': 'https://www.bungie.net/en/ClanV2?groupid=4231275',
            'C': 'https://www.bungie.net/en/ClanV2?groupid=4397838',
            'F': 'https://www.bungie.net/en/ClanV2?groupid=4422836',
            'X': 'https://www.bungie.net/en/ClanV2/Index?groupId=4613286'
        }

        self.clan_admin = {
            'A': [160472069606342656, 492731788079267840, 489214493503520778],
            'B': [614544813530021920, 273722496212008960],
            'C': [527863507270631445],
            'F': [264069820633448448, 477846486403645454],
            'X': [740857014439247902, 249290472189591554, 335821679953707019]
        }

        self.set_author(name='Karpathian Horsemen', icon_url='https://cdn.discordapp.com/icons/710809754057834496/c1e14b8c875da15ad7f84409c5559c79.jpg)')
        self.set_thumbnail(url='https://www.pngitem.com/pimgs/m/63-636562_join-us-won-t-you-hd-png-download.png')

        for clan in clan_numbers:
            ping_str = ' '.join([f'<@{user}>' for user in self.clan_admin[clan]])
            self.add_field(name=f'Clan {":steam:" if clan != "X" else ":xbox:"} [Karpathian Horsemen #{clan}]({self.url_dict[clan]}) **{f"{clan_numbers[clan]} free spaces" if clan_numbers[clan] != 0 else "FULL CLAN"}**',
                           value=f"Contact: {ping_str} \n \n \n",
                           inline=False)

        self.set_footer(text='© Karpathian Horsemen', icon_url='https://cdn.discordapp.com/icons/710809754057834496/c1e14b8c875da15ad7f84409c5559c79.jpg)')


# async def ping_user(user_id, bot):
#     user = bot.get_user(user_id)
#     return user


async def init(ctx):
    clan_numbers = {}
    letters = ['A', 'B', 'C', 'F', 'X']
    for letter in letters:
        clan_dict = find_players.get_destiny_clan_memebrs_by_letter(letter)
        clan_numbers[letter] = (100 - len(clan_dict))

    await ctx.send(embed=ClanEmbed(clan_numbers))

