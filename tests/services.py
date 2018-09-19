import unittest
from core import app,agent,simulation
from core.common import get_conn

class ServicesTestCase(unittest.TestCase):

   def test_consume_f(self):
      """consume friend services test"""
      agent.deleteAll()
      simulation.clear_all_messages()
      simulation.reset_ts()

      a = agent.random_agent()
      b = agent.random_agent()

      a["agentName"] = "a"
      a["agentX"] = str(100)
      a["agentY"] = str(100)
      a["agentOwner"] = str(50)
      a["agentBatch"] = str(50)
      a["agentLocality"] = str(100)

      b["agentName"] = "b"
      b["agentX"] = str(450)
      b["agentY"] = str(100)
      b["agentOwner"] = str(50)
      b["agentBatch"] = str(51)
      b["agentLocality"] = str(100)

      agent.new_agent(0,a)
      agent.new_agent(0,b)
      db = get_conn()

      db.agents.find_one_and_update({"name":"a"},{"$set":{"service_need":{"10":None}}})
      db.agents.find_one_and_update({"name":"b"},{"$set":{"service_offer":["10"]}})

      simulation.start(3)

      ag = {a["name"]:a for a in db.agents.find()}

      self.assertTrue( "a" in ag["b"]["friendships"])
      self.assertTrue( "b" in ag["a"]["friendships"])
      self.assertTrue( "b" == ag["a"]["service_need"]["10"])

   def test_consume_ff(self):
      """consume friend of friends services test"""
      agent.deleteAll()
      simulation.clear_all_messages()
      simulation.reset_ts()

      a = agent.random_agent()
      b = agent.random_agent()
      c = agent.random_agent()

      a["agentName"] = "a"
      a["agentX"] = str(100)
      a["agentY"] = str(100)
      a["agentOwner"] = str(50)
      a["agentBatch"] = str(50)
      a["agentLocality"] = str(100)

      b["agentName"] = "b"
      b["agentX"] = str(450)
      b["agentY"] = str(100)
      b["agentOwner"] = str(50)
      b["agentBatch"] = str(51)
      b["agentLocality"] = str(100)

      c["agentName"] = "c"
      c["agentX"] = str(950)
      c["agentY"] = str(100)
      c["agentOwner"] = str(52)
      c["agentBatch"] = str(51)
      c["agentLocality"] = str(50)

      agent.new_agent(0,a)
      agent.new_agent(0,b)
      agent.new_agent(0,c)
      db = get_conn()
      db.agents.find_one_and_update({"name":"a"},{"$set":{"service_need":{"10":None}}})
      db.agents.find_one_and_update({"name":"a"},{"$set":{"service_offer":["5"]}})
      db.agents.find_one_and_update({"name":"b"},{"$set":{"service_need":{"20":None}}})
      db.agents.find_one_and_update({"name":"b"},{"$set":{"service_offer":["11"]}})
      db.agents.find_one_and_update({"name":"c"},{"$set":{"service_need":{"12":None}}})
      db.agents.find_one_and_update({"name":"c"},{"$set":{"service_offer":["10"]}})

      simulation.start(3)

      ag = {a["name"]:a for a in db.agents.find()}
      print(ag)

      self.assertTrue( "a" in ag["b"]["friendships"])
      self.assertTrue( "b" in ag["a"]["friendships"])
      self.assertTrue( "c" in ag["b"]["friendships"])
      self.assertTrue( "c" == ag["a"]["service_need"]["10"])


   def test_consume_fff(self):
      """consume friend of friend of friends services test"""
      agent.deleteAll()
      simulation.clear_all_messages()
      simulation.reset_ts()

      a = agent.random_agent()
      b = agent.random_agent()
      c = agent.random_agent()
      d = agent.random_agent()

      a["agentName"] = "a"
      a["agentX"] = str(100)
      a["agentY"] = str(100)
      a["agentOwner"] = str(50)
      a["agentBatch"] = str(50)
      a["agentLocality"] = str(100)

      b["agentName"] = "b"
      b["agentX"] = str(450)
      b["agentY"] = str(100)
      b["agentOwner"] = str(50)
      b["agentBatch"] = str(51)
      b["agentLocality"] = str(100)

      c["agentName"] = "c"
      c["agentX"] = str(950)
      c["agentY"] = str(100)
      c["agentOwner"] = str(52)
      c["agentBatch"] = str(51)
      c["agentLocality"] = str(50)

      d["agentName"] = "d"
      d["agentX"] = str(950)
      d["agentY"] = str(400)
      d["agentOwner"] = str(52)
      d["agentBatch"] = str(54)
      d["agentLocality"] = str(50)

      agent.new_agent(0,a)
      agent.new_agent(0,b)
      agent.new_agent(0,c)
      agent.new_agent(0,d)
      db = get_conn()
      db.agents.find_one_and_update({"name":"a"},{"$set":{"service_need":{"10":None}}})
      db.agents.find_one_and_update({"name":"a"},{"$set":{"service_offer":["5"]}})
      db.agents.find_one_and_update({"name":"b"},{"$set":{"service_need":{"20":None}}})
      db.agents.find_one_and_update({"name":"b"},{"$set":{"service_offer":["11"]}})
      db.agents.find_one_and_update({"name":"c"},{"$set":{"service_need":{"12":None}}})
      db.agents.find_one_and_update({"name":"c"},{"$set":{"service_offer":["13"]}})
      db.agents.find_one_and_update({"name":"d"},{"$set":{"service_need":{"15":None}}})
      db.agents.find_one_and_update({"name":"d"},{"$set":{"service_offer":["10"]}})

      simulation.start(3)

      ag = {a["name"]:a for a in db.agents.find()}

      self.assertTrue( "a" in ag["b"]["friendships"])
      self.assertTrue( "b" in ag["a"]["friendships"])
      self.assertTrue( "c" in ag["b"]["friendships"])
      self.assertTrue( "d" in ag["c"]["friendships"])
      self.assertTrue( "d" == ag["a"]["service_need"]["10"])


