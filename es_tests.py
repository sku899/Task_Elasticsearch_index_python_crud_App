#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
from elasticsearch import Elasticsearch
import random
from flask import Flask, render_template, request, flash, session, url_for, redirect
from es_functions_list import *
from es_app import app

def create_random_index(num):
    index_list = []
    for n in range(num):        
        is_duplicate = True
        while is_duplicate:
            index_to_create = '';
            for i in range(10):
                index_to_create = index_to_create+ chr(random.randint(97, 122))
            if not (index_to_create in index_list):
                index_list.append(index_to_create)
                is_duplicate = False
    return index_list



class TestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
 
    def tearDown(self):
        pass

    def test_login_page(self):
        print('test login page')
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    ##
    def test_updatebooking_get(self):
        response = self.app.get('/create', follow_redirects=True)
        self.assertEqual(response.status_code,200)
    ##


    def test_no_duplicated_index_created(self):
        ## test no duplicated index will be created        
        index_to_create =  create_random_index(1)[0]
        #first create if OK
        # second create is not OK    
        self.assertTrue(create_index(es,index_to_create)['acknowledged'])
        # status 400 = index exits
        self.assertEqual(create_index(es,index_to_create)['status'],400)
        es.indices.delete(index=index_to_create, ignore=[400, 404])


    def test_load_data(self):
        ## test if data is returned in the correct format
        fids = ["6cafe024c7e9f79dcb654fdc34b2577a","cb404b5abaff0e2c302790c3d698d53a","dc186f2d44cf7389606ed1da176aa854"]
        locations =["/var/www/data/example.txt", "/var/www/data/downloads/test.txt", "/var/www/data/huge_file.mp4"]
        location_dict =[{"fid": fids[0], "location_on_disk": locations[0]}, \
            {"fid": fids[1],"location_on_disk": locations[1]},\
                {"fid": fids[2],"location_on_disk":locations[2]}]
        self.assertEqual(load_data(fids, locations), location_dict)

    def test_new_created_index(self):
        ## test new created indices are included in thev list of all index
        new_index_list = create_random_index(5)
        existing_index_list = get_index_list(es)
        #print(existing_index_list)
        is_in_list = False
        for index in new_index_list:
            if self.assertNotIn(index, existing_index_list):
                is_in_list = True
                break
        
        if not is_in_list:
            for index in new_index_list:
                create_index(es,index)
            new_existing_index_list = get_index_list(es)
            #print(new_existing_index_list)
            for index in new_index_list:
                self.assertIn(index, new_existing_index_list)
                es.indices.delete(index=index, ignore=[400, 404])

    def test_no_document_in_index(self):
        ## test new created index has no document 
        index_to_create =  create_random_index(1)[0]
        existing_index_list = get_index_list(es)
        if not index_to_create in existing_index_list:
            create_index(es,index_to_create)
            msg, d_list, l_list = query_all(es, index_to_create)
            self.assertEqual(msg, 'Selected index '+ index_to_create + ' has no ' + ' documents.')
            self.assertEqual(d_list, ["No Document in Selected Index"])
            es.indices.delete(index=index_to_create, ignore=[400, 404])

    def test_document_in_index(self):
        ## test new created index has no document 
        index_to_create =  create_random_index(1)[0]
        existing_index_list = get_index_list(es)
        fids = ["6cafe024c7e9f79dcb654fdc34b2577a","cb404b5abaff0e2c302790c3d698d53a","dc186f2d44cf7389606ed1da176aa854"]
        locations =["/var/www/data/example.txt", "/var/www/data/downloads/test.txt", "/var/www/data/huge_file.mp4"]
        if not index_to_create in existing_index_list:
            create_index(es,index_to_create)
            data = load_data(fids, locations)
            create_data(es, index_to_create,data)
            es.indices.refresh(index=index_to_create)
            msg, d_list, l_list= query_all(es, index_to_create)
            self.assertEqual(msg, index_to_create + ' has ' + str(len(locations))+ ' documents of this app.' )            
            self.assertEqual(l_list, locations)
            es.indices.delete(index=index_to_create, ignore=[400, 404])








if __name__ == '__main__':
    username = input('Elasticsearch user name: ')
    password = input('Elasticsearch user password: ')
    es = Elasticsearch(hosts=['localhost:9200'], http_auth=(username, password))
    if es.ping():
        unittest.main()
    else:
        print('Cannot connect to local Elasticsearch. No test is done.')
