#!/usr/bin/python
# -*- coding: utf-8 -*-

# Full-text search of entity alternate names within the corpus.
# No disambiguation

from nel_baseline import load_entity_data, do_nel
from bottle import route, request, response, run, static_file
from json import dumps

@route('/', method=['GET', 'POST'])
@route('/index.html', method=['GET', 'POST'])
def root():
	text = ''
	if request.query.get('query'):
		text = request.query.get('query')
	else:
		text = request.body.read()
	if text:
		mentions = do_nel(trie, entities_by_name, text)
		print(mentions)
		print(type(mentions))
		response.content_type = 'application/json'
		return dumps(mentions)
	else:
		return static_file('index.html', root='web')		

entity_filename = 'wikidata/entities.json'
trie, entities_by_name = load_entity_data(entity_filename)
run(host='localhost', port=8080, debug=True)
