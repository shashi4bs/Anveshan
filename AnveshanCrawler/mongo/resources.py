from mongo.mongodump import MongoPipeline
import json

class AnveshanResource(MongoPipeline):
    def __init__(self, db_name="AnveshanResource"):
        MongoPipeline.__init__(self, db_name)
        self.graphs = self.db["graphs"]
        self.links = self.db["links"]
        self.p_vector = self.db["p_vector"]

    def save_graph(self, graph, links, name):
        # graph -> JSON #use nx.node_link_data()
        query = {name: {"$exists": "true"}}
        graph_result = self.graphs.find(query)
        link_result = self.links.find({name: {"$exists": "true"}})
        print("in save graph", graph_result.count(), link_result.count())
        if graph_result.count() == 0:
            insert_query = {name: json.dumps(graph)}
            self.graphs.insert(insert_query)
            self.links.insert({name: links})

        else:
            for res in graph_result:
                update_query = {"$set": {name: json.dumps(graph)}}
                self.graphs.update(
                    {'_id': res['_id']},
                    update_query
                )
            
            print('saving link test')

            for link_res in link_result:
                update_query = {"$set": {name: links}}
                self.links.update(
                    {'_id': link_res['_id']},
                    update_query
                )

    def load_graph(self, name):
        query = {name: {"$exists": "true"}}
        graph = self.graphs.find(query)
        print('graph', graph.count())
        json_graph = None
        link = None
        for g in graph:
            json_graph = json.loads(g[name])
        query = {name: {"$exists": "true"}}
        links = self.links.find(query)
        print(links.count())
        for l in links:
            link = l[name]
        return json_graph, link

    def load_pvector(self, name):
        query = {name : {"$exists": "true"}}
        p_vec = self.p_vector.find(query)
        for p in p_vec:
            return json.loads(p[name])

    def save_pvector(self, p_vec, name):
        query = {name : {"$exists" : "true"}}
        result = self.p_vector.find(query)
        if(result.count() == 0):
            insert_query = {name : json.dumps(p_vec)}
            self.p_vector.save(insert_query)
        else:
            for r in result:
                update_query = {'$set' : {name: json.dumps(p_vec)}}
                self.p_vector.update(
                    {'_id' : r['_id']},
                    update_query
                )
        return
