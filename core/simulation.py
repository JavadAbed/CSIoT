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
       for msg in db.messages.find({"from":node2["name"],"to":node1["name"],"ts":current_ts-1}):
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
      send_mag(current_ts,node1,node2,MESSAGE_FRIENDSHIP_ACCEPTED)
      start_friendship(current_ts, node1, node2)

def is_friend(node1,node2):
   for friendship in node1.friendships:
       if friendship["name"] == node2["name"]:
           return True
   return False

def trying_frienship(current_ts,node1,node2):
   if node1["owner"] == node2["owner"] or node1["batch"] == node2["batch"] or distance(node1,node2) < 100:
     send_mag(current_ts,node1,node2,MESSAGE_FRIENDSHIP_INIT)

def distance(node1,node2):
   return  math.sqrt( (node1["x"] - node2["x"])**2 + (node1["y"] - node2["y"])**2 )

def send_mag(current_ts,node1,node2,msg_type):
   db = get_conn()
   db.messages.insert({"from":node1["name"],"to":node2["name"],"ts":current_ts,"msg_type":msg_type})

def change_friendship_level(current_ts,node1,node2,friendship):
   pass

def start_friendship(current_ts, node1, node2):
   if is_friend(node1,node2) is None:
      db.agents.find_one_and_update({"_id":node1["_id"]},{"$push":{ "friendships":  {"node2":node2["name"],"ts_start":current_ts,"strength":1})
