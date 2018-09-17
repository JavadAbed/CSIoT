import unittest
from core import app,agent,simulation
from core.common import get_conn

class FriendshipTestCase(unittest.TestCase):

   def test_locality(self):
      """locality test: two node in locale should be friend after 2 step"""
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
      b["agentX"] = str(150)
      b["agentY"] = str(100)
      b["agentOwner"] = str(51)
      b["agentBatch"] = str(51)
      b["agentLocality"] = str(100)

      c["agentName"] = "c"
      c["agentX"] = str(350)
      c["agentY"] = str(100)
      c["agentOwner"] = str(52)
      c["agentBatch"] = str(52)
      c["agentLocality"] = str(50)

      agent.new_agent(0,a)
      agent.new_agent(0,b)
      agent.new_agent(0,c)

      simulation.start(2)

      db = get_conn()
      ag = {a["name"]:a for a in db.agents.find()}

      self.assertTrue( "a" in ag["b"]["friendships"])
      self.assertTrue( "b" in ag["a"]["friendships"])
      self.assertTrue( "c" not in ag["a"]["friendships"])
      self.assertTrue( "c" not in ag["b"]["friendships"])

   def test_owner(self):
      """owner test: two node with same owner should be friend after 2 step"""
      agent.deleteAll()
      simulation.clear_all_messages()
      simulation.reset_ts()

      a = agent.random_agent()
      b = agent.random_agent()

      a["agentName"] = "a"
      a["agentX"] = str(150)
      a["agentY"] = str(100)
      a["agentOwner"] = str(50)
      a["agentBatch"] = str(53)
      a["agentLocality"] = str(50)

      b["agentName"] = "b"
      b["agentX"] = str(950)
      b["agentY"] = str(100)
      b["agentOwner"] = str(50)
      b["agentBatch"] = str(52)
      b["agentLocality"] = str(50)

      agent.new_agent(0,a)
      agent.new_agent(0,b)

      simulation.start(2)

      db = get_conn()
      ag = {a["name"]:a for a in db.agents.find()}

      self.assertTrue( "a" in ag["b"]["friendships"])
      self.assertTrue( "b" in ag["a"]["friendships"])

   def test_batch(self):
      """batch test: two node with same batchId should be friend after 2 step"""
      agent.deleteAll()
      simulation.clear_all_messages()
      simulation.reset_ts()

      a = agent.random_agent()
      b = agent.random_agent()

      a["agentName"] = "a"
      a["agentX"] = str(150)
      a["agentY"] = str(100)
      a["agentOwner"] = str(53)
      a["agentBatch"] = str(50)
      a["agentLocality"] = str(50)

      b["agentName"] = "b"
      b["agentX"] = str(950)
      b["agentY"] = str(100)
      b["agentOwner"] = str(52)
      b["agentBatch"] = str(50)
      b["agentLocality"] = str(50)


      agent.new_agent(0,a)
      agent.new_agent(0,b)

      simulation.start(2)

      db = get_conn()
      ag = {a["name"]:a for a in db.agents.find()}

      self.assertTrue( "a" in ag["b"]["friendships"])
      self.assertTrue( "b" in ag["a"]["friendships"])

   def test_frienship_change(self):
      """Frienship change: if a+b+c+d is more than 20 frienship strength gets increased and if it is less than 20 gets decreased"""
      agent.deleteAll()
      simulation.clear_all_messages()
      simulation.reset_ts()

      a = agent.random_agent()
      b = agent.random_agent()

      a["agentName"] = "a"
      a["agentX"] = str(150)
      a["agentY"] = str(100)
      a["agentOwner"] = str(53)
      a["agentBatch"] = str(50)
      a["agentLocality"] = str(50)

      b["agentName"] = "b"
      b["agentX"] = str(950)
      b["agentY"] = str(100)
      b["agentOwner"] = str(52)
      b["agentBatch"] = str(50)
      b["agentLocality"] = str(50)


      agent.new_agent(0,a)
      agent.new_agent(0,b)

      simulation.start(2)

      db = get_conn()
      ag = {a["name"]:a for a in db.agents.find()}

      self.assertTrue( "a" in ag["b"]["friendships"])
      self.assertTrue( "b" in ag["a"]["friendships"])

      db.agents.find_one_and_update({"name":"a"},{"$set":{"qoi":5,"qos":5,"qod":5,"availability":5}})
      db.agents.find_one_and_update({"name":"b"},{"$set":{"qoi":5,"qos":5,"qod":5,"availability":5}})
      simulation.start(30)
      ag = {a["name"]:a for a in db.agents.find()}
      self.assertTrue( ag["b"]["friendships"]["a"]["strength"] == 2)
      self.assertTrue( ag["a"]["friendships"]["b"]["strength"] == 2)
      simulation.start(30)
      ag = {a["name"]:a for a in db.agents.find()}
      self.assertTrue( ag["b"]["friendships"]["a"]["strength"] == 3)
      self.assertTrue( ag["a"]["friendships"]["b"]["strength"] == 3)
      simulation.start(30)
      ag = {a["name"]:a for a in db.agents.find()}
      self.assertTrue( ag["b"]["friendships"]["a"]["strength"] == 4)
      self.assertTrue( ag["a"]["friendships"]["b"]["strength"] == 4)
      simulation.start(30)
      ag = {a["name"]:a for a in db.agents.find()}
      self.assertTrue( ag["b"]["friendships"]["a"]["strength"] == 5)
      self.assertTrue( ag["a"]["friendships"]["b"]["strength"] == 5)
      simulation.start(70)
      ag = {a["name"]:a for a in db.agents.find()}
      self.assertTrue( ag["b"]["friendships"]["a"]["strength"] == 5)
      self.assertTrue( ag["a"]["friendships"]["b"]["strength"] == 5)
      db.agents.find_one_and_update({"name":"a"},{"$set":{"qoi":5,"qos":5,"qod":5,"availability":2}})
      db.agents.find_one_and_update({"name":"b"},{"$set":{"qoi":5,"qos":5,"qod":5,"availability":2}})
      simulation.start(30)
      ag = {a["name"]:a for a in db.agents.find()}
      self.assertTrue( ag["b"]["friendships"]["a"]["strength"] == 4)
      self.assertTrue( ag["a"]["friendships"]["b"]["strength"] == 4)
      simulation.start(30)
      ag = {a["name"]:a for a in db.agents.find()}
      self.assertTrue( ag["b"]["friendships"]["a"]["strength"] == 3)
      self.assertTrue( ag["a"]["friendships"]["b"]["strength"] == 3)
      simulation.start(30)
      ag = {a["name"]:a for a in db.agents.find()}
      self.assertTrue( ag["b"]["friendships"]["a"]["strength"] == 2)
      self.assertTrue( ag["a"]["friendships"]["b"]["strength"] == 2)
      simulation.start(30)
      ag = {a["name"]:a for a in db.agents.find()}
      self.assertTrue( ag["b"]["friendships"]["a"]["strength"] == 1)
      self.assertTrue( ag["a"]["friendships"]["b"]["strength"] == 1)
      simulation.start(30)
      ag = {a["name"]:a for a in db.agents.find()}
      self.assertTrue("a" not in ag["b"]["friendships"])
      self.assertTrue("b" not in ag["a"]["friendships"])




#if __name__ == '__main__':
#    unittest.main()
