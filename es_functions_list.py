import json
import random

def create_index(es, index):
    ## this function is to create a new index
    ## input: elastic connection, the string of index to be created
    ## this function returns an acknowledgment if successful or error 
    body = dict()
    #body['settings'] = get_setting()
    body['mappings'] = get_mappings()
    #print(json.dumps(body)) #examine the format    
    res = es.indices.create(index=index , body=body,ignore = 400)
    #print(res)
    return res


def get_setting():
    settings = {
        "index": {
            "setting1": 1,
            "setting2": 2
        }
    }
    return settings


def get_mappings():
    ## this function defines a document and its fields
    ## this function returns a Python dictionary
    mappings = {
        "properties": {
            "fid":{"type":"keyword"},
            "location_on_disk": {"type": "text"}  
                      }
               } #mappings
    return mappings

def load_data(fids,locations):
    ## this functopn convert the data of document into python dictionary 
    ## input list of data 
    ## this function returns a list of Python dictionary    
    #indces = ["6cafe024c7e9f79dcb654fdc34b2577a","cb404b5abaff0e2c302790c3d698d53a","dc186f2d44cf7389606ed1da176aa854"]
    #locations =["/var/www/data/example.txt", "/var/www/data/downloads/test.txt", "/var/www/data/huge_file.mp4"]
    ## **in this program, the document contains only one field. number of the fields can be dynamic as another input)

    data = list()
    for fid, location in zip(fids,locations):
        data.append(
            {
                "fid": fid,
                "location_on_disk": location
            }
        )
    return data

def create_data(es, index, data):
    ## this function is to create documents in the specific index
    ## input:  elastic connection, index that the ducuments are added to, documents in Python dictionary
    for d in data:
        res =es.index(index=index, body=d) 
        print(res['result'])

def get_query(field, val):
    ## this function is to create the query for search
    ## input: the field and the value of the field
    ## In this program, the document only contains one field
    ## this function returns the query as a Python dictionary
    query = {
        "query": {
            "bool": {
                "must": [
                 {
                    "match_phrase": {
                        field: val
                                    }}]
            }}}
    return query

def get_index_list(es):
    ## this fuction is to get all the exiting indices in elasticsearch
    ## input: elastic connection,
    ## this function returns index in Python list
    index_list = list()    
    for index in es.indices.get('*'):
        if index == '.security-7':
            continue
        index_list.append(index)
    if not index_list:
        index_list = ['No Index Found']
    return index_list


def query_all(es, selected_index):
    ## this function search all the documents in the specific index
    ## input: elastic connection, index to be searched
    ## this function returns the documents in Python list and string to summarise the search result
    fid_list = ["No Document in Selected Index"]
    location_list = []
    index_message = 'Selected index '+ selected_index + ' has no ' + ' documents.'
    if selected_index == 'No Index Found':
        fid_list = ["No Index Selected"]
        index_message = 'No Index Selected'
    else:
        query ={"query": {"match_all": {}}}      
        result = es.search(index=selected_index, body=query,ignore = [404])
        if result.get('hits')!=None and result['hits'].get('hits')!=None:
            num_of_docs = len(result['hits']['hits'])
            
            if num_of_docs > 0:
                fid_list = []
                index_message = selected_index + ' has ' + str(num_of_docs) + ' documents of this app.'               
                for hit in result['hits']['hits']:
                    if hit['_source'].get('fid')!= None and hit['_source'].get('location_on_disk')!= None:
                        fid_list.append(hit['_source']['fid']) 
                        location_list.append(hit['_source']['location_on_disk'])   
                


                if len(fid_list)==0:
                    location_list = []
                    fid_list = ["No Document in Selected Index"]
                    index_message = 'Selected index '+ selected_index + ' has no ' + ' documents of this app, ' + str(num_of_docs) + ' documents in total.'
                elif len(fid_list) != num_of_docs:
                    index_message = selected_index + ' has ' + str(len(fid_list)) + ' documents of this app, ' + str(num_of_docs) + ' documents in total.'

    return (index_message, fid_list, location_list)


def code_string(username, password):
    asc_usr =[]
    asc_pass =[]
    for u in username:
        asc_usr.append(ord(u))
    for p in password:
        asc_pass.append(ord(p))
    
