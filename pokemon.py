from query import query
from PIL import Image
import requests
from io import BytesIO

class Pokemon:

    def __init__(self, identifier):

        pokemon = query('/api/v1/pokemon/' + identifier)

        description_uri = pokemon['descriptions'][0]['resource_uri']

        self.id = pokemon['national_id']
        self.name = pokemon['name']
        self.sprite = 'http://pokeapi.co/media/img/' + str(self.id) + ".png"
        self.description = query(description_uri)['description']

        weight = float(int(pokemon['weight']) / 10)

        self.kg = str(weight)
        self.pounds = str(round(weight * 2.2, 1))

        height = float(int(pokemon['height']) / 10)
        self.meters = str(height)

        total_inches = height * 100 * 0.39

        self.inches = int(total_inches % 12)
        self.feet = int(total_inches / 12)

        self.type1 = pokemon['types'][0]["name"]
        self.type2 = pokemon['types'][1]["name"] if len(pokemon['types']) > 1 else "none"

        self.hp = pokemon['hp']

        self.attack = pokemon['attack']
        self.special_attack = pokemon['sp_atk']

        self.defense = pokemon['defense']
        self.special_defense = pokemon['sp_def']

        self.speed = pokemon['speed']

        self.exp = pokemon['exp']

        self.background_color = get_background_color(self.sprite)


def get_background_color(url):

    print("using url: ", url)
    response = requests.get(url)

    image = Image.open(BytesIO(response.content))
    image = image.convert('RGB')

    width, height = image.size
    pixels = image.load()

    r, g, b, count = 0, 0, 0, 0

    for x in range(width):
        for y in range(height):
                pixel = pixels[x, y]

                r += int(pixel[0])
                g += int(pixel[1])
                b += int(pixel[2])

                if pixel[0] is 0 and pixel[1] is 0 and pixel[2] is 0:
                    continue

                count += 1

    return (int((r/count)), int((g/count)), int((b/count)))