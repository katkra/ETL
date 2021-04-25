import json
import pandas as pd
import requests
from pandas.io.json import json_normalize
from pandas import DataFrame
headers={"Authorization": "bearer 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"}

url = 'https://api.github.com/graphql'
query = """query {
  organization(login: "facebook") {
    name
    url
    repository(name: "react"){
      name,
      url
      pullRequests (first:5){
        nodes {
          title
        }
      }
    }
  }
}"""
r = requests.post(url, json={'query': query},headers=headers)
#print(r.status_code)
print(r.text)

