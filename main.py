import json
import pandas as pd
import requests
import argparse
from sqlalchemy import create_engine


#ToDo Error handling user input
# Create the parser
my_parser = argparse.ArgumentParser(prog='CLI',description='Organization information from GitHub')

# Add the arguments
my_parser.add_argument('Organization',
                       metavar='organization',
                       type=str,
                       help='the organization to get from GitHub')

# Execute the parse_args() method
args = my_parser.parse_args()
#User input argument
input_organization = args.Organization

headers={"Authorization": "bearer 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"}

url = 'https://api.github.com/graphql'
#ToDo: could read in all data about Organizations but later create database entries only with few selected entries
#ToDo Pagination-get all repositories and members (not just first 5)
#ToDo CommitConnection(Commit)database-sha

variables={"Orga":input_organization}
#Some relevant organization data is queried via the GraphQL GitHub API
query_exOrganization="""
query{
  organization(login: "%(Orga)s"){
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
  }"""%(variables)
#ToDo Error handling for None values in any query related output(maybe default substitute)-> sql does not like it

#ToDo create Repository database with more detailed data-post request,save in file,normalize then create database

#the "answer" from the API
r = (requests.post(url, json={'query': query_exOrganization},headers=headers))
#is transformed to json and written into a .json file
json_data = json.loads(r.text)
r_json=r.json()
jsonString = json.dumps(r_json)
jsonFile = open("%(Orga)s_data.json", "w")
jsonFile.write(jsonString)
jsonFile.close()
#reading json into several dataframes-members and repositories have lists that need to specially be normalized
df_organization=json_data['data']['organization']

df_repo = json_data['data']['organization']['repositories']
df_members=json_data['data']['organization']['membersWithRole']
#we only want some information in our database- .loc
dfOrganization=pd.json_normalize(df_organization)
df_Organization=dfOrganization.loc[:,['id','name','url','description']]

dfMembers = pd.json_normalize(df_members,record_path=['nodes'])
dfMembers=dfMembers.loc[:,['id']]
#we want to create a relation database that represents the connection between the organisation and the members, so the organization ID is added for all members
dfMembers['organization_id']=df_Organization['id'][0]

dfRepo=pd.json_normalize(df_repo,record_path=['nodes'])
#the relation of the repositories and organizations also requires the organization ID
dfRepo['organization_id'] = df_Organization['id'][0]

#ToDo one could think about adding rows in all databases (if they exist locally) for each new organization and related queries
#lastly we create the databases and save the into a file
engine = create_engine('sqlite:///save_pandas.db', echo=True)
sqlite_connection = engine.connect()
dfMembers.to_sql("MembersOrganizationConnection",sqlite_connection,if_exists='fail')
dfRepo.to_sql("RepositoryOrganizationConnection", sqlite_connection, if_exists='fail')
df_Organization.to_sql("Organizations",sqlite_connection,if_exists='fail')
