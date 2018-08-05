import pymongo
import csv
import io
from core.common import get_conn
from core.common import  WebException
from random import *

def new_agent(params):
  db = get_conn()
  # validate, agent name must be uniq
  old = db.agents.find({"name": params["agentName"]})
  if old.count()>0:
     raise WebException("Agent with identical name already exists.")
  # TODO more validations

  agent ={
    "name": params["agentName"],
    "owner": params["agentOwner"],
    "batch": params["agentBatch"],
    "locality": float(params["agentLocality"]),
    "x": float( params["agentX"]),
    "y": float(params["agentY"]),
    "friends_h": params["agentFriendsH"].split('-'),
    "friends_m": params["agentFriendsM"].split('-'),
    "friends_l": params["agentFriendsL"].split('-'),
    "qoi" : randint(0,10),
    "qod" : randint(0,10),
    "qos" : randint(0,10),
    "availability" : randint(0,10),
    "friendships": {}
  }
  db.agents.insert(agent)
  return agents()

def deleteAll():
   db = get_conn()
   db.agents.delete_many({})

def upload_agent(file):
  in_memory_file = io.BytesIO()
  file.save(in_memory_file)
  reader = csv.reader(file)
  for row in reader:
     print(row)
  pass#TODO


def agents():
  db = get_conn()
  agents = db.agents.find()
  data = []
  for agent in agents:
     data.append({"data": {"name": agent["name"]},
		"position": {"x": agent["x"],"y":agent["y"] }    })
  return data

def makeCSVString():
   db = get_conn() # TODO update 
   agents = db.agents.find()
   output = io.StringIO()
   spamwriter = csv.writer(output)
   spamwriter.writerow(["agentName","agentOwner","agentBatch","agentFamily","agentX","agentY","agentFriends","agentNeeds","agentOffers"])
   for agent in agents:
       spamwriter.writerow([agent.get("agentName"),agent.get("agentOwner"),
				agent.get("agentBatch"),agent.get("agentFamily"),
				agent.get("agentX"),agent.get("agentY"),agent.get("agentFriends"),
				agent.get("agentNeeds"),agent.get("agentOffers")])
   return output.getvalue()
