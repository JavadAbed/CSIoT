from core.common import get_conn
import math

MESSAGE_FRIENDSHIP_INIT = 100
MESSAGE_FRIENDSHIP_ACCEPTED = 101
MESSAGE_FRIENDSHIP_TERMINATE = 102
CONSUME_SERVICE_FRIEND = 200
CONSUME_SERVICE_FRIEND_FRIEND = 210
CONSUME_SERVICE_FRIEND_FRIEND_FRIEND = 220

def start(numberOfSteps):
   for i in range(numberOfSteps):
       current_ts =find_ts()
       simulate_one_step(current_ts)

def simulate_one_step(current_ts):
   db = get_conn()
   nodes = list( db.agents.find())
   nodes_dic = {node1["name"]:node1 for node1 in nodes}
   # reply message
   for node1 in nodes:
     for node2 in nodes:
       if node1 == node2:
          continue
       # if there is a message j->i at t-1 then respond
       for msg in db.messages.find({"from":node2["name"],"to":node1["name"],"ts":current_ts-1}):
          reply_msg(msg, current_ts, node1, node2)

   # friendship
   for node1 in find_nodes_friendship(nodes):
     for node2 in find_nodes_friendship_for_node(nodes,node1):
       if node1 == node2:
          continue
       if is_friend(node1,node2):
          change_friendship_level(current_ts,node1,node2)
       else:
          if is_first_relation(node1,node2):
              trying_frienship(current_ts,node1,node2)

   # service
   for node in find_nodes_services(nodes):
     for service in [srv[0] for srv in node["service_need"].items() if srv[1] is None]:
        found = False
        for fshipk,fshipv in sorted(node["friendships"].items(), key=lambda x: x[1]["strength"] * -1):
           node2 = nodes_dic[fshipk]
           if service in node2["service_offer"]:
                consume_service(current_ts,node1, node2, service,CONSUME_SERVICE_FRIEND)
                found = True
                break
        if found:
           break
        for fshipk2,fshipv2 in sorted(node["friendships"].items(), key=lambda x: x[1]["strength"] * -1):
           node2 = nodes_dic[fshipk2]
           for fshipk3,fshipv3 in sorted(node2["friendships"].items(), key=lambda x: x[1]["strength"] * -1):
              node3 = nodes_dic[fshipk3]
              if service in node3["service_offer"]:
                   consume_service(current_ts,node1, node3, service,CONSUME_SERVICE_FRIEND_FRIEND)
                   found = True
                   break
           if found:
               break
        if found:
           break
        for fshipk2,fshipv2 in sorted(node["friendships"].items(), key=lambda x: x[1]["strength"] * -1):
           node2 = nodes_dic[fshipk2]
           for fshipk3,fshipv3 in sorted(node2["friendships"].items(), key=lambda x: x[1]["strength"] * -1):
              node3 = nodes_dic[fshipk3]
              for fshipk4,fshipv4 in sorted(node3["friendships"].items(), key=lambda x: x[1]["strength"] * -1):
                node4 = nodes_dic[fshipk4]
                if service in node4["service_offer"]:
                   consume_service(current_ts,node1, node4, service,CONSUME_SERVICE_FRIEND_FRIEND_FRIEND)
                   found = True
                   break
              if found:
                  break
           if found:
               break


def find_nodes_friendship(nodes):
    return nodes

def find_nodes_friendship_for_node(nodes,node1):
    return nodes

def find_nodes_services(nodes):
    return nodes

def consume_service(current_ts,node1, node2, service, type):
   send_msg(current_ts,node1,node2,type,"",service)
   db = get_conn()
   db.agents.find_one_and_update({"name":node1["name"]},{"$set":{"service_need."+service : node2["name"]}})

def find_ts(do_update=True):
   db = get_conn()
   lastmsg = db.vars.find({},{"ts"})
   if lastmsg.count() == 0:
      db.vars.insert({"ts":0})
      current_ts = 0
   else:
      current_ts = lastmsg.next()["ts"]
   if do_update:
       db.vars.find_one_and_update({},{"$inc":{"ts":1}})
   return current_ts

def reset_ts():
   db = get_conn()
   db.vars.find_one_and_update({},{"$set":{"ts":0}})

