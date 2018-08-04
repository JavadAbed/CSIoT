from core.common import get_conn
import math

MESSAGE_FRIENDSHIP_INIT = 100
MESSAGE_FRIENDSHIP_ACCEPTED = 101

def start(params):
   current_ts = find_ts()
   for i in range(params["numberOfSteps"]):
       simulate_one_step(current_ts+i)

def simulate_one_step(current_ts):
   nodes = db.agents.find()
   for node1 in nodes:
     for node2 in nodes:
       if node1 == node2:
          break
       # if there is a message j->i at t-1 then respond
       for msg in db.messages.find({"from":node2["agentName"],"to":node1["agentName"],"ts":current_ts-1}):
          reply_msg(msg, current_ts, node1, node2)
       friendship = is_friend(node1,node2)
       if friendship is not None:
          change_friendship_level(current_ts,node1,node2,friendship)
       else:
          trying_frienship(current_ts,node1,node2)

def find_ts():
   db = get_conn()
   lastmsg = db.messages.find().limit(1).sort("{$natural:-1}")
   if lastmsg.count() == 0:
      current_ts = 0
   else:
      current_ts = lastmsg["ts"]
   return current_ts

def reply_msg(msg, current_ts, node1, node2):
   if msg["msg_type"] == MESSAGE_FRIENDSHIP_INIT:
      send_mag(current_ts,node1,node2,MESSAGE_FRIENDSHIP_ACCEPTED,1)
      start_friendship(current_ts, node1, node2)

def is_friend(node1,node2):
   db = get_conn()
   friendship = db.friends.find({"$or":[{"node1":node1["agentName"], "node2":node2["agentName"]},{"node1":node1["agentName"], "node2":node2["agentName"]}], "ts_finish":-1})
   if friendship.count() > 0:
      return friendship.next()
   else:
      return None

def trying_frienship(current_ts,node1,node2):
   if node1["agentOwner"] == node2["agentOwner"] or node1["agentBatch"] == node2["agentBatch"] or distance(node1,node2) < 100:
     send_mag(current_ts,node1,node2,MESSAGE_FRIENDSHIP_INIT,0)

def distance(node1,node2):
   return 2000 *  math.sqrt( (node1["agentX"] - node2["agentX"])**2 + (node1["agentY"] - node2["agentY"])**2 )

def send_mag(current_ts,node1,node2,msg_type,is_reply):
   db = get_conn()
   db.messages.insert({"from":node1["agentName"],"to":node2["agentName"],"is_reply":is_reply,"ts":current_ts,"msg_type":msg_type})

def change_friendship_level(current_ts,node1,node2,friendship):
   pass

def start_friendship(current_ts, node1, node2):
   if is_friend(node1,node2) is None:
      db.friends.insert({"node1":node1["agentName"], "node2":node2["agentName"],"ts_start":current_ts,"ts_finish":-1,"strength":1})
