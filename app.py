import json
import re

import requests
from flask import Flask, render_template, request, make_response
from elasticsearch import Elasticsearch
from flask_paginate import Pagination, get_page_args
from jproperties import Properties

app = Flask(__name__)
es = Elasticsearch("http://localhost:9200")
index_name = "unh2,folder_data"
index_name2 = "folder_data"
crawl_configs_dict = {}


@app.route('/')
def home():
    return render_template('search.html')


@app.route('/search', methods=['GET', 'POST'])
def search_request():
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')

    print(page)
    print(per_page)
    print(offset)

    search_term = "";
    if request.method == 'POST':
        search_term = request.form["query"]
    if request.method == 'GET':
        search_term = request.args.get("query")
        print(search_term)
        if search_term is None:
            search_term = "*"
    print(search_term)
    if offset == 0:
        from_param = 0
    else:        
        from_param = offset #+ (page - 2)
    print("from_param " + str(from_param))
    res = es.search(
        index=index_name,
        size=per_page,
        from_=from_param,
        body={
            "query": {
                "query_string": {
                    "fields": [
                        "title",
                        "url",
                        "meta_keywords",
                        "description",
                    ],
                    "query": search_term,
                    "default_operator": "OR",
                    "analyzer": "standard"
                }
            },
            "highlight": {
                "fields": {
                    "title": {
                        "pre_tags": [
                            "<strong>"
                        ],
                        "post_tags": [
                            "</strong>"
                        ],
                        "fragment_size": 150,
                        "number_of_fragments": 1,
                        "type": "plain"

                    },
                    "description": {
                        "pre_tags": [
                            "<strong>"
                        ],
                        "post_tags": [
                            "</strong>"
                        ],
                        "fragment_size": 150,
                        "number_of_fragments": 1,
                        "type": "plain"

                    }
                },
                "encoder": "html"
            }

        }
    )

    total_count = res["hits"]["total"]["value"]
    time = (res["took"] / 1000)

    pagination = Pagination(page=page, per_page=per_page, total=total_count, css_framework='bootstrap4')
    print(res)
    headers = {'Content-Type': 'text/html'}
    # res=resp,page=page,per_page=per_page,pagination=pagination,
    return render_template('results.html', query=search_term, res=res, page=page, per_page=per_page, total=total_count,
                           time=time, pagination=pagination, )


@app.route('/auto', methods=['GET', 'POST'])
def auto_search_request():
    search_term = "";
    if request.method == 'POST':
        search_term = request.form["data"]
    if request.method == 'GET':
        search_term = request.args.get("query")
        print(search_term)
        if search_term is None:
            search_term = "*"
    print(search_term)

    baseQuery = {
        "_source": [],
        "size": 0,
        "min_score": 0.5,
        "query": {
            "bool": {
                "must": [
                    {
                        "match_phrase_prefix": {

                            "meta_keywords": {
                                "query": search_term
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
                    "field": "meta_keywords.keyword",
                    "order": {
                        "_count": "desc"
                    }

                }
            }
        }
    }

    res = es.search(index=index_name, body=baseQuery)
    return res


if __name__ == '__main__':
    try:
        configs = Properties()
        with open('crawler.properties', 'rb') as config_file:
            configs.load(config_file)

        crawl_configs_dict.clear()
        items_view = configs.items()
        for item in items_view:
            crawl_configs_dict[item[0]] = str(item[1].data)

        es_url = crawl_configs_dict["elastic_search_url"]
        print(es_url)
        index_name = crawl_configs_dict["search_index_name"]
        es = Elasticsearch(es_url)
        app.secret_key = 'mysecret'
        app.run(host='0.0.0.0', port=5001)
    except Exception as e:
        print("exception " + str(e))
