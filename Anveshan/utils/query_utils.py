from mongo.query import AnveshanQueryManager
import re

query_manager = AnveshanQueryManager()


def log_query(query, name="default"):
	query_manager.add_query(query.query, name)

def get_query_recommendation(query, name="default"):
	recommendations = {}
	queries = query_manager.read_queries(name)
	for q in queries:
		pattern = "^" + query
		if(re.search(pattern, q)):
			if q not in recommendations:
				recommendations[q] = 1
			else:
				recommendations[q] += 1
	def sort(x):
		return recommendations[x]
	return sorted(recommendations.keys(), key=sort, reverse=True)

def frequent_search(name="default", no_of_results=5):
	query = dict()
	queries = query_manager.read_queries(name)
	print(queries)
	for q in queries:
		if q not in query:
			query[q] = 1
		else:
			query[q] += 1

	def sort(x):
		return query[x]
	sorted_query = sorted(query.keys(), key=sort, reverse=True)
	if len(sorted_query) > 5:
		sorted_query = sorted_query[:5]

	return sorted_query
	
