# UNH Search Engine

This project is used search keywords similar to UNH site, this project is extention to project 1.

Sowftwares used :

1. Python
2. Elasticsearch

** you can skip installation steps if you already installed for project1, as most of the modules are same **
## Instalation

##### Python and dependent module steps:
- Download and install python 3.9.X from "https://www.python.org/downloads/"
- Check installtion status using "python -v" command in command prompt
- Install pip from "https://phoenixnap.com/kb/install-pip-windows"
- Install all dependecy modules using "pip install 'module name'" syntax, below are required examples, it will ignore if module already exists.
		- pip install requests
		- pip install bs4
		- pip install jproperties
		- pip install flask
		- pip install elasticsearch
		- pip install flask_paginate
- Incase if you see any error like "*Module Not found*" which is not listed above then, please install that module using pip command
		- pip install module_name

##### Elastic Search Instalation:

- Install the latest java version or check your current version by using “java -version” command in command line prompt (Java version should be 8 or more)
- Set environment variable for JAVA
- Download elastic zip file from "https://www.elastic.co/downloads/elasticsearch"
- Unzip the file
- Go to bin folder
- Double click on “elasticsearch.bat” file
- Open a browser, type “*localhost:9200*” and it will show you name, cluster name of elasticsearch and other information in JSON format.
					{
					  "name" : "LAPTOP-1234567",
					  "cluster_name" : "elasticsearch",
					  "cluster_uuid" : "XggqxXAhSgW8scTOBgiyHg",
					  "version" : {
						"number" : "7.12.1",
						"build_flavor" : "default",
						"build_type" : "zip",
						"build_hash" : "3186837139b9c6b6d23c3200870651f10d3343b7",
						"build_date" : "2021-04-20T20:56:39.040728659Z",
						"build_snapshot" : false,
						"lucene_version" : "8.8.0",
						"minimum_wire_compatibility_version" : "6.8.0",
						"minimum_index_compatibility_version" : "6.0.0-beta1"
					  },
					  "tagline" : "You Know, for Search"
					}

### run search api

	- Once unh crawlling is done using project 1, now we can start search engine to search on stored content.
	- Before running, we can edit crawler.properties file to configure like elastic_search url, index name (this index name should be same used in for storing using unh_crawler)
	
		- search_index_name = unh						- index to be searched when given query, if you created multiple indexes (like using file crawler), then you can pass unh, 													unh2 to search on both
		- elastic_search_url = http://localhost:9200	- configure elastic search server url details

#command#
	- Open command prompt and run "*python app.py*" from current directory where project1 source code is available. 
	- Once the server started, it will show console like below on command prompt
				 * Serving Flask app "app" (lazy loading)
				 * Environment: production
				   WARNING: This is a development server. Do not use it in a production deployment.
				   Use a production WSGI server instead.
				 * Debug mode: off
				 * Running on http://0.0.0.0:5001/ (Press CTRL+C to quit)
	- Open any browser and type "http://localhost:5001/", will open search page, where we can type key words in search box and enter for searching.
	- http://localhost:5001/search?query=computer+science will automatically search and open results without entering in text box
	- http://localhost:5001/search?query=computer+science&per_page=20 returns per page 20 results and pagination links created dynamically based on total results found for that query

##Type Ahead Functionality
	- As when usder start typing, it shows results in drown down list as suggestions.
	- I have used front end, Jquery and Ajax to submit HTTP request, when user type very letter in text box.
	- In backend created an API /auto which query elastic searcch for matching words in meta_keywords field from unh index stored.
	- elastic search provides match_phrase_prefix query type , where it can check for given field phrase matching and aggaregate results before sending response as JSON