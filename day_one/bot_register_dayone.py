import discord
from day_one import bot_get_char_summary


async def init(cmd_channel, args):
    print(len(args))
    print(args)
    if len(args) == 6:
        member_info = {}
        for member in args:
            member_info[member.nick] = [member.mention]
        await cmd_channel.send(embed=RegisterEmbed(member_info))
    else:
        # await cmd_channel.send(content='Gresit', ephemeral=True)
        print('nasol')


class RegisterEmbed(discord.Embed):
    def __init__(self, member_info):
        super().__init__(title=f"Echipa noua Day One", color=0x75d975)

        for member in member_info:
            member_info, member_raid = bot_get_char_summary.get_member_data(member)
            if member_info and member_raid:
                self.add_field(name ='Nume', value=fr'[{member}](https://raid.report/{member_info["mem_type"]}/{member_info["mem_id"]})')
                self.add_field(name='Total completions', value= f'{member_raid["total_raids"]}')
                self.add_field(name='KDA', value=f'{member_raid["kda"]}')
                self.add_field(name='', value='', inline=False)
            else:
                continue