def reply_msg(msg, current_ts, node1, node2):
   if msg["msg_type"] == MESSAGE_FRIENDSHIP_INIT:
      mm = []
      if node1["owner"] == node2["owner"]:
         mm.append( "owner" )
      if  node1["batch"] == node2["batch"]:
         mm.append( "batch" )
      if distance(node1,node2) < node1["locality"]:
         mm.append( "distance" )
      if len(mm)>0:
          send_msg(current_ts,node1,node2,MESSAGE_FRIENDSHIP_ACCEPTED,"|".join(mm))
          start_friendship(current_ts, node1, node2)
   if msg["msg_type"] == MESSAGE_FRIENDSHIP_ACCEPTED:
      start_friendship(current_ts, node1, node2)
   if msg["msg_type"] == MESSAGE_FRIENDSHIP_TERMINATE:
      terminate_friendship(node1, node2)


def is_friend(node1,node2):
   fs = node1.get("friendships")
   return fs.get(node2["name"]) is not None

def is_first_relation(node1,node2):
   db = get_conn()
   return db.messages.count({"from":node1["name"],"to":node2["name"],"msg_type":MESSAGE_FRIENDSHIP_INIT})==0

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
   fship = node1["friendships"].get(node2["name"])
   if fship is not None:
       if fship["ts_start"] - current_ts > 30:
           if  node2["qos"] + node2["qoi"] + node2["qod"] + node2["availability"] > 20:
               update_friendship_strength(current_ts,node1,node2,ship["strength"] +1 )
           else:
               update_friendship_strength(current_ts,node1,node2,ship["strength"] -1 )

def start_friendship(current_ts, node1, node2):
   if not is_friend(node1,node2):
      db = get_conn()
      db.agents.find_one_and_update({"_id":node1["_id"]},
		{"$set":{ "friendships."+ node2["name"]:  {"ts_start":current_ts,"strength":1}}})
      db.agents.find_one_and_update({"_id":node1["_id"]},
		{"$push":{ "friendships_h."+ node2["name"]:  {"ts":current_ts,"strength":1}}})

def update_friendship_strength(current_ts,node1,node2,strength):
   if strength > 5:
      return
   db = get_conn()
   if strength == 0:
      # terminate friendship
      terminate_friendship(node1,node2)
      send_msg(current_ts,node1,node2,MESSAGE_FRIENDSHIP_TERMINATE,"")
   else:
      # update friendship
      db.agents.find_one_and_update({"name":node1["name"]},{"$push":{"friendships_h."+node2["name"], {"ts":current_ts,"strength":strength}}})
      db.agents.find_one_and_update({"name":node1["name"]},{"$set":{"friendships."+node2["name"]+".strength" : strength}})

def terminate_friendship(node1, node2):
    db = get_conn()
    db.agents.find_one_and_update({"name":node1["name"]},{"$push":{"friendships_h."+node2["name"], {"ts":current_ts,"strength":0 }}})
    db.agents.find_one_and_update({"name":node1["name"]},{"$unset":{"friendships."+node2["name"] : ""}})

def last_messages(number):
    db = get_conn()
    data = []
    for msg in list(db.messages.find().sort("$natural",-1).limit(number)):
       data.append({
              "from":msg["from"],
              "to": msg["to"],
              "ts":msg["ts"],
              "type": {
                100: "FRIENDSHIP_INIT",
                101: "FRIENDSHIP_ACCEPTED",
                102: "FRIENDSHIP_TERMINATE"
                    }[msg["msg_type"]],
              "extra":msg.get("extra")
          })
    return data


def clear_all_messages():
   db = get_conn()
   db.messages.delete_many({})


def logs_for_ts(numberOfSteps):
   db = get_conn()
   ts = find_ts(do_update=False)
   data = []
   for i in range(int(numberOfSteps)):
          for msg in list(db.messages.find({"ts":ts-i})):
                data.append({
                    "from":msg["from"],
                    "to": msg["to"],
                    "ts":msg["ts"],
                    "type": {
                        100: "FRIENDSHIP_INIT",
                        101: "FRIENDSHIP_ACCEPTED",
                        102: "FRIENDSHIP_TERMINATE"
                      }[msg["msg_type"]],
                    "extra":msg.get("extra")
                 })
   return data
