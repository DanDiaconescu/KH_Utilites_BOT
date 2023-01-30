import get_content
from datetime import datetime

# html_file = r''
# files = [f for f in os.listdir('.') if os.path.isfile(f)]
#
# for file in files:
#     if file.find('.html') > 1:
#         html_file = file


def get_destiny_clan_memebrs_by_letter(letter = 'A'):
    name_list = []
    last_online_list = []

    get_content.init(letter)

    with open('clan_site.txt', 'r', encoding="utf8") as f:
        text = f.readlines()
        for line in text:
            if '<a href="/7/en/User/Profile/' in line:
                name = line[line.find('>') + 1:]
                name = name.replace(r'</a>', '')
                name = name.replace(r'&#39;', "'")
                name = name.replace('\n', "")
                name_list.append(name)
            if '<p class="user-bnet last-played-date js-last-played-date">Last Online:  <em data-datetime="' in line:
                time = line.replace('<p class="user-bnet last-played-date js-last-played-date">Last Online:  <em data-datetime=', '')
                time = time[time.find('"') + 1:]
                time = time[:time.find('"')]
                time = datetime.strptime(time, '%m/%d/%Y %I:%M:%S %p')
                last_online_list.append(time)

        player_dict = dict(zip(name_list, last_online_list))
        return player_dict
