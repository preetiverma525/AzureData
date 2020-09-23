#!/usr/bin/env python
# coding: utf-8

# In[7]:


from flask import Flask,request, render_template, session, redirect


# In[8]:
#import os
#print(os.getcwd())
#os.chdir(r'\Users\preeti.sitaram.verma\Documents\python\PY')



from Track_record_inside_the_QB_Multiple_data_BPS import *
#import Track_record_inside_the_QB_Multiple_data_BPS 

# In[9]:


print(all_data)


# In[10]:


val=all_data.to_dict('records')


# In[11]:


print(val)


# In[6]:


# id='2'
# results = []
# book=[]
# for data in track_changed_for_ins:
#     if data['Record_Id']==id:
#         results.append(data)
# print(results)
# #         data=jsonify(results)
# #         print(data)


# In[12]:


import flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Create some test data for our catalog in the form of a list of dictionaries.
data=val


@app.route('/', methods=['GET'])
def home():
    return '''<h1>WELCOME</h1>
<p>Get all insterted and delected text from the word document.</p>'''

# A route to return all of the available entries in our catalog.
@app.route('/api/all', methods=['GET'])
def api_all():
    return jsonify(data)

@app.route('/api', methods=['GET'])

def api_id():
    if 'Id' in request.args:
        Id = request.args['Id']
        print(Id)
    else:
        return "Error: No id field provided. Please specify an id."
    results = []
    for d in data:
        if d['Record_Id'] == Id:
            results.append(d)
    return jsonify(results)
    

app.run(debug=True,use_reloader=False)


# In[ ]:




