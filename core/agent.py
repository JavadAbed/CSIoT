import pymongo
import csv
import io
from core.common import get_conn
from core.common import  WebException
from random import *

def new_agent(params):
  db = get_conn()
  # validate, agent name must be uniq
  old = db.agents.find({"agentName": params["agentName"]})
  if old.count()>0:
     raise WebException("Agent with identical name already exists.")
  # TODO more validations
  params["agentQoI"] = randint(1,5)
  params["agentQoD"] = randint(1,5)
  params["agentAvailability"] = randint(1,5)
  params["agentQoS"] = randint(1,5)
  db.agents.insert(params)
  return agents()


def upload_agent(file):
  in_memory_file = io.BytesIO()
  file.save(in_memory_file)
  reader = csv.reader(file)
  for row in reader:
     print(row)
  pass#TODO


def getShape(batchId):
  return "ellipse";

def agents():
  db = get_conn()
  agents = db.agents.find()
  data = []
  for agent in agents:
     data.append({"data": {"agentName": agent["agentName"],
			"shape": getShape(agent["agentBatch"]),
		},
		"position": {"x": float(agent["agentX"])*2000,"y":float(agent["agentY"])*2000 }    })
  return data

def makeCSVString():
   db = get_conn()
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
