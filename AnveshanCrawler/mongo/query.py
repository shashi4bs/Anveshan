from mongo.resources import AnveshanResource

class AnveshanQueryManager(AnveshanResource):
	def __init__(self):
		AnveshanResource.__init__(self)
		self.query = self.db["query"]


	def add_query(self, query, name="default"):
		try:
			q = {"name": name}
			result = self.query.find(q)
			count = result.count()
			if count == 0:
				insert_query = {"name": name, \
				"query": [query]
				}
				self.query.insert(insert_query)
			else:
				update_query = {"query": query}

				for r in result:
					self.query.update(
						{'_id' : r['_id']},
						{'$push' : update_query}
					)
			print("Saved: {}".format(query))
		except Exception as e:
			print(e)

	def read_queries(self, name="default"):
		
		try:
			q = {"name" : name}
			result = self.query.find_one(q)
			#print(result)
			return result['query']
		except Exception as e:
			print(e)
			print("Query Read Failed")
			
		
