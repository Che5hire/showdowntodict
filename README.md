Generates a dict based off of showdown import text.

dicts generated using *showdown2dict* will be in following format:
>{teamName: {tier: tier, pokemon: [listofpokemon]}}

The list of pokemon should have dicts in it that have the following format:
>{'nickname': (nickname of pokemon or None), 'pokemon': (including forme so 'pokemon-forme'), 'moves': [move1,move2,move3,move4], 'item': item, ivs:{'stat':iv} 'evs':{stat:evs(int)}}

If you're converting a single team or a pokemon use pokemon2list, it will return a list of pokemon with the format above instead of a dict.

This library is in pre-alpha and is most likely not accurate/functional.