import pymongo
import csv
import io
from core.common import get_conn
from core.common import  WebException
from random import *

def random_agent():
   return {
	"agentName": str( randint(1,10000)),
        "agentOwner": str( randint(1,100)),
        "agentBatch": str( randint(1,10000)),
 	"agentLocality": str( randint(2,17)*10),
	"agentX": str( randint(1,2000)),
	"agentY": str( randint(1,2000)),
	"agentFriendsH": ",".join([str(randint(1,100)) for x in range(randint(1,10)) ]),
	"agentFriendsM": ",".join([str(randint(1,100)) for x in range(randint(1,10)) ]),
	"agentFriendsL": ",".join([str(randint(1,100)) for x in range(randint(1,10)) ])
   }
def new_agent(ts, params):
  db = get_conn()
  # validate, agent name not empty
  if len(params["agentName"].strip()) == 0:
     raise WebException("Agent name is empty")
  # validate, agent name must be uniq
  old = db.agents.find({"name": params["agentName"]})
  if old.count()>0:
     raise WebException("Agent with identical name already exists.")

  service_need = {str(randint(0,100)):None for x in range(4)}
  service_offer = [str(randint(0,100)) for x in range(4)]

  agent ={
    "name": params["agentName"],
    "owner": params["agentOwner"],
    "batch": params["agentBatch"],
    "locality": float(params["agentLocality"]),
    "ts_added": ts,
    "x": float( params["agentX"]),
    "y": float(params["agentY"]),
    "friends_h": params["agentFriendsH"].split('-'),
    "friends_m": params["agentFriendsM"].split('-'),
    "friends_l": params["agentFriendsL"].split('-'),
    "qoi" : randint(0,10),
    "qod" : randint(0,10),
    "qos" : randint(0,10),
    "availability" : randint(0,10),
    "friendships": {},
    "friendships_h": {},
    "service_need": service_need,
    "service_offer": service_offer
  }
  db.agents.insert(agent)
  return agents(ts,ts)

def deleteAll():
   db = get_conn()
   db.agents.delete_many({})

def upload_agent(file):
  in_memory_file = io.BytesIO()
  file.save(in_memory_file)
  reader = csv.reader(file)
  for row in reader:
     print(row)
  pass # TOD O

def agents(ts_real, ts_requested):
  if ts_requested is None:
    ts_requested = ts_real
  ts_requested = int(ts_requested)
  db = get_conn()
  agents = list(db.agents.find({"ts_added": {"$lte": ts_requested} }))
  data = []
  for agent in agents:
     agent.pop('_id')
     data.append({"data": {"id": agent["name"], "locality":agent.get("locality"),"obj":agent },
		"position": {"x": agent["x"],"y":agent["y"] }    })
     for fshipk,fshipv_a in agent["friendships_h"].items() :
         tmp = [x for x in fshipv_a if x["ts"]<=ts_requested ]
         if len(tmp)==0: continue
         fshipv = tmp[-1]
         # average:
         skip_me = False
         for d in data:
             if d["data"].get("source") == fshipk and d["data"].get("target") == agent["name"]:
                skip_me = True
                break
         if skip_me:
             continue
         for agent2 in agents:
             if agent2["name"] == fshipk:
                score2 = agent2["friendships_h"][agent["name"]][-1]["strength"]
         #
         data.append({"data":{"id": agent["name"]+"-"+fshipk ,"source":agent["name"], "target":fshipk, "strength": (int(fshipv["strength"])+int(score2)) / 2 }})
  return {"data": data, "ts_real": ts_real, "ts_requested":ts_requested}

def makeCSVString():
   db = get_conn() # TOD O update 
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
