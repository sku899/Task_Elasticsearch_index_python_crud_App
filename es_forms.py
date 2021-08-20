from flask import Flask, render_template, request, flash, session, url_for, redirect
from wtforms import StringField, SubmitField, PasswordField, SelectField, validators
import flask_wtf #import FlaskFormimport




class LoginForm(flask_wtf.FlaskForm):
    username = StringField('User name')
    password = PasswordField('Password')
    connect = SubmitField('Connect to Elasticsearch')
    #register = SubmitField('Create New Account')
    #entrydate =DateField()

class CreateForm(flask_wtf.FlaskForm):
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