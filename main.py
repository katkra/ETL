import json
import pandas as pd
import requests
from pandas.io.json import json_normalize
from pandas import DataFrame
headers={"Authorization": "bearer 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"}

url = 'https://api.github.com/graphql'
#ToDo: read in all data about Organizations but later create database entries only with few selected entries
query_exOrganization= """
query {
  organization(login: "github") {
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
    }
    }
    }
  }
"""

r = (requests.post(url, json={'query': query_exOrganization},headers=headers))

r_json = r.json()
#print(r_json)
jsonString = json.dumps(r_json)
jsonFile = open("Github_data.json", "w")
jsonFile.write(jsonString)
jsonFile.close()
df_data = pd.read_json("Github_data.json",orient='columns')
df = pd.DataFrame(df_data)


json_data = json.loads(r.text)
df_organization=json_data['data']['organization']
df_repo = json_data['data']['organization']['repositories']
df_members=json_data['data']['organization']['membersWithRole']

dfOrganization=pd.json_normalize(df_organization)
dfRepo = pd.json_normalize(df_repo)
dfMembers = pd.json_normalize(df_members)

print(dfOrganization.columns)
print(dfOrganization.values)

print(dfRepo.columns)
print(dfRepo.values)

print(dfMembers.columns)
print(dfMembers.values)