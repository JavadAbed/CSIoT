import pymongo
from core.common import get_conn
from core.common import  WebException


def new_agent(params):
  db = get_conn()
  # validate, agent name must be uniq
  old = db.agents.find({"agentName": params["agentName"]})
  if old.count()>0:
     raise WebException("Agent with identical name already exists.")
  # TODO more validations
  db.agents.insert(params)
  return agents()


def upload_agent(file):
  pass


def agents():
  db = get_conn()
  agents = db.agents.find()
  data = []
  for agent in agents:
     data.append({"data": {"agentName": agent["agentName"]}, "position": {"x": float(agent["agentX"])*2000,"y":float(agent["agentY"])*2000 }    })
  return data

def makeCSVString(agents):
   pass
