import asyncio
import aiohttp
from typing import Dict, Union, List
from storage_db.storage_db import DbClient, Person
import requests
import sys


URL = 'https://www.swapi.tech/api/people/'
PG_DSN = 'postgresql://postgres:postgres@127.0.0.1:5431/netology'
db_client = DbClient(PG_DSN)
QUANTITY_PERSON = 82


async def get_person(person_id: int, session: aiohttp.ClientSession):
    response = await session.get(f'{URL}{person_id}')
    return await response.json()


def get_value_from_list(id: str, data: Dict):
    result = ''
    for url in data:
        response = requests.get(f'{url}{id}').json()
        response = response['name']
        result += f', {response}'
    return result


def get_name_planet(url: str):
    data = requests.get(url).json()
    return data['result']['properties']['name']


async def prepare_data_person(id: str, data_person: Dict[str, Union[str, List]]):
    birth_year = data_person['birth_year']
    eye_color = data_person['eye_color']
    gender = data_person['gender']
    hair_color = data_person['hair_color']
    height = data_person['height']
    homeworld = get_name_planet(data_person['homeworld'])
    mass = data_person['mass']
    name = data_person['name']
    skin_color = data_person['skin_color']
    # species = get_value_from_list(id, data_person['species'])
    # starships = get_value_from_list(id, data_person['starships'])
    # vehicles = get_value_from_list(id, data_person['vehicles'])

    data_for_db = Person(id=id, birth_year=birth_year, eye_color=eye_color, gender=gender, hair_color=hair_color,
                         height=height, homeworld=homeworld, mass=mass, name=name, skin_color=skin_color)

    return data_for_db


def clear_db():
    db_client.session.query(Person).delete(synchronize_session='fetch')
    db_client.session.commit()
    db_client.session.close()


async def main():
    session = aiohttp.ClientSession()
    coros = []
    for person_id in range(1, QUANTITY_PERSON + 1):
        if person_id == 17:  # видимо сбой в swapi, под id 17 нет персонажа
            continue
        couroutine = get_person(person_id, session)
        print(person_id)
        coros.append(couroutine)
    data = await asyncio.gather(*coros)
    await session.close()
    list_data_for_db = []
    for person_id, el in enumerate(data, start=1):
        data = prepare_data_person(el['result']['uid'], el['result']['properties'])
        list_data_for_db.append(data)
        print(f'person with id {person_id} successfully processed')
    db_client.session.add_all(list_data_for_db)
    db_client.session.commit()
    db_client.session.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
