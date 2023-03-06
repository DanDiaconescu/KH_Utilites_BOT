import discord
from api import bungie_api
import json
from random import randint


async def init(interaction, author, profile_link, cmd_channel):
    await interaction.response.defer(ephemeral=True)

    with open('./api/competitie.json', 'r') as file:
        #  escape in cazul in care e deja inscris
        file_data = json.load(file)
        for player_dict in file_data["comp"]:
            if player_dict['displayName'] == author:
                await interaction.followup.send(content='Deja te-ai inscris', ephemeral=True)
                return

    dest_api = bungie_api.DestinyAPI()
    player_info = {'displayName': author}
    try:
        player_data = dest_api.get_data_by_link(profile_link)
        player_info['membershipType'] = player_data['Response'][0]['membershipType']
        player_info['membershipId'] = player_data['Response'][0]['membershipId']
    except:
        await interaction.followup.send(
            content='Eroare, verifica link-ul, daca tot nu merge, contacteaza-l pe <@489214493503520778>',
            ephemeral=True)
        print('[EVENT] Eroare link')
        return

    try:
        player_data = dest_api.get_player_profile(player_info['membershipType'], player_info['membershipId'], [100])
        player_name = player_data['Response']['profile']['data']['userInfo']['bungieGlobalDisplayName']

        if player_name == author or author in player_name or player_name in author:
            pass
        else:
            await interaction.followup.send(
                content='Contul nu este al tau, daca este o eroare, contacteaza-l pe <@489214493503520778>',
                ephemeral=True)
            print('[EVENT] Eroare posesie cont')
            return
        player_info['characterIds'] = player_data['Response']['profile']['data']['characterIds']

    except:
        await interaction.followup.send(
            content='Eroare, verifica link-ul, daca tot nu merge, contacteaza-l pe <@489214493503520778>',
            ephemeral=True)
        print('[EVENT] Eroare generare profil')
        return

    with open('./api/competitie.json', 'r+') as file:
        file_data = json.load(file)
        file_data["comp"].append(player_info)
        # file_data["comp"] = list({tuple(sorted(d.items())): d for d in file_data["comp"]}.values())
        file.seek(0)
        json.dump(file_data, file, indent=4)

    await interaction.followup.send(content='Te-ai inscris cu succes!', ephemeral=True)
    await cmd_channel.send(embed=EmbedSuccess(player_info))
    return


class EmbedSuccess(discord.Embed):
    def __init__(self, player_info):
        messages = {
            1: 'Un nou jucător apare, {}!',
            2: '{} Bine ai venit, luptătorule!',
            3: 'Intră în ring: {}!',
            4: 'Noul nostru campion: {}!',
            5: 'Hai să-i urăm bun venit {}!',
            6: '{} A venit momentul să lupte!',
            7: 'Întâmpinăm un nou oponent!',
            8: 'Un alt jucător se alătură! {}',
            9: 'Începe războiul: {}!',
            10: 'Să-l salutăm pe {}!'
        }

        super().__init__(title=f"New Competitor!", color=0xdfff7a)

        self.add_field(name=f'',
                       value=messages[randint(1, 10)].format(
                           f"[{player_info['displayName']}]({'https://destinytracker.com/destiny-2/profile/bungie/{}/sessions'.format(player_info['membershipId'])})"),
                       inline=False)

        self.add_field(name=f'',
                       value='Competitia incepe pe data de **21/02/2023**, mult succes!',
                       inline=False)
