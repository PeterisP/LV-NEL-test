# Wikidata dump import
# Taken from experimental wikidata exports at http://78.46.100.7/wikidata/20180101/ , not the full (large) wikidata dump
import re

wikidata_folder = 'D:\Robertraksts\\'
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
			break
	return entity_types

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
			print(entity_id, label, category)
			break




entity_types = load_wikidata_types(wikidata_folder+'wikidatawiki-20180101-instance-types-transitive.ttl')
print(list(entity_types.keys())[0])
entities = load_wikidata_entities(wikidata_folder+'wikidatawiki-20171220-labels.ttl', entity_types)


print('Done!')
