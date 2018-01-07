# Full-text search of entity alternate names within the corpus.
# No disambiguation

import csv, re, json
from collections import namedtuple
from trie import TrieSearch
from entitynames import fixName, orgAliases, personAliases
from InflectEntity import inflectEntity

Entity = namedtuple('Entity', ['name', 'uri', 'type', 'aliases', 'inflections'])
goodtypes = set(['http://schema.org/Place', 'http://schema.org/Person', 'http://schema.org/Organization'])

blacklist = ['Sana','Biksi','Alva','Roli','MakSim','Peru','Oša','Doha','Reģi','Vitol','Neptūns','Igo','MaNga','Barta','Notra','Deli','Lībe','Basi','Vore','Nove','Ozols','Tuma','Auri','Dons','Modo','Uda','Aģe','Pink','Sita','Auseklis','Čada','Viktorija','3. kilometrs','Paks','Meka','A-ha','Jūta','Meks','Nē','Ēre','Kalē','Gulag','Sīpoli','Modes','Dāvi','Monro','Lins','Aima','Rudus','Aksi','Rāvi','Anastasija','Nātre','Hama','Daka','Taurene','Zeme','Elka']
blacklist = set(blacklist)

def prepare_entities(source, filename):
	with open(filename, 'w') as f:
		entities = load_entities(source)
		json.dump(list(entities), f, ensure_ascii=False, indent=2)	

def load_entities(filename):
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
			inflections = inflectEntity(name, category)
			aliases = set(name)
			for key, inflection in inflections.items():
				if key == 'Dzimte':
					continue
				if 'Person' in instancetype:				
					aliases.update(personAliases(inflection))
				elif 'Organization' in instancetype:
					aliases.update(orgAliases(inflection))
				else:
					aliases.add(inflection)			
			aliases = list(aliases)
			entity = Entity(name, uri, instancetype, aliases, inflections)
			yield entity

def check_entities(entities, filename):
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
entity_filename = 'dbpedia/entities.json'
corpus_filename = 'corpus/speeches_reversed.csv'
output_filename = 'corpus/speeches_reversed_entities.csv'

# prepare_entities(entity_source, entity_filename)
with open(entity_filename) as f:
	entities = [Entity._make(entity) for entity in json.load(f)]

# check_entities(entities, entity_filename)
entity_names = [name for entity in entities for name in entity.aliases]
entities_by_name = {name : entity for entity in entities for name in entity.aliases}
seen_entities = set()
trie = TrieSearch(entity_names, splitter='')

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
				entity = entities_by_name.get(pattern)
				seen_entities.add(entity.name)
				mentions.append( (pattern, entity.name, start_idx, entity.uri, entity.type) )
			if mentions:
				row.append(str(mentions))
			outwriter.writerow(row)

with open('seen_entities.txt', 'w') as f:
	for name in seen_entities:
		entity = entities_by_name.get(name)
		if entity:
			f.write(f'{entity.type} {entity.name}\n')
		else:
			f.write(f'{name}\n')