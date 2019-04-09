#Python module for converting showdown exports to dict made by Che5hire (Che5hire#4179 on Discord)
#This is licenced under GNU GENERAL PUBLIC LICENSE 3.0, a copy of this licence must be provided if you redistribute this code, do not delete these comments.
class showdownFormatError(Exception):
	def __init__(self, message):
		self.errors = message
def showdown2dict(showdown):
	"""Takes a showdown export (datatype str) and converts it to the dict datatype. This is for full backups with multiple teams."""
	returndict = {}
	linespassed = 0
	teamName = None
	tierName = ''
	pokemondict = None
	for line in showdown.splitlines():
		if line.startswith('#'):
			pass
		elif linespassed + 1 >= len(showdown.splitlines()):
			if returndict == {}:
				raise showdownFormatError('Could not find any teams.')
			return returndict
		elif line.startswith('===') and line.startswith('==='):#Team titles are formatted '=== [tierName] teamName(may contain spaces) ==='
			tierName = line[(line.find(' [') + 2) : (line.find('] '))]
			teamName = line[(line.find('] ')+2) : (line.find(' ==='))].strip()
			
			pokemonStr = ''
			for pokeline in showdown.splitlines()[linespassed + 2:]:
				if pokeline.strip().startswith("===") and pokeline.strip().endswith("==="):
					break
				pokemonStr += pokeline + '\n'
			print(">>>" + pokemonStr + "<<<")
			returndict.update({teamName:{'tier':tierName, 'pokemon':pokemon2list(pokemonStr)}})
		linespassed += 1
	else:		
		if returndict == {}:
			raise showdownToolsFormatError('Could not find any teams.')
		return returndict
def pokemon2list(showdown):
	'''Returns a list of pokemon in the showdown export you enter, intended for teams or singular pokemon. Pokemon are dict datatype.'''
	showdown = showdown.splitlines()
	listPokemon = []
	linespassed = 0
	for line in showdown:
		if line.find(' @ ') != -1:
			pokemongender = None#None == Random/Genderless, True == Male, False == Female. 'sex' would be faster to type but they call it 'gender' in-game so to avoid confusion, that's what I'm doing.
			if line.find('(F) @') != -1:
				line = line.replace('(F) @', ' @')
				pokemongender = False
			elif line.find('(M) @') != -1:
				line = line.replace('(F) @', ' @')
				pokemongender = True
			if line.find(' (') != -1:
				pokemon = line[(line.find(' (')+2):line.find(') @')].strip()
			else:
				pokemon = line[0:(line.find(' @'))].strip()
			if line.find(' (') != -1:
				nickname = line[0:(line.find(' ('))].strip()
			else:
				nickname = ''
			pokemondict = {'pokemon': pokemon, 'nickname': nickname, 'gender': pokemongender, 'shiny':False, 'moves': [], 'nature':'serious', 'item': (line[(line.find(' @ ')+2):].strip())}#The shiny value may be marked true later. 'Serious' is the default nature on most tools
			_linespassespoke = 0
			_nature = ''
			_moves = []#This allows more than 4 moves as some custom metagames may allow additional moves but this is usually 4 or less in standard metagames.
			#The order of which stat is which is the same as it is in-game and on showdown from top to bottom: HP,Atk,Def,SpA,SpD,Spe.
			evs = [0,0,0,0,0,0]
			ivs = [31,31,31,31,31,31] #IVS are assumed to be max unless otherwise stated in showdown exports.
		elif line.strip().endswith('Nature'):
			pokemondict['nature'] = line.split(' ')[0]
		elif line.startswith('-'):
			pokemondict['moves'].append(line[1:].strip())
		elif line.startswith('Shiny:'):#This will block this from catching in the 'catch all' if statement.
			if line.lower().find('yes') == -1:
				pokemondict['shiny'] = True#No need to code the other condition, it's False by default if the Shiny: No is there or not.
		elif line.lower().startswith('ivs:'):
			_ivvalues = line.lower().replace('ivs:', '').strip().split(' / ')
			for iv in _ivvalues:
				iv = iv.split(' ')
				_ivpos = ['hp','atk','def','spa','spd','spe']#Way faster to just map another list than adding a bunch of if statements.
				_ivpos = _ivpos.index(iv[1].lower())
				try:
					ivs[_ivpos] = int(iv[0])
				except ValueError:
					raise showdownFormatError('IVs must be int')
			pokemondict['ivs']=ivs
		elif line.lower().startswith('evs:'):
			_evvalues = line.lower().replace('evs:', '').strip().split(' / ')
			for ev in _evvalues:
				ev = ev.split(' ')
				_evpos = ['hp','atk','def','spa','spd','spe']
				_evpos = _evpos.index(ev[1].lower())
				try:
					evs[_evpos] = int(ev[0])
				except ValueError:
					raise showdownFormatError('EVs must be int')

			pokemondict['evs'] = evs
		elif line.find(':') != -1:#Catch all for other things I'm too lazy to code, like happiness.
			_value = line[(line.find(':')+1):].strip()
			_key = line[:line.find(':')]
			if _value.isdigit():
				_value = int(_value)
			pokemondict[_key] = _value
		elif len(line) == 0:
			if len(listPokemon) >> 0:	
				if len(listPokemon) != 6 and pokemondict != listPokemon[-1]:# This is a temporary fix as this will cause issues on the rare occasion that a team is from a meta that allows more than 6 pokemon and that two pokemon on that team are exactly the same.
					listPokemon += [pokemondict]
				else:
					return listPokemon
			else:
				listPokemon += [pokemondict]
		linespassed += 1
	else:
		return listPokemon
