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


def getShape(batchId):
  return "ellipse";
#  shape = "diamond"
#  shape =  {
#	0: "diamond",
#	1: "ellipse",
#	2: "triangle",
#	3: "rectangle",
#	4: "roundrectangle",
#	5: "bottomroundrectangle",
#	6: "cutrectangle",
# #       7: "barrel",
#  #      8: "rhomboid",
#   #     9: "diamond",
#    #    10: "pentagon",
#        11: "hexagon",
#        12: "concavehexagon",
#        13: "heptagon",
#        14: "octagon",
#        15: "star",
#        16: "tag"
#  }[int(batchId) % 16]
#  return shape


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
   import csv
   import io

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
