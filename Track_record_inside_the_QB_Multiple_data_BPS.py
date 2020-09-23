#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import xmltodict
import pprint
import json


# In[2]:


url = "https://bps.quickbase.com/db/bqsuve7qy?a=API_DoQuery&fmt=structured&usertoken=b5d3bm_kn5b_d4c4hh5b76ajm4t6fzg96bbber"
#url = "https://builderprogram-pverma.quickbase.com/db/bqscz87a5?a=API_DoQuery&fmt=structured&ticket=9_bqs7bdfax_b5fdma_nx3z_a_-b_ufsj4vbstivafsmxsfcdxq9mdbckgwuzxb8r9rk9bvnwt8ebi7agah_d2re5rt"


# In[3]:


url


# In[4]:


response = requests.request("GET", url)
print(response)
r=response.text.encode('utf8')
print(r)
pp = pprint.PrettyPrinter(indent=4)
data=json.dumps(xmltodict.parse(r))
data1=json.loads(data)


# In[5]:


data1


# In[6]:


# def get_data(Title):
#     Record Id=Title=Description=Document URL=""
#     for i in data1.values():
#             values=i['table']['records']['record']['f']
#             print(values)
#             for id_item in values:
#                 if id_item["@id"]=="6":
#                     Title=id_item['#text']
#                     print(Title)
#                 if id_item["@id"]=="7":
#                     Description=id_item['#text']
#                     print(Description)
#                 if id_item["@id"]=="8":
#                     Document=id_item['#text']
#             #return {"Title":Title,"Description":Description,"Document":Document}
#                     doc_data={"Document":Document }
#             return doc_data
            


# In[7]:


document_url=[]
R_ID=[]
def get_data():
    document_url=[]
    R_ID=[]
    R_Id=Document=""
    for i in data1.values():
        values=i['table']['records']['record']
        for j in values:
            list_data=j['f']
#             print(list_data)
            for data in list_data:
                if data['@id']=="8":
                    Document=data['url']
                    document_url.append(Document)
                if data['@id']=="3":
                    R_Id=data['#text']
                    R_ID.append(R_Id)
#     print(R_ID)
#     print(document_url)
    Mapped_data=dict(zip(R_ID,document_url))
    return Mapped_data
#             latest={"Document":Document,"R_Id":R_Id}
#             latest=dict(zip(Document,R_Id))
#             print(latest)
#                 doc_data={R_id:Document}


# In[8]:


data_all=get_data()


# In[9]:


data_all


# In[10]:


from zipfile import ZipFile
from urllib.request import urlopen
from io import BytesIO
from zipfile import *
from bs4 import BeautifulSoup
import pandas as pd


# In[11]:


for key, value in data_all.items():
    print(value)
#     wordfile=urlopen(value).read()
#     print(wordfile)


# In[12]:


track_changed_for_del=[]
track_changed_for_ins=[]
for key, value in data_all.items():
    wordfile=urlopen(value).read()
    wordfile=BytesIO(wordfile)
    document=ZipFile(wordfile)
    document.namelist()
    xml_content=document.read('word/document.xml')
    wordobj=BeautifulSoup(xml_content.decode('utf-8'),'xml')
    key_record=key
    for dl in wordobj.find_all('w:del'):
        Text=dl.text
        author=dl.get('w:author')
        Date=dl.get('w:date')
        Type='Deleted Text'
        ID=dl.get('w:id')
        ID=int(ID)
        dataDict_del = { 'Text':Text,'Author':author,'Date':Date,'Type':Type,'ID':ID,'Record_Id':key_record}
        track_changed_for_del.append(dataDict_del)
    
        
    for ins in wordobj.find_all('w:ins'):
        Text=ins.text
        author=ins.get('w:author')
        Date=ins.get('w:date')
        Type='Inserted Text'
        ID=ins.get('w:id')
        ID=int(ID)
        dataDict_ins = { 'Text':Text,'Author':author,'Date':Date,'Type':Type,'ID':ID,'Record_Id':key_record}
        track_changed_for_ins.append(dataDict_ins)
    df_track_changed_ins= pd.DataFrame(track_changed_for_ins)
    df_track_changed_del= pd.DataFrame(track_changed_for_del)
    df_track_changed_del["Text"]= df_track_changed_del["Text"].replace(' ', "NaN")
    df_track_changed_ins["Text"]= df_track_changed_ins["Text"].replace('', "NaN")
    df_track_changed_del.drop(df_track_changed_del.loc[df_track_changed_del['Text']=='NaN'].index, inplace=True)
    df_track_changed_ins=df_track_changed_ins.sort_values(by='ID')
    df_track_changed_del=df_track_changed_del.sort_values(by='ID')
    


# In[13]:


type(track_changed_for_ins)


# In[14]:


df_track_changed_ins


# In[15]:


df_track_changed_del


# In[16]:


all_data=df_track_changed_ins.append(df_track_changed_del)


# In[17]:


all_data=all_data.sort_values(by='ID',ascending=True)


# In[18]:


print(all_data)


# In[19]:


val=all_data.to_dict('records')


# In[20]:


print(val)


# In[21]:


val


# In[23]:


csv_data=all_data.to_csv(index=False,header=False)


# In[32]:


csv_data


# In[38]:


usertoken = 'b5d3bm_kn5b_d4c4hh5b76ajm4t6fzg96bbber'
dbid = 'bqi9wpaun'


# In[39]:


field_list='12.6.8.7.11.13'


# In[40]:


headers = {'Content-Type': 'application/xml', 'QUICKBASE-ACTION': 'api_importfromcsv'}
data = '<qdbapi><records_csv><![CDATA[' + csv_data + ']]></records_csv><clist>'+field_list+'</clist>        <usertoken>' + usertoken + '</usertoken></qdbapi>'


# In[41]:


import requests
r2 = requests.post(url='https://bps.quickbase.com/db/' + dbid, data=data.encode('utf-8'), headers=headers)

r2
# In[37]:


print(r2)


# In[ ]:




