import unittest
from core import app,agent,simulation
from core.common import get_conn

class SomeTestCase(unittest.TestCase):
   """locality test: two node in locale should be friend after 1 step"""

   def test_1(self):
      agent.deleteAll()
      simulation.clear_all_messages()
      simulation.reset_ts()

      a = agent.random_agent()
      b = agent.random_agent()
      c = agent.random_agent()

      a["agentName"] = "a"
      a["agentX"] = str(100)
      a["agentY"] = str(100)
      a["agentLocality"] = str(100)

      b["agentName"] = "b"
      b["agentX"] = str(150)
      b["agentY"] = str(100)
      b["agentLocality"] = str(100)

      c["agentName"] = "c"
      c["agentX"] = str(350)
      c["agentY"] = str(100)
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

#if __name__ == '__main__':
#    unittest.main()
