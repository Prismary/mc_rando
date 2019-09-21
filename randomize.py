import os
import random
import io
import zipfile
import json
import sys

print("  __  __  ___   ___              _     \n |  \/  |/ __| | _ \__ _ _ _  __| |___ \n | |\/| | (__  |   / _` | ' \/ _` / _ \\\n |_|  |_|\___| |_|_\__,_|_||_\__,_\___/\n")

if len(sys.argv) >= 2:
	if str(sys.argv[1]) == 'r':
		datapack_name = 'random_loot'
		datapack_desc = 'Loot Table Randomizer'
	else:
		print('[i] Using seed provided in arguments.')
		try:
			seed = int(sys.argv[1])
		except:
			print('[!] Failed to convert input into an integer.')
			exit()
		datapack_name = 'random_loot_{}'.format(seed)
		datapack_desc = 'Loot Table Randomizer, Seed: {}'.format(seed)
		random.seed(seed)
else:
	while True:
		seed_input = input('[i] Please input a seed. An empty string will result in a random seed.\n> ')
		if seed_input != '':
			try:
				seed = int(seed_input)
			except:
				print('[!] Failed to convert input into an integer.\n')
				continue
			datapack_name = 'random_loot_{}'.format(seed)
			datapack_desc = 'Loot Table Randomizer, Seed: {}'.format(seed)
			random.seed(seed)
			break
		else:
			datapack_name = 'random_loot'
			datapack_desc = 'Loot Table Randomizer'
			break

datapack_filename = datapack_name + '.zip'

print('[i] Generating datapack...')

file_list = []
remaining = []

for dirpath, dirnames, filenames in os.walk('loot_tables'):
	for filename in filenames:
		file_list.append(os.path.join(dirpath, filename))
		remaining.append(os.path.join(dirpath, filename))

file_dict = {}

for file in file_list:
	i = random.randint(0, len(remaining)-1)
	file_dict[file] = remaining[i]
	del remaining[i]

zipbytes = io.BytesIO()
zip = zipfile.ZipFile(zipbytes, 'w', zipfile.ZIP_DEFLATED, False)

for from_file in file_dict:
	with open(from_file) as file:
		contents = file.read()

	zip.writestr(os.path.join('data/minecraft/', file_dict[from_file]), contents)

zip.writestr('pack.mcmeta', json.dumps({'pack':{'pack_format':1, 'description':datapack_desc}}, indent=4))
zip.writestr('data/minecraft/tags/functions/load.json', json.dumps({'values':['{}:reset'.format(datapack_name)]}))
zip.writestr('data/{}/functions/reset.mcfunction'.format(datapack_name), 'tellraw @a ["",{"text":"Item Drop Randomizer","color":"green"}]')

zip.close()
with open(datapack_filename, 'wb') as file:
	file.write(zipbytes.getvalue())

print('[i] Created datapack "{}"'.format(datapack_filename))
