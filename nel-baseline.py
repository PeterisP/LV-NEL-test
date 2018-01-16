# Full-text search of entity alternate names within the corpus.
# No disambiguation

import csv, re, json
from collections import namedtuple
from trie import TrieSearch
from entitynames import fixName, orgAliases, personAliases
from InflectEntity import inflectEntity

Entity = namedtuple('Entity', ['name', 'uri', 'category', 'aliases', 'inflections'])
goodtypes = set(['http://schema.org/Place', 'http://schema.org/Person', 'http://schema.org/Organization'])

blacklist = ['Sana','Biksi','Alva','Roli','MakSim','Peru','Oša','Doha','Reģi','Vitol','Neptūns','Igo','MaNga','Barta','Notra','Deli','Lībe','Basi','Vore','Nove','Ozols','Tuma','Auri','Dons','Modo','Uda','Aģe','Pink','Sita','Auseklis','Čada','Viktorija','3. kilometrs','Paks','Meka','A-ha','Jūta','Meks','Nē','Ēre','Kalē','Gulag','Sīpoli','Modes','Dāvi','Monro','Lins','Aima','Rudus','Aksi','Rāvi','Anastasija','Nātre','Hama','Daka','Taurene','Zeme','Elka','v','bāka','Jums']
blacklist = ['Mūsu', 'Zemnieki', 'Vars', 'Vads', 'Tempa', 'Zāle', 'Kara', 'Joma', 'Gata', 'Sava', 'Terors']
blacklist = set(blacklist)

def prepare_entities(source, filename):
	with open(filename, 'w') as f:
		entities = load_dbpedia_entities(source)
		json.dump(list(entities), f, ensure_ascii=False, indent=2)	

def load_dbpedia_entities(filename):
	with open(filename) as entityfile:
		for line in entityfile:
			if line.startswith('#'):
				continue
			uri, _, instancetype = re.findall(r'<([^>]+)>', line)
			if instancetype not in goodtypes:
				continue
			name = uri.replace('http://lv.dbpedia.org/resource/','').replace('_',' ')
			if '(' in name or name in blacklist:
				continue
			category = ''
			if 'Person' in instancetype:
				category = 'person'
			elif 'Organization' in instancetype:
				category = 'org'
			elif 'Place' in instancetype:
				category = 'loc'

			aliases = list(get_inflection_aliases(name, category))
			entity = Entity(name, uri, instancetype, aliases, inflections)
			yield entity

def get_inflection_aliases(name, category):
	inflections = inflectEntity(name, category)
	aliases = set([name])
	for key, inflection in inflections.items():
		if key == 'Dzimte':
			continue
		if category == 'person':
			aliases.update(personAliases(inflection))
		elif category == 'org':
			aliases.update(orgAliases(inflection))
		else:
			aliases.add(inflection)			
	return aliases, inflections

def inflect_entities(entities):
	for entity in entities:
		aliases = set([entity.name])
		for alias in entity.aliases:
			new_aliases, inflections = get_inflection_aliases(alias, entity.category)
			aliases |= new_aliases
		new_entity = Entity(entity.name, entity.uri, entity.category, list(aliases), inflections)
		yield new_entity

def check_dbpedia_entities(entities, filename):
	entitydict = {}
	for entity in entities:
		if entity.name in entitydict:
			print(f'Duplicates:\n{entity}\n{entitydict.get(entity.name)}')
			break
		else:
			entitydict[entity.name] = entity
	with open(filename) as entityfile:
		for line in entityfile:
			if line.startswith('#'):
				continue
			uri, _, instancetype = re.findall(r'<([^>]+)>', line)
			name = uri.replace('http://lv.dbpedia.org/resource/','').replace('_',' ')
			if name not in entitydict:
				# print(f'Entity "{name}" missing')
				# break
				pass

entity_source = 'dbpedia/instance_types_transitive_lv.ttl'
# entity_filename = 'dbpedia/entities.json'
entity_filename_noinflect = 'wikidata/entities_noinflect.json'
entity_filename = 'wikidata/entities.json'
corpus_filename = 'corpus/speeches_reversed.csv'
output_filename = 'corpus/speeches_reversed_entities.csv'

# prepare_entities(entity_source, entity_filename)
def inflect_entity_file():
	with open(entity_filename_noinflect) as f:
		entities = [Entity._make(entity) for entity in json.load(f)]
		entities = inflect_entities(entities)
		with open(entity_filename, 'w') as f:
			json.dump(list(entities), f, ensure_ascii=False, indent=2)	
	print('Entities inflected..')

# inflect_entity_file()

with open(entity_filename) as f:
	entities = [Entity._make(entity) for entity in json.load(f)]

# check_entities(entities, entity_filename)
entity_names = [name for entity in entities for name in entity.aliases]
entities_by_name = {name : entity for entity in entities for name in entity.aliases}
seen_entities = set()
trie = TrieSearch(entity_names, splitter='')

print('processing corpus....')
with open(corpus_filename) as corpusfile:
	with open(output_filename, 'w', newline='') as outfile:
		corpusreader = csv.reader(corpusfile)
		outwriter = csv.writer(outfile)
		next(corpusreader)
		outwriter.writerow(['type', 'source', 'session_name', 'session_type', 'date', 'id', 'speaker', 'category', 'subcategory', 'role', 'sequence', 'text', 'entities'])
		for row in corpusreader:
			text = row[11]
			text = text.replace('\n',' ')
			text = fixName(text)

			mentions = []
			for pattern, start_idx in trie.search_all_patterns(text):
				if start_idx+len(pattern)<len(text) and text[(start_idx+len(pattern))].isalpha(): # ja nākamais simbols aiz vārda ir burts, tad izlaižam - lai nav vārdu daļas.
					continue
				if pattern in blacklist:
					continue
				entity = entities_by_name.get(pattern)
				if entity.name in blacklist:
					continue
				if entity.category == 'person' and ' ' not in entity.name:
					continue
				seen_entities.add(entity.name)
				mentions.append( (pattern, entity.name, start_idx, entity.uri, entity.category) )
			row.append(json.dumps(mentions, ensure_ascii=False))
			outwriter.writerow(row)

with open('seen_entities.txt', 'w') as f:
	for name in seen_entities:
		entity = entities_by_name.get(name)
		if entity:
			f.write(f'{entity.category} {entity.name}\n')
		else:
			f.write(f'{name}\n')

print('Done')