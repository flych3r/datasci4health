import itertools
import re
from collections import Counter
from pathlib import Path

import bs4
import requests
import pandas as pd
from tqdm.auto import tqdm


def read_script_from_url(url: str) -> bs4.element.Tag:
    html_text = requests.get(url).text
    soup = bs4.BeautifulSoup(html_text, "html.parser")
    try:
        script = soup.find_all("pre")[0]
    except IndexError:
        script = soup.find_all("td", {"class": "scrtext"})[0]
    return script


def split_scenes(script: str) -> list[str]:
    scenes = re.split("<b>[ 0-9]*(INT.|EXT.)", script)
    return scenes[::2]


def extract_entities_from_scenes(scenes: list[str]) -> list[list[str]]:
    scene_entities = map(
        lambda x: re.findall(
            "<b>(.*)(\n?)<\/b>|([/A-Z0-9 -]+ *:)|(Artoo-Detoo)||(Artoo)|(Chewbacca)|(Chewie)",
            x,
        ),
        scenes,
    )
    scene_entities = filter(lambda x: x != [], scene_entities)
    scene_entities = map(
        lambda x: [
            list(
                filter(
                    lambda x: x != "",
                    map(lambda x: x.removesuffix(":").strip().upper(), c),
                )
            )
            for c in x
        ],
        scene_entities,
    )
    scene_entities = map(lambda x: list(itertools.chain(*x)), scene_entities)
    return list(scene_entities)


def extract_characters_in_scene(scene_entities: list[list[str]]) -> list[set[str]]:
    scene_interacting_characters = map(
        lambda x: [
            episode_alias[name] if name in episode_alias else name for name in x
        ],
        scene_entities,
    )
    scene_interacting_characters = map(
        lambda x: list(filter(lambda y: y in characters, x)),
        scene_interacting_characters,
    )
    scene_interacting_characters = map(set, scene_interacting_characters)
    scene_interacting_characters = filter(
        lambda x: len(x) > 1, scene_interacting_characters
    )
    return list(scene_interacting_characters)


def extract_characters_in_scene(scene_entities: list[list[str]]) -> list[set[str]]:
    scene_interacting_characters = map(
        lambda x: [
            episode_alias[name] if name in episode_alias else name for name in x
        ],
        scene_entities,
    )
    scene_interacting_characters = map(
        lambda x: list(filter(lambda y: y in characters, x)),
        scene_interacting_characters,
    )
    scene_interacting_characters = map(set, scene_interacting_characters)
    scene_interacting_characters = filter(
        lambda x: len(x) > 1, scene_interacting_characters
    )
    return list(scene_interacting_characters)


def create_scene_interactions(
    scene_interacting_characters: list[set[str]],
) -> list[tuple[str, str]]:
    scene_interactions = map(
        lambda x: list(itertools.combinations(x, 2)), scene_interacting_characters
    )
    scene_interactions =  list(itertools.chain(*scene_interactions))
    return [tuple(list(k) + [v]) for k, v in Counter(scene_interactions).items()]


if __name__ == '__main__':
    star_wars_scripts = {
        "Episode 1": "https://imsdb.com/scripts/Star-Wars-The-Phantom-Menace.html",
        "Episode 2": "https://imsdb.com/scripts/Star-Wars-Attack-of-the-Clones.html",
        "Episode 3": "https://imsdb.com/scripts/Star-Wars-Revenge-of-the-Sith.html",
        "Episode 4": "https://imsdb.com/scripts/Star-Wars-A-New-Hope.html",
        "Episode 5": "https://imsdb.com/scripts/Star-Wars-The-Empire-Strikes-Back.html",
        "Episode 6": "https://imsdb.com/scripts/Star-Wars-Return-of-the-Jedi.html",
        "Episode 7": "https://imsdb.com/scripts/Star-Wars-The-Force-Awakens.html",
    }

    data_path = Path('../data/')
    aliases = pd.read_csv(data_path / 'external' / 'aliases.csv')
    with open(data_path / 'external' / "characters.txt") as f:
        characters = [c.strip() for c in f.readlines()]


    all_episodes = []
    for episode in tqdm(star_wars_scripts.keys()):
        script_url = star_wars_scripts[episode]

        episode_alias = aliases[aliases[episode] == 1][["Alias", "Name"]]
        episode_alias = {r["Alias"]: r["Name"] for _, r in episode_alias.iterrows()}

        script = read_script_from_url(script_url)
        scenes = split_scenes(str(script))
        scene_entities = extract_entities_from_scenes(scenes)
        scene_interacting_characters = extract_characters_in_scene(scene_entities)
        scene_interactions = create_scene_interactions(scene_interacting_characters)
        scene_interactions = pd.DataFrame(
            scene_interactions, columns=["source", "target", "interactions"]
        )
        scene_interactions['movie'] = episode

        csv_name =  f'{episode.lower().replace(" ", "-")}-interactions.csv'
        scene_interactions.to_csv(data_path / 'processed' / csv_name, index=False)
        all_episodes.append(csv_name)


    all_episodes = pd.concat([
        pd.read_csv(data_path / 'processed' / csv_name) for csv_name in all_episodes
    ])
    all_episodes.to_csv(data_path / 'processed' / 'episodes-interactions.csv', index=False)
