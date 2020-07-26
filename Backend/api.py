try:
    from flask import app,Flask
    from flask_restful import Resource, Api, reqparse
    import elasticsearch
    from elasticsearch import Elasticsearch
    import datetime
    import concurrent.futures
    import requests
    import json
except Exception as e:
    print("Modules Missing {}".format(e))


app = Flask(__name__)
api = Api(app)

#------------------------------------------------------------------------------------------------------------

NODE_NAME = 'myelkfirst'
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

#------------------------------------------------------------------------------------------------------------


"""
{
"wildcard": {
    "title": {
        "value": "{}*".format(self.query)
    }
}
}

"""


class Controller(Resource):
    def __init__(self):
        self.query = parser.parse_args().get("query", None)
        self.baseQuery ={
            "_source": [],
            "size": 0,
            "min_score": 0.5,
            "query": {
                "bool": {
                    "must": [
                        {
                            "match_phrase_prefix": {
                                "title": {
                                    "query": "{}".format(self.query)
                                }
                            }
                        }
                    ],
                    "filter": [],
                    "should": [],
                    "must_not": []
                }
            },
            "aggs": {
                "auto_complete": {
                    "terms": {
                        "field": "title.keyword",
                        "order": {
                            "_count": "desc"
                        },
                        "size": 25
                    }
                }
            }
        }

    def get(self):
        res = es.search(index=NODE_NAME, size=0, body=self.baseQuery)
        return res


parser = reqparse.RequestParser()
parser.add_argument("query", type=str, required=True, help="query parameter is Required ")

api.add_resource(Controller, '/autocomplete')


if __name__ == '__main__':
    app.run(debug=True, port=4000)