def list2pokemon(listOfPokemon: list):
	'''Turns a list of pokemon dicts into a showdown import/export. Returns a string.'''
	pokemonString = ''
	for pokemon in listOfPokemon:
		gender = {True:' (M) ', False: ' (F) ', None: ''}
		_pokemonname = pokemon['pokemon']
		_pokemonitem = ''
		if pokemon.get('nickname', '') != '':
			_pokemonname = ' (' + pokemon['pokemon'] + ') '
		if pokemon.get('item') != None:
			_pokemonitem = ' @ ' + pokemon['item']
		pokemonString += ''.join([pokemon.get('nickname', ''), _pokemonname, gender.get(pokemon.get('gender', ''), ''), _pokemonitem]).replace('  ', ' ') + '\n'
		pokemonString += 'Ability: ' + pokemon['Ability'] + ' \n'
		pokemonString += 'EVs: {p[0]} HP / {p[1]} Atk / {p[2]} Def / {p[3]} SpA / {p[4]} SpD / {p[5]} Spe \n'.format(p=pokemon.get('evs', [0,0,0,0,0,0]))
		pokemonString += pokemon['nature'] + ' Nature \n'
		pokemonString += 'IVs: {p[0]} HP / {p[1]} Atk / {p[2]} Def / {p[3]} SpA / {p[4]} SpD / {p[5]} Spe \n'.format(p=pokemon.get('ivs', [31,31,31,31,31,31]))
		for move in pokemon['moves']:
			pokemonString += '- {}'.format(move) + ' \n'
		if pokemon['shiny'] == True:
			pokemonString += 'Shiny: Yes'
		pokemonString += '\n'
	return pokemonString

def dict2showdown(dictOfTeams: dict):
	'''Turns a dict into a full showdown backup. Returns str'''
	showdownBackup = ''
	for team in dictOfTeams.items():
		teamName = ''
		tier = ''
		pokemon = ''
		showdownBackup += "===[{}] {} ===\n\n".format(team[1].get('tier', 'gen7'), team[0])
		showdownBackup += list2pokemon(team[1]['pokemon']) + "\n"
	return showdownBackup
