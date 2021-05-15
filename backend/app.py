import json
import uvicorn
from starlette.responses import JSONResponse
from unibots import salut
from unibots import Bot, Request, Keyboard

bot = Bot(platforms_sdk=[
    salut.SDK(),
])

app = bot.app

with open('names.json', 'r', encoding='utf8') as file:
    names = json.load(file)


def gender(name):
    return names.get(name, 'female')


@app.route('/test', methods=['GET'])
async def test(request):
    return JSONResponse({'ok': True})


bot.sort_routes()


def type_token(_type, nlu):
    if _type in nlu.types:
        return nlu.lemmas[nlu.types.index(_type)]


@bot.script
def script(r: Request):
    players = []
    players_indexes = {}

    rsp = bot.rsp(r)
    rsp.add_command({'type': 'update_data', 'action': {'players': players}})
    rsp.set_message('Привет! Это помощник для игры Манчкины. Здесь можно добавлять и отслеживать уровни игроков')
    yield rsp

    while True:
        rsp: salut.Response = bot.rsp(r)
        if r.type == 'SERVER_ACTION':
            name = r.action['name']
            if r.action['type'] == 'new_player':
                players_indexes[name] = len(players)
                players.append({'name': name, 'level': 1, 'gender': gender(name)})

            elif r.action['type'] == 'delete_player':
                del players[players_indexes[name]]
                del players_indexes[name]

            elif r.action['type'] == 'plus_player':
                if players[players_indexes[name]]['level'] < 10:
                    players[players_indexes[name]]['level'] += 1
            elif r.action['type'] == 'minus_player':
                if players[players_indexes[name]]['level'] > 1:
                    players[players_indexes[name]]['level'] -= 1
            rsp.add_command({'type': 'update_data', 'action': {'players': players}})
            yield rsp
            continue
        # print(r.nlu.types)
        # print(r.nlu.lemmas)

        name = type_token('NAME_TOKEN', r.nlu)
        if name:
            name = name.capitalize()
        lvl = type_token('NUM_TOKEN', r.nlu)
        action = r.nlu.tokens[0].lemma

        if action in ['добавить', ] and name:
            if players_indexes.get(name, None) is None:
                players_indexes[name] = len(players)
                players.append({'name': name, 'level': 1, 'gender': gender(name)})
                rsp.add_command({'type': 'update_data', 'action': {'players': players}})
                rsp.set_message(f'Игрок {name} добавлен')
            else:
                rsp.set_message(f'Игрок {name} уже есть в списке. Пожалуйста, используйте другое имя')

        elif (action in ['дать', 'сделать', 'изменить']) and name and (lvl is not None) and \
                ('уровень' in r.nlu.lemmas):
            if players_indexes.get(name, None) is not None:
                players[players_indexes[name]]['level'] = int(lvl)
                rsp.add_command({'type': 'update_data', 'action': {'players': players}})
                rsp.set_message(f'Игрок {name} получил {lvl} уровень')
            else:
                rsp.set_message(f'Игрока {name} нету в списке')

        elif (action in ['удалить', ]) and name:
            if players_indexes.get(name, None) is not None:
                del players[players_indexes[name]]
                del players_indexes[name]
                rsp.add_command({'type': 'update_data', 'action': {'players': players}})
                rsp.set_message(f'Игрок {name} удален')
            else:
                rsp.set_message(f'Игрока {name} нету в списке')

        elif ('уровень' in r.nlu.lemmas) and name:
            if players_indexes.get(name, None) is not None:
                rsp.set_message(f'У игрока {name} {players[players_indexes[name]]["level"]} уровень')
            else:
                rsp.set_message(f'Игрока {name} нету в списке')
        elif 'помощь' in r.nlu.lemmas:
            rsp.set_message('В этом приложении вы можете редактировать список игроков и менять их уровни')
        else:
            rsp.set_message('Я вас не понимаю. Скажите Помощь для справки')
        yield rsp


if __name__ == '__main__':
    uvicorn.run('app:app', reload=True, use_colors=True)
