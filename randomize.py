import os
import random
import io
import zipfile
import json
import sys

def namedesc(seed):
	nameprefix = 'randomizer'
	descprefix = 'Data Randomizer'
	if seed == 'r':
		return nameprefix, descprefix
	else:
		return nameprefix+'_{}'.format(seed), descprefix+', Seed: {}'.format(seed)

print("  __  __  ___   ___              _     \n |  \/  |/ __| | _ \__ _ _ _  __| |___ \n | |\/| | (__  |   / _` | ' \/ _` / _ \\\n |_|  |_|\___| |_|_\__,_|_||_\__,_\___/\n")

if len(sys.argv) >= 2:
	print('[i] Using settings provided in arguments.')

	if str(sys.argv[1]) == 'r':
		datapack_name, datapack_desc = namedesc('r')
	else:
		try:
			seed = int(sys.argv[1])
		except:
			print('[!] Failed to convert seed into an integer.')
			exit()
		datapack_name, datapack_desc = namedesc(seed)
		random.seed(seed)

	if 'advancements' in sys.argv:
		use_adv = True
	else:
		use_adv = False

	if 'loot_tables' in sys.argv or 'loot' in sys.argv:
		use_loo = True
	else:
		use_loo = False

	if 'recipes' in sys.argv:
		use_rec = True
	else:
		use_rec = False

else:
	while True:
		seed_input = input('[i] Please input a seed. An empty string will result in a random seed.\n> ')
		if seed_input != '':
			try:
				seed = int(seed_input)
			except:
				print('[!] Failed to convert input into an integer.\n')
				continue
			datapack_name, datapack_desc = namedesc(seed)
			random.seed(seed)
			break
		else:
			datapack_name, datapack_desc = namedesc('r')
			break

	qtext = '\n[?] Should {} be randomized? (y/n)\n> '
	qinvalid = '[!] Invalid input, defaulting to false.'

	loo_input = input(qtext.format('loot tables'))
	if loo_input == 'y':
		use_loo = True
	elif loo_input == 'n':
		use_loo = False
	else:
		print(qinvalid)
		use_loo = False

	adv_input = input(qtext.format('advancements [BETA]'))
	if adv_input == 'y':
		use_adv = True
	elif adv_input == 'n':
		use_adv = False
	else:
		print(qinvalid)
		use_adv = False

	rec_input = input(qtext.format('recipes [BETA]'))
	if rec_input == 'y':
		use_rec = True
	elif rec_input == 'n':
		use_rec = False
	else:
		print(qinvalid)
		use_rec = False

datapack_filename = datapack_name + '.zip'

print('\n[i] Generating datapack...')

def randomize(path):
	file_list = []
	remaining = []

	for dirpath, dirnames, filenames in os.walk(path):
		for filename in filenames:
			if path == 'advancements' and 'recipes' in os.path.join(dirpath, filename):
				continue
			file_list.append(os.path.join(dirpath, filename))
			remaining.append(os.path.join(dirpath, filename))

	file_dict = {}

	for file in file_list:
		i = random.randint(0, len(remaining)-1)
		file_dict[file] = remaining[i]
		del remaining[i]

	return file_dict

zipbytes = io.BytesIO()
zip = zipfile.ZipFile(zipbytes, 'w', zipfile.ZIP_DEFLATED, False)

if use_adv == True:
	file_dict = randomize('advancements')
	for from_file in file_dict:
		with open(from_file) as file:
			contents = file.read()
		zip.writestr(os.path.join('data/minecraft/', file_dict[from_file]), contents)

if use_loo == True:
	file_dict = randomize('loot_tables')
	for from_file in file_dict:
		with open(from_file) as file:
			contents = file.read()
		zip.writestr(os.path.join('data/minecraft/', file_dict[from_file]), contents)

if use_rec == True:
	file_dict = randomize('recipes')
	for from_file in file_dict:
		with open(from_file) as file:
			contents = file.read()
		zip.writestr(os.path.join('data/minecraft/', file_dict[from_file]), contents)

zip.writestr('pack.mcmeta', json.dumps({'pack':{'pack_format':1, 'description':datapack_desc}}, indent=4))
zip.writestr('data/minecraft/tags/functions/load.json', json.dumps({'values':['{}:reset'.format(datapack_name)]}))
zip.writestr('data/{}/functions/reset.mcfunction'.format(datapack_name), 'tellraw @a ["",{"text":"Minecraft Data Randomizer","color":"green"}]')

zip.close()
with open(datapack_filename, 'wb') as file:
	file.write(zipbytes.getvalue())

print('[i] Created datapack "{}"'.format(datapack_filename))
