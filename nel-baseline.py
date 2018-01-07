# Full-text search of entity alternate names within the corpus.
# No disambiguation

import csv, re
from collections import namedtuple
from trie import TrieSearch

Entity = namedtuple('Entity', ['name', 'uri', 'type'])
goodtypes = set(['http://schema.org/Place', 'http://schema.org/Person', 'http://schema.org/Organization'])

def load_entities(filename):
	with open(filename) as entityfile:
		for line in entityfile:
			if line.startswith('#'):
				continue
			uri, _, instancetype = re.findall(r'<([^>]+)>', line)
			if instancetype not in goodtypes:
				continue
			name = uri.replace('http://lv.dbpedia.org/resource/','').replace('_',' ')
			entity = Entity(name, uri, instancetype)
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


entity_filename = 'dbpedia/instance_types_transitive_lv.ttl'
corpus_filename = 'corpus/speeches_reversed.csv'
output_filename = 'corpus/speeches_reversed_entities.csv'

entities = list(load_entities(entity_filename))
# check_entities(entities, entity_filename)
entity_names = [entity.name for entity in entities]
entities_by_name = {entity.name : entity for entity in entities}
trie = TrieSearch(entity_names, splitter='')
# trie = TrieSearch(['Paldies.', 'A.Kaimiņš', 'P'], splitter='')


with open(corpus_filename) as corpusfile:
	with open(output_filename, 'w', newline='') as outfile:
		corpusreader = csv.reader(corpusfile)
		outwriter = csv.writer(outfile)
		next(corpusreader)
		outwriter.writerow(['type', 'source', 'session_name', 'session_type', 'date', 'id', 'speaker', 'category', 'subcategory', 'role', 'sequence', 'text', 'entities'])
		for row in corpusreader:
			text = row[11]
			text = text.replace('\n',' ')
			mentions = []
			for pattern, start_idx in trie.search_all_patterns(text):
				entity = entities_by_name.get(pattern)
				mentions.append( (pattern, entity.name, start_idx, entity.uri) )
			if mentions:
				row.append(str(mentions))
			outwriter.writerow(row)
			if mentions:
				print(row)
				print(text)
				print(mentions)
				break

	# return  text form, base form, offset, knowledge base id

