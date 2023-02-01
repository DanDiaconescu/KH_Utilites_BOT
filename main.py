import datetime
from discord.ext import commands, tasks
import discord
import bot_clan_members
import clan_invite_embed
import sys


class UtilsBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True

        # super().__init__(command_prefix=commands.when_mentioned_or('$'), intents=intents)  # se apeleaza la @
        super().__init__(intents=intents, command_prefix=commands.when_mentioned_or('/test'))
        # sau cand e comanda cu $
        self.synced = False

    async def on_ready(self):
        if not self.synced:
            await command_tree.sync(guild=discord.Object(id=710809754057834496))
            self.synced = True
        cmd_channel = await bot.fetch_channel(797387549089333268)

        await cmd_channel.send(content='Bot online — Kind reminder sa restartezi embedul cu link-uri')
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

        print('Starting tasks...')
        do_refresh_embed.start()
        do_refresh_bot.start()
        print('Done!')

        print('------')
        print('Bot ready!')
        print('------')


bot = UtilsBot()
command_tree = bot.tree  # discord.app_commands.CommandTree(bot)


@command_tree.command(name='curatenie_generala', description='Admin-only',
                      guild=discord.Object(id=710809754057834496))
async def privat_1(interaction: discord.Interaction, role_call: discord.Role):
    print(f'{"—"*10} \nInitializare curatenie pentru {role_call.name} ')

    author = interaction.user.roles
    allowed_roles = [729027061322350762, 790256564110884864, 710818161867620412, 919993853933670480]

    is_allowed = 0
    for role in allowed_roles:
        if str(role) in str(author):
            is_allowed = 1
        else:
            pass

    if is_allowed:
        if role_call:
            await bot_clan_members.init(bot, role_call, interaction)
        else:
            await interaction.response.defer()
            await interaction.response.send_message(content='Teapa', ephemeral=True)
    else:
        await interaction.response.send_message(content='Teapa', ephemeral=True)


@command_tree.command(name='generate_clan_invite_embed', description='Admin-only',
                      guild=discord.Object(id=710809754057834496))
async def privat_2(interaction: discord.Interaction):
    print(f'{"—"*10} \nGenerare embed cu invinte link')
    author = interaction.user.roles
    allowed_roles = [729027061322350762, 790256564110884864]

    is_allowed = 0
    for role in allowed_roles:
        if str(role) in str(author):
            is_allowed = 1
        else:
            pass

    if is_allowed:
        await clan_invite_embed.init(interaction, bot)
    else:
        await interaction.response.send_message(content='Teapa', ephemeral=True)


@bot.event
async def on_member_join(member):
    print(f"{'—'*5} Generare mesaj membru nou - {member.name} {'—'*5}")
    welcome_channel = await bot.fetch_channel(954083245522313266)
    welcome_txt = '''Salut {} ! O sa fie nevoie să iți dai register ca să poți avea acces la canalele de pe server. 
Te rog să mergi pe <#938290015195238400> și să urmezi pașii de acolo. 
Dacă dai join pe unul dintre clanuri, te rog să dai tag responsabililor de clan pe <#938294344853647431>. 
Registerul cu Warmind (Charlemange) este obligatoriu in cadrul comunitatii noastre.
Dacă întâmpini probleme, te rog să contactezi un administrator in thread-ul de mai jos. '''
    new_message = await welcome_channel.send(content=welcome_txt.format(member.mention).replace('\n', ''))

    # server = await bot.fetch_guild(710809754057834496)
    # gatekeep = server.get_role(729027061322350762)
    # tech = server.get_role(790256564110884864)
    # admin = server.get_role(710818161867620412)

    admin_list = ['<@&729027061322350762>', '<@&790256564110884864>', '<@&710818161867620412>']
    new_thread = await new_message.create_thread(name=f'Support Thread - {member.name}')
    await new_thread.send(content=f'Dacă întâmpini probleme, te rog să ne lași un mesaj aici și te vom asista în cel mai scurt timp posibil. {member.mention} {" ".join(admin_list)}')


@tasks.loop(minutes=60)
async def do_refresh_embed():
    print(f'{"—" * 5} Refresh embed clan link {"—" * 5}')
    clan_invite_channel = await bot.fetch_channel(938290015195238400)
    try:
        with open('embed_msg.txt') as f:
            msg_id = str(f.readline())
    except:
        print('[INIT] Nu exista log al embedului')
        return

    if not msg_id:
        print('[INIT] Nu exista message_id al embedului')
        return

    try:
        embed_message = await clan_invite_channel.fetch_message(msg_id)
    except:
        print('[INIT] Mesajul cu embed nu mai exista!')
        return
    clan_numbers = clan_invite_embed.get_clan_stats()
    await embed_message.edit(content='', embed=clan_invite_embed.ClanEmbed(clan_numbers))


@tasks.loop(minutes=2)
async def do_refresh_bot():
    now = datetime.datetime.now()
    log_time = now.strftime("%m/%d/%Y %H:%M:%S")
    # print(f'[{log_time}] Refresh BOT')

# TOKEN = str(environ.get('TOKEN'))  # sus la run dropdown file -> edit config -> enviroment variables -> TOKEN
if len(sys.argv) > 1:
    TOKEN = sys.argv[1]
    bot.run(TOKEN)
