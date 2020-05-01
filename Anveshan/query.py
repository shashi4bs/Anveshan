from autocorrect import Speller
from nltk.corpus import wordnet
from text_normalizer import Tokenizer

spell = Speller(lang="en")
tokenizer = Tokenizer()

special_chars = ['-', '_', '#', '@', '&']

def replace_with_spaces(query):
    for s in special_chars:
        query = query.replace(s, ' ')
    return query

class Query(object):
	def __init__(self, query):
		self.query = replace_with_spaces(query)
		self.do_you_mean = False
		self._autocorrect()
		self.tokens = tokenizer.processItem(self.query)
		self._get_synonyms()
		self.true_tokens, self.token_weights = self._combine_all_tokens()

	def _autocorrect(self):
		self.true_query = spell(self.query)
		if self.true_query != self.query:
			self.do_you_mean = True

	def _get_synonyms(self):
		self.synonyms = []
		self.syn_tokens = []
		for token in self.tokens:
			for syn in wordnet.synsets(token):
				for l in syn.lemmas():
					if l.name() not in self.synonyms:
						self.synonyms.append(l.name())
						synonym = replace_with_spaces(l.name())
						self.syn_tokens.append(tokenizer.processItem(synonym)) 

	def _combine_all_tokens(self):
		#combine tokens and syn_tokens
		final_tokens = dict()
		token_weight = dict()
		#if self.do_you_mean:
		#	tokens = tokenizer.processItem(self.query)
		#	for token in tokens:
		#		final_tokens[token] = tokens[token]
		
		for token in self.tokens:
			if token not in final_tokens:
				final_tokens[token] = self.tokens[token]
				token_weight[token] = 1
	
		for token_dict in self.syn_tokens:
			for token in token_dict:
				if token not in final_tokens:
					final_tokens[token] = token_dict[token]
					token_weight[token] = 0.8

		return final_tokens, token_weight
	
	def __repr__(self):
		return "Query : {}, TrueQuery: {}, Tokens: {}, TokenWeight: {}"\
		.format(self.query, self.true_query, self.true_tokens, self.token_weights)
