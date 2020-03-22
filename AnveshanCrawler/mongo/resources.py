from mongo.mongodump import MongoPipeline
import json

class AnveshanResource(MongoPipeline):
    def __init__(self, db_name="AnveshanResource"):
        MongoPipeline.__init__(self, db_name)
        self.graphs = self.db["graphs"]
        self.links = self.db["links"]

    def save_graph(self, graph, links, name):
        # graph -> JSON #use nx.node_link_data()
        query = {name: {"$exists": "true"}}
        graph_result = self.graphs.find(query)
        link_result = self.links.find({"links": {"$exists": "true"}})
        if graph_result.count() == 0:
            insert_query = {name: json.dumps(graph)}
            self.graphs.insert_one(insert_query)
            self.links.insert_one({"links": links})

        else:
            for res in result:
                update_query = {"$set": {name: json.dumps(graph)}}
                self.graphs.update(
                    {'_id': res['_id']},
                    update_query
                )
            for link_res in link_result:
                update_query = {"$set": {"links": links}}
                self.links.update(
                    {'_id': link_res['_id']},
                    update_query
                )

    def load_graph(self, name):
        query = {name: {"$exists": "true"}}
        graph = self.graphs.find(query)
        for g in graph:
            json_graph = json.loads(g[name])
        query = {"links": {"$exists": "true"}}
        links = self.links.find(query)
        for l in links:
            link = l["links"]
        return json_graph, link
