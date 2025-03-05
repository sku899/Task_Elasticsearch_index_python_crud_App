#By Sabina Ku#

This task is to develop a CRUD application, which will allow the users to read and modify files on disk.

**- Assumption: To run this app, it is assumed that a local Elasticsearch is installed. The users will require to input user name and password of Elasticsearch.**

## 1.The app ##

This app allows the users to add new indices and new documents to Elasticsearch. The index should be a string. The mappings of the document is as following,

    mappings = {
    "properties": {
    "fid":{"type":"keyword"},
    "location_on_disk": {"type": "text"}  
      }}

After login successfully, the app will display all the existing indices. Select any of the indices and retrieve index, the app will display all information of the documents under the selected index.


Please be noted that this app will only work fully with the documents having the same mappings above. The app can only work partially with the documents which have larger mappings including the above mappings (can be deleted). The documents with different mappings (i.e. not including the above mappings) cannot be seen in details or deleted. But they will be included in document counts. For example, if one index has three documents,




- only one has the same mappings. The display message would be:  Selected index (index xxxx) has 1 documents of this app, 3 documents in total.
- all have same mappings. The display message would be:  Selected index (index xxxx) has 3 documents.
- none of them is the same: The display message would be:  Selected index (index xxxx) has 3 documents of this app.

The users are allowed to add a new index, delete an existing index, add a new document to selected index and delete an exiting document from a selected index. For document operation, all the documents should be in the same mapping of this app.

##2.The Codes
This app contains four files:



1. es_app.py: The main app program which contains the routes of the flask.
2. es_forms: Define two forms in web app.
3. es_functions_list: A collection of functions used in the app.
4. es_tests.py: unittest for python. 7 test in total

The list of the functions are as following,

#### es_app.py



    @app.route('/', methods=['GET', 'POST'])
	@app.route('/home', methods=['GET', 'POST'])
	def login():
    	# login page
    	form = LoginForm()
    	username = form.username.data
    	password = form.password.data


	@app.route('/create', methods=['GET', 'POST']) 
	def create():
    	#document management page
    	username = session.get('username','elastic')
    	password = session.get('password','password')
 

#### es_forms.py ####

    class LoginForm(flask_wtf.FlaskForm):
		#login form
    	username = StringField('User name')
    	password = PasswordField('Password')
    	connect = SubmitField('Connect to Elasticsearch')
    
    class CreateForm(flask_wtf.FlaskForm):
		#document management form
	    es_index = SelectField('Existing Indices',choices=[],render_kw={'style': 'width: 23ch'})
	    documents = SelectField('Existing File ID',choices=[], render_kw={'style': 'width: 23ch'})
	    create = SubmitField('Create an index')
	    go = SubmitField('Retrieve Index')
	    new_index = StringField('New Index')#),validators=[validators.DataRequired()])
	    delete=  SubmitField('Delete selected Index')
	    add_document = SubmitField('Add a new document')
	    delete_document = SubmitField('Delete a document')
	    new_fid = StringField('New File ID')#),validators=[validators.DataRequired()])
	    new_location = StringField('New Location on Disk')

#### es_functions_list.py ####

    def create_index(es, index):
	    ## this function is to create a new index
	    ## input: elastic connection, the string of index to be created
	    ## this function returns an acknowledgment if successful or error         
    
    def get_mappings():
	    ## this function defines a document and its fields
	    ## this function returns a Python dictionary


    def load_data(fids,locations):
	    ## this functopn convert the data of document into python dictionary 
	    ## input list of data 
	    ## this function returns a list of Python dictionary
    
    def create_data(es, index, data):
	    ## this function is to create documents in the specific index
	    ## input:  elastic connection, index that the ducuments are added to, documents in Python dictionary
    
    
    def get_index_list(es):
	    ## this fuction is to get all the exiting indices in elasticsearch
	    ## input: elastic connection,
	    ## this function returns index in Python list
        
    
    def query_all(es, selected_index):
	    ## this function search all the documents in the specific index
	    ## input: elastic connection, index to be searched
	    ## this function returns the documents in Python list and string to summarise the search result

#### es_tests.py ####

	class TestCase(unittest.TestCase):

	    def setUp(self):
	        app.config['TESTING'] = True
	        self.app = app.test_client()
	
	    def test_login_page(self):
	        ##test login page	
	    
	    def test_updatebooking_get(self):
			## test document management page	
	
	    def test_no_duplicated_index_created(self):
	        ## test no duplicated index will be created   
	
	    def test_load_data(self):
	        ## test if data is returned in the correct format

	    def test_new_created_index(self):
	        ## test new created indices are included in thev list of all index

	    def test_no_document_in_index(self):
	        ## test new created index has no document 
	
	    def test_document_in_index(self):
	        ## test new created index has no document 

	  
## 3.Docker Images ##

The docker image of this app is built by this Dockerfile as shown,

    FROM python:3.9.6
    COPY . .
    RUN pip install Flask requests
    RUN pip install flask_wtf
    RUN pip install wtforms
    RUN pip install email_validator
    RUN pip install elasticsearch
    RUN pip install flask
    EXPOSE 5000
    ENTRYPOINT ["python"]
    CMD ["es_app.py"]

This image can be pull by

`docker pull sabinaku/optibrium_task:v2`

it can be run by

`docker run -d -p 5000:5000 sabinaku/optibrium_technical_task:v2`  


## 4.Link to CI-CD ##

The CI-CD Pipeline can be built by the Jenkinsfile as below, 


    pipeline {
        agent any 
        stages{
            stage("Test"){
                steps{
                    sh './scripts/test.sh'
                }
            }
        
            stage("Build-Images"){
                steps{
                    sh './scripts/build-images.sh'
                }
            }
                
            stage("Deploy"){
                steps{
                    sh './scripts/deploy.sh'
               }
           }  
