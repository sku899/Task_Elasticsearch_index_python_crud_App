#!/bin/bash
	
	sudo rm -rf Task_Elasticsearch_index_python_crud_App

	
	git clone https://github.com/sku899/Task_Elasticsearch_index_python_crud_App
	
	cd Task_Elasticsearch_index_python_crud_App
	
	sudo docker login
	
  sudo docker stack deploy --compose-file docker-compose.yaml task
