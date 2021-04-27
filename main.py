import json
import pandas as pd
import requests
from sqlalchemy import create_engine
import sqlite3 as lite
import sys
from pandas.io import sql
from pandas import DataFrame
headers={"Authorization": "bearer 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"}

url = 'https://api.github.com/graphql'
#ToDo: read in all data about Organizations but later create database entries only with few selected entries
#ToDo exchange specific organization with variables-values will be set by user input
#ToDo Pagination-get all repositories and members (not just first 5)

#query ($Orga:String!){
query_exOrganization="""
query{
  organization(login: "github"){
    name
    url
    id
    description
    
    membersWithRole(first:5){
    nodes{
    id
    company
   
        }
      }
    repositories(first:5){
    nodes{
    id
    name
    owner{
    id
    login
    }
      
    }
    }
    }
  }"""
#variables={"Orga":'github'}
#ToDo create Repository database with more detailed data-post request,save in file,normalize then create database
query_exRepo = """"
query {
  repository(owner:"github",name:"media"){
    name
    url
    id
    isPrivate
    createdAt
    updatedAt
    
    
    }
  }"""


r = (requests.post(url, json={'query': query_exOrganization},headers=headers))

r_json = r.json()
print(r_json)
jsonString = json.dumps(r_json)
jsonFile = open("Github_data.json", "w")
jsonFile.write(jsonString)
jsonFile.close()
df_data = pd.read_json("Github_data.json", orient='columns')
df = pd.DataFrame(df_data)


json_data = json.loads(r.text)

df_organization=json_data['data']['organization']



df_repo = json_data['data']['organization']['repositories']
df_members=json_data['data']['organization']['membersWithRole']


dfOrganization=pd.json_normalize(df_organization)


df_Organization=dfOrganization.loc[:,['id','name','url','description']]


dfMembers = pd.json_normalize(df_members,record_path=['nodes'])
dfMembers['organization_id']=df_Organization['id'][0]
dfRepo=pd.json_normalize(df_repo,record_path=['nodes'])
dfRepo['organization_id'] = df_Organization['id'][0]




engine = create_engine('sqlite:///save_pandas.db', echo=True)
sqlite_connection = engine.connect()
dfMembers.to_sql("MembersOrganizationConnection",sqlite_connection,if_exists='fail')
dfRepo.to_sql("RepositoryOrganizationConnection", sqlite_connection, if_exists='fail')
df_Organization.to_sql("Organizations",sqlite_connection,if_exists='fail')

#ToDo one could think about adding rows in all databases (if they exist locally) for each new organization and related queries