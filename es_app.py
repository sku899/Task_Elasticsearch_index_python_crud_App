from flask import Flask, render_template, request, flash, session, url_for, redirect
from elasticsearch import Elasticsearch
import random
from es_forms import LoginForm, CreateForm
from  es_functions_list import *


app = Flask(__name__)
app.config['SECRET_KEY'] = 'YOUR_SECRET_KEY'

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    username = form.username.data
    password = form.password.data
    if not(username is None or password is None) and form.connect.data: 
        #"host": "host.docker.internal"
        #"host": "localhost"
        es = Elasticsearch(hosts=[{"host": "localhost", "port": 9200}], http_auth=(username, password))
        if es.ping():
            session['username'] = username
            session['password'] = password
            return  redirect(url_for('create'))
        else:
            return render_template('login.html', form = form, message = "incorrect passsword or user name" )
    else:
        return render_template('login.html', form = form, message = '' )

@app.route('/create', methods=['GET', 'POST']) #'/create/<password>/<username>'
def create():
    username = session.get('username','elastic')
    password = session.get('password','password')
    #{"host": "host.docker.internal", "port": 9200}]
    #{"host": "localhost", "port": 9200}
    es = Elasticsearch(hosts=[{"host":"localhost", "port": 9200}], http_auth=(username, password)) 
    if not es.ping():
        return  redirect(url_for('login'))

    form = CreateForm()
    form.es_index.choices = []
    #{"host": "host.docker.internal", "port": 9200}]
    #es = Elasticsearch(hosts=[{"host": "localhost", "port": 9200}], http_auth=(username, password))    
    form.es_index.choices = get_index_list(es)
    if form.es_index.data is None:
        selected_index = form.es_index.choices[0]
    else:
        selected_index = form.es_index.data   
    index_message, fid_list, location_list = query_all(es, selected_index)
    form.documents.choices = fid_list



    if form.go.data:      
        selected_index = form.es_index.data
        index_message, fid_list, location_list = query_all(es, selected_index)
        # if len(fid_list) ==0:
        #     fid_list = ["No Document in Selected Index"]
        form.documents.choices = fid_list
        return render_template('create.html', form = form, \
            message_index=index_message, message_create_index='', message_document='' ) 

    if form.create.data:
        new_index = form.new_index.data
        index_message = ''
        if new_index is None or len(new_index)==0:
            message_create_index = 'Please input an index.'
        else:
            is_exist = es.indices.exists(index=new_index)
            if is_exist:
                message_create_index = 'Index ' + new_index + ' has already existed. No index is created.'
            else:
                create_index(es, new_index)
                message_create_index = 'Index ' + new_index + ' has been created.'
                is_created = es.indices.exists(index=new_index)
                if is_created:                    
                    form.es_index.choices = get_index_list(es)
                #change status
                form.es_index.data = new_index
                index_message = 'New created index '+ new_index + ' has no ' + ' documents.'
                form.documents.choices = ["No Document in Selected Index"]
                form.new_index.data = ''
        return render_template('create.html', form = form, \
            message_create_index=message_create_index, message_index=index_message)

    if form.delete.data:
        deleted_index = form.es_index.data
        if deleted_index == 'No Index Found':
            message_create_index = 'No Index is Deleted. '
        else:
            is_exist = es.indices.exists(index=deleted_index, ignore=400)
            if is_exist: 
                es.indices.delete(index=deleted_index, ignore=[400, 404])
                is_deleted = not es.indices.exists(index=deleted_index)
                if is_deleted:
                    #index_message = 'Selected Index ' + deleted_index + ' has been deleted'
                    form.es_index.choices = get_index_list(es)
                    ##update
                    form.new_fid.data =''
                    form.new_index.data =''
                    selected_index = form.es_index.choices[0]
                    index_message, fid_list, location_list = query_all(es, selected_index)
                    form.documents.choices = fid_list
                    message_create_index = 'Index ' + deleted_index + ' has been deleted.' 

        return render_template('create.html', form = form, message_create_index=message_create_index, message_index= index_message)
    
    if form.add_document.data:
        new_fid = form.new_fid.data
        new_location = form.new_location.data
        index_message = ''
        if new_fid is None or new_location is None or len(new_fid)==0 or len(new_location)==0:
            document_message = 'File id and location cannot be empty.'
        else:
            index_to_add_document = form.es_index.data
            ## check if document already exists
            msg, doc_list, location_list = query_all(es, index_to_add_document)
            is_exist = [new_fid in doc_list, new_location in location_list]
            if is_exist[0] or is_exist[1]:
                if is_exist[0] and is_exist[1]:
                    document_message = 'No Ducuement added. Input file id ' + new_fid + ' and location ' + new_location + ' have existed in selected index '+ index_to_add_document
                elif is_exist[0]:
                    document_message = 'No Ducuement added. Input file id ' + new_fid + ' has existed in selected index '+ index_to_add_document
                else:
                    document_message = 'No Ducuement added. Input location ' + new_location + ' has existed in selected index '+ index_to_add_document

            else:
                document_message = 'New document with file id ' + new_fid + ' has been added.'
                data = load_data([new_fid], [new_location])
                create_data(es, index_to_add_document,data)
                es.indices.refresh(index=index_to_add_document)
                msg, fid_list, location_list = query_all(es, index_to_add_document)
                form.documents.choices = fid_list
                #update
                form.new_fid.data = ''
                form.new_location.data = ''
                index_message = msg #index_to_add_document + ' has ' + str(len(form.documents.choices))+ ' documents.' 
        return render_template('create.html', form = form, message_document = document_message, message_index = index_message)
    
    if form.delete_document.data:
        fid_list = []
        index_to_delete_document = form.es_index.data
        document_to_be_deleted = form.documents.data
        # query ={"query": {"match_all": {}}}
        # result = es.search(index=index_to_delete_document, body=query)            
        # for hit in result['hits']['hits']:
        #     fid_list.append(hit['_source']['fid']) 
        msg, fid_list, location_list = query_all(es, index_to_delete_document)
        query = get_query("fid", document_to_be_deleted )
        result_to_be_deleted = es.search(index=index_to_delete_document, body=query)
        result = result_to_be_deleted ['hits']['hits']
        for hit in result:
            id = hit['_id']
            es.delete(index=index_to_delete_document,id=id, refresh=True)
        ##refresh ES
       
        
        # if not fid_list:
        #     doc_list = ["No Document in Selected Index"]
        #es.indices.refresh(index=document_to_be_deleted)
        #index_message, doc_list = query_all(es, index_to_delete_document)
        msg, fid_list, location_list = query_all(es, index_to_delete_document)
        # if len(fid_list)==0:
        #     fid_list = ["No Document in Selected Index"]
        form.documents.choices = fid_list  
            
        ##update'
        return render_template('create.html', form = form, \
            message_document='Document with file id ' + document_to_be_deleted + ' has been deleted', message_index = msg)

    return render_template('create.html', form = form, \
        message='', message_index=index_message, message_create_index='', message_document='') 



if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)  