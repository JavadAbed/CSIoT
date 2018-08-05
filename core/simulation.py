from core.common import get_conn
import math

MESSAGE_FRIENDSHIP_INIT = 100
MESSAGE_FRIENDSHIP_ACCEPTED = 101

def start(params):
   for i in range(int(params["numberOfSteps"])):
       current_ts =find_ts()
       simulate_one_step(current_ts)

def simulate_one_step(current_ts):
   db = get_conn()
   nodes = list( db.agents.find())
   for node1 in nodes:
     for node2 in nodes:
       if node1 == node2:
          continue
       # if there is a message j->i at t-1 then respond
       for msg in db.messages.find({"from":node2["name"],"to":node1["name"],"ts":current_ts-1}):
          reply_msg(msg, current_ts, node1, node2)
       if is_friend(node1,node2):
          change_friendship_level(current_ts,node1,node2)
       else:
          trying_frienship(current_ts,node1,node2)

def find_ts():
   db = get_conn()
   lastmsg = db.vars.find({},{"ts"})
   if lastmsg.count() == 0:
      db.vars.insert({"ts":0})
      current_ts = 0
   else:
      current_ts = lastmsg.next()["ts"]
   db.vars.find_one_and_update({},{"$inc":{"ts":1}})
   return current_ts

def reply_msg(msg, current_ts, node1, node2):
   if msg["msg_type"] == MESSAGE_FRIENDSHIP_INIT:
      msg = []
      if node1["owner"] == node2["owner"]:
         msg.append( "owner" )
      if  node1["batch"] == node2["batch"]:
         msg.append( "batch" )
      if distance(node1,node2) < node1["locality"]:
         msg.append( "distance" )
      if len(msg)>0:
          send_msg(current_ts,node1,node2,MESSAGE_FRIENDSHIP_ACCEPTED)
          start_friendship(current_ts, node1, node2,"|".join(msg))
   if msg["msg_type"] == MESSAGE_FRIENDSHIP_ACCEPTED:
      msg = []
      if node1["owner"] == node2["owner"]:
         msg.append( "owner" )
      if  node1["batch"] == node2["batch"]:
         msg.append( "batch" )
      if distance(node1,node2) < node1["locality"]:
         msg.append( "distance" )
      if len(msg)>0:
          start_friendship(current_ts, node1, node2,"|".join(msg))

def is_friend(node1,node2):
   fs = node1.get("friendships")
   if fs is None:
      return False
   return fs.get(node2["name"]) is not None

def trying_frienship(current_ts,node1,node2):
   msg = []
   if node1["owner"] == node2["owner"]:
      msg.append( "owner" )
   if  node1["batch"] == node2["batch"]:
      msg.append( "batch" )
   if distance(node1,node2) < node1["locality"]:
      msg.append( "distance" )

   if len(msg)>0:
     send_msg(current_ts,node1,node2,MESSAGE_FRIENDSHIP_INIT,"|".join(msg))



def distance(node1,node2):
   return  math.sqrt( (node1["x"] - node2["x"])**2 + (node1["y"] - node2["y"])**2 )

def send_msg(current_ts,node1,node2,msg_type,extra):
   db = get_conn()
   db.messages.insert({"from":node1["name"],"to":node2["name"],"ts":current_ts,"msg_type":msg_type,"extra":extra})

def change_friendship_level(current_ts,node1,node2):
   fship = node1.friendships.get(node2["name"])
   if fship is not None:
       if fship["ts_start"] - current_ts > 30:
           if  node2["qos"] + node2["qoi"] + node2["qod"] + node2["availability"] > 20:
               update_friendship_strength(node1,node2["name"],ship["strength"] +1 )
           else:
               update_friendship_strength(node1,node2["name"],ship["strength"] -1 )

def start_friendship(current_ts, node1, node2):
   if not is_friend(node1,node2):
      db = get_conn()
      db.agents.find_one_and_update({"_id":node1["_id"]},
		{"$set":{ "friendships."+ node2["name"]:  {"ts_start":current_ts,"strength":1}}})

def update_friendship_strength(node1,node2_name,strength):
   if strength > 5:
      return
   db = get_conn()
   if strength == 0:
      # terminate friendship
      db.agents.find_one_and_update({"name":node1["name"]},{"$unset":{"friendships."+node2_name : ""}})
   else:
      # update friendship
      db.agents.find_one_and_update({"name":node1["name"]},{"$set":{"friendships."+node2_name+".strength" : strength}})
