from discord.ext import commands
import discord
from os import environ
import bot_clan_members
import clan_invite_embed
import sys


class UtilsBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True

        # super().__init__(command_prefix=commands.when_mentioned_or('$'), intents=intents)  # se apeleaza la @
        super().__init__(intents=intents, command_prefix=commands.when_mentioned_or('/'))
        # sau cand e comanda cu $
        self.synced = False

    async def on_ready(self):
        if not self.synced:
            await command_tree.sync(guild=discord.Object(id=710809754057834496))
            self.synced = True
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')


bot = UtilsBot()
command_tree = bot.tree  # discord.app_commands.CommandTree(bot)


# @bot.command(pass_context=True)
# @commands.has_permissions(manage_messages=True)
# async def get_curatenie_generala(ctx, _role_call: discord.Role):
#     if _role_call:
#         await bot_clan_members.init(ctx, _role_call)
#     else:
#         ctx.send(context='Teapa', ephemeral=True)
#
#
# @bot.command(pass_context=True)
# @commands.has_permissions(manage_messages=True)
# async def get_new_embed_with_clan_links(ctx):
#     await clan_invite_embed.init(ctx)


@command_tree.command(name='curatenie_generala', description='Admin-only',
                      guild=discord.Object(id=710809754057834496))
async def privat_1(interaction: discord.Interaction, role_call: discord.Role):
    print(f'{"—"*10} \nInitializare curatenie pentru {role_call.name} ')

    channel = bot.get_channel(797387549089333268)
    # message_id = channel.last_message_id
    # message = await channel.fetch_message(message_id)
    author = interaction.user.roles
    allowed_roles = [729027061322350762, 790256564110884864, 710818161867620412, 919993853933670480]

    # print(author)

    is_allowed = 0
    for role in allowed_roles:
        if str(role) in str(author):
            is_allowed = 1
        else:
            pass

    if is_allowed:
        # print("daaa")

        if role_call:
            await bot_clan_members.init(bot, role_call, interaction)
        else:
            await interaction.response.defer()
            await interaction.response.send_message(content='Teapa', ephemeral=True)
    else:
        # print('NUU')
        await interaction.response.send_message(content='Teapa', ephemeral=True)


@command_tree.command(name='generate_clan_invite_embed', description='Admin-only',
                      guild=discord.Object(id=710809754057834496))
async def privat_2(interaction: discord.Interaction):
    print(f'{"—"*10} \nGenerare embed cu invinte link')

    channel = bot.get_channel(797387549089333268)
    author = interaction.user.roles
    allowed_roles = [729027061322350762, 790256564110884864, 710818161867620412, 919993853933670480]



    # print(author)

    is_allowed = 0
    for role in allowed_roles:
        if str(role) in str(author):
            is_allowed = 1
        else:
            pass

    if is_allowed:
        # print("daaa")
        await clan_invite_embed.init(interaction)
    else:
        # print('NUU')
        await interaction.response.send_message(content='Teapa', ephemeral=True)


# TOKEN = str(environ.get('TOKEN'))  # sus la run dropdown file -> edit config -> enviroment variables -> TOKEN
if len(sys.argv) > 1:
    TOKEN = sys.argv[1]
    bot.run(TOKEN)

# https://discord.com/api/oauth2/authorize?client_id=1068908188520423486&permissions=534723950656&scope=bot