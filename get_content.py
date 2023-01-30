import urllib.request


def init(clan_letter):
    url_dict = {
        'A': r'https://www.bungie.net/en/ClanV2?groupid=4066018',
        'B': r'https://www.bungie.net/en/ClanV2?groupid=4231275',
        'C': r'https://www.bungie.net/en/ClanV2?groupid=4397838',
        'F': r'https://www.bungie.net/en/ClanV2?groupid=4422836',
        'X': r'https://www.bungie.net/en/ClanV2/Index?groupId=4613286'
    }

    url = url_dict[clan_letter]
    create_clan_txt(url)


def create_clan_txt(url):

    page = urllib.request.urlopen(url)
    txt = page.read()

    with open('clan_site.txt', 'wb') as f:
        f.write(txt)
