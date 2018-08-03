import pymongo
from core.common import get_conn
from core.common import  WebException

import code

def new_agent(params):
  db = get_conn()
  # validate, agent name must be uniq
  #code.interact(local=locals())
  old = db.agents.find({"agentName": params["agentName"]})
  if old.count()>0:
     raise WebException("Agent with identical name already exists.")
  # TODO more validations
  db.agents.insert(params)
  print(params)


  pass



def upload_agent(file):
  pass
