# Wikidata dump import
# Taken from experimental wikidata exports at http://78.46.100.7/wikidata/20180101/ , not the full (large) wikidata dump
import re, json
from collections import namedtuple

wikidata_folder = 'D:\Robertraksts\\'
wikidata_folder = '../'
instancetype_filename = 'wikidatawiki-20180101-instance-types-transitive.ttl'
labels_filename = 'wikidatawiki-20180101-labels.ttl'
goodtypes = set(['http://schema.org/Place', 'http://schema.org/Person', 'http://schema.org/Organization'])

def load_wikidata_types(filename):
	entity_types = {}
	with open(filename) as entityfile:
		for line in entityfile:
			if line.startswith('#'):
				continue
			uri, _, instancetype = re.findall(r'<([^>]+)>', line)
			if instancetype not in goodtypes:
				continue
			assert uri.startswith('http://wikidata.dbpedia.org/resource/Q')
			entity_id = uri[37:]		

			category = ''
			if 'Person' in instancetype:
				category = 'person'
			elif 'Organization' in instancetype:
				category = 'org'
			elif 'Place' in instancetype:
				category = 'loc'

			entity_types[entity_id] = category
	return entity_types

Entity = namedtuple('Entity', ['name', 'uri', 'type', 'aliases', 'inflections'])

def load_wikidata_entities(filename, entity_types):
	entities = {}
	with open(filename, encoding='utf-8') as entityfile:
		for line in entityfile:
			if line.startswith('#'):
				continue
			match = re.match(r'<([^>]+)> <[^>]+> "(.+)"@lv .', line)
			if not match:
				continue
			uri = match.group(1)
			label = match.group(2)

			assert uri.startswith('http://wikidata.dbpedia.org/resource/Q')
			entity_id = uri[37:]

			category = entity_types.get(entity_id)
			if category == None:
				continue

			entity = entities.get(entity_id)
			if entity == None:
				entity = Entity(label, uri, category, [label], None)
			else:
				entity.aliases.append(label)
				print(entity)
			entities[entity_id] = entity
	return entities.values()

def inflect_entities(entities):
	for entity in entities:				
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
	return entities

entity_types = load_wikidata_types(wikidata_folder+instancetype_filename)
with open('wikidata/entities_noinflect.json', 'w') as f:
	entities = load_wikidata_entities(wikidata_folder+labels_filename, entity_types)
	json.dump(list(entities), f, ensure_ascii=False, indent=2)	



print('Done!')
