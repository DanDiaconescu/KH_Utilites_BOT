import urllib
import requests


class DestinyAPI:
    def __init__(self):
        self.HEADERS = {"X-API-Key": '9d6a3967b68d44baa53f9238a8229689'}
        self.api_url = 'https://www.bungie.net/platform'

    # destinyMembershipId = 4611686018493903636
    # membershipId = 4611686018493903636
    # characterId = 0
    # displayName = 'Dan Diaconescu#8727'

    def get_destiny_player(self, displayName):
        membershipType = -1
        url = f"{self.api_url}/Destiny2/SearchDestinyPlayer/{membershipType}/{displayName}/"
        encoded_url = urllib.parse.quote(url, safe=':/?&=,.')
        r = requests.get(encoded_url, headers=self.HEADERS)
        data = r.json()
        if data['ErrorCode'] == 1:
            return r.json()
        raise Exception('Player not found!!!')

    def get_player_by_id(self, membershipID):
        url = f"{self.api_url}/User/GetBungieNetUserById/{membershipID}/"
        encoded_url = urllib.parse.quote(url, safe=':/?&=,.')
        r = requests.get(encoded_url, headers=self.HEADERS)
        return r.json()

    def get_player_profile(self,membershipType, destinyMembershipId, components):  # de pus components as Union
        url = f"{self.api_url}/Destiny2/{membershipType}/Profile/{destinyMembershipId}/?components={','.join(str(comp) for comp in components)}"
        encoded_url = urllib.parse.quote(url, safe=':/?&=,.')
        r = requests.get(encoded_url, headers=self.HEADERS)
        return r.json()

    def get_activity_history(self, membershipType, destinyMembershipId, characterId, mode):
        # de chimbat 'mode=' in alt mod daca se doreste sa se verifice alte activitati decat nightfall
        url = f"{self.api_url}/Destiny2/{membershipType}/Account/{destinyMembershipId}/Character/{characterId}/Stats/Activities/?mode={mode}"
        encoded_url = urllib.parse.quote(url, safe=':/?&=,.')
        r = requests.get(encoded_url, headers=self.HEADERS)
        return r.json()

    def get_activity_definitions(self, entity_type: str, hash):
        url = f"{self.api_url}/Destiny2/Manifest/{entity_type}/{hash}/"
        encoded_url = urllib.parse.quote(url, safe=':/?&=,.')
        r = requests.get(encoded_url, headers=self.HEADERS)
        return r.json()

    def get_data_by_link(self, link):
        link = link.split('/')
        membershipType = int(link[-2])
        membershipID = link[-1]
        membershipID = int(membershipID.split('?')[0])
        'https://www.bungie.net/7/en/User/Profile/3/4611686018493903636?bgn=Dan%20Diaconescu'
        r = {'Response': [{
            'membershipType': membershipType,
            'membershipId': membershipID,
        }]}
        return r


test_dest = DestinyAPI()
# print(test_dest.get_destiny_player('Dan Diaconescu#8727'))

# print(test_dest.get_player_profile(3, 4611686018493903636, [100]))

# print(test_dest.get_activity_history(3, 4611686018493903636, 2305843009530324714))

# print(test_dest.get_activity_definitions('DestinyActivityDefinition', 2416314399))

# print(test_dest.get_player_by_id(23652611))

# print(test_dest.get_data_by_link('https://www.bungie.net/7/en/User/Profile/3/4611686018493903636?bgn=Dan%20Diaconescu'))