import unittest
from core import app,agent,simulation
from core.common import get_conn

class PlaybackTestCase(unittest.TestCase):

   def test_add_agent(self):
      pass
      agent.deleteAll()
      simulation.clear_all_messages()
      simulation.reset_ts()

      a = agent.random_agent()
      b = agent.random_agent()
      c = agent.random_agent()

      a["agentName"] = "a"
      b["agentName"] = "b"
      c["agentName"] = "c"

      agent.new_agent(0,a)
      agent.new_agent(5,b)
      agent.new_agent(10,c)

      data1 = agent.agents(10,0);
      data2 = agent.agents(10,3);
      data3 = agent.agents(10,5);
      data4 = agent.agents(10,7);
      data5 = agent.agents(10,10);
      data6 = agent.agents(10,12);

      data1 = [x["data"]["id"] for x in data1["data"] if "locality" in x["data"] ]
      data2 = [x["data"]["id"] for x in data2["data"] if "locality" in x["data"] ]
      data3 = [x["data"]["id"] for x in data3["data"] if "locality" in x["data"] ]
      data4 = [x["data"]["id"] for x in data4["data"] if "locality" in x["data"] ]
      data5 = [x["data"]["id"] for x in data5["data"] if "locality" in x["data"] ]
      data6 = [x["data"]["id"] for x in data6["data"] if "locality" in x["data"] ]

      self.assertIn(   "a", data1 )
      self.assertNotIn("b", data1 )
      self.assertNotIn("c", data1 )
      self.assertIn(   "a", data2 )
      self.assertNotIn("b", data2 )
      self.assertNotIn("c", data2 )
      self.assertIn(   "a", data3 )
      self.assertIn(   "b", data3 )
      self.assertNotIn("c", data3 )
      self.assertIn(   "a", data4 )
      self.assertIn(   "b", data4 )
      self.assertNotIn("c", data4 )
      self.assertIn(   "a", data5 )
      self.assertIn(   "b", data5 )
      self.assertIn(   "c", data5 )
      self.assertIn(   "a", data6 )
      self.assertIn(   "b", data6 )
      self.assertIn(   "c", data6 )


   def test_frienships(self):
      pass
      agent.deleteAll()
      simulation.clear_all_messages()
      simulation.reset_ts()

      a = agent.random_agent()
      b = agent.random_agent()
      c = agent.random_agent()

      a["agentName"] = "a"
      a["agentOwner"] = str(50)
      b["agentName"] = "b"
      b["agentOwner"] = str(50)
      c["agentName"] = "c"
      c["agentOwner"] = str(50)

      agent.new_agent(0,a)
      simulation.start(5)
      agent.new_agent(5,b)
      simulation.start(5)
      agent.new_agent(10,c)
      simulation.start(5)

      data1 = agent.agents(15,0);
      data2 = agent.agents(15,3);
      data3 = agent.agents(15,5);
      data4 = agent.agents(15,7);
      data5 = agent.agents(15,10);
      data6 = agent.agents(15,12);
      data7 = agent.agents(15,15);

      data1 = [x["data"]["id"] for x in data1["data"] ]
      data2 = [x["data"]["id"] for x in data2["data"] ]
      data3 = [x["data"]["id"] for x in data3["data"] ]
      data4 = [x["data"]["id"] for x in data4["data"] ]
      data5 = [x["data"]["id"] for x in data5["data"] ]
      data6 = [x["data"]["id"] for x in data6["data"] ]
      data7 = [x["data"]["id"] for x in data7["data"] ]

      self.assertIn(   "a", data1 )
      self.assertNotIn("b", data1 )
      self.assertNotIn("c", data1 )
      self.assertNotIn("a-b", data1 )
      self.assertNotIn("a-c", data1 )
      self.assertNotIn("b-c", data1 )
      self.assertIn(   "a", data2 )
      self.assertNotIn("b", data2 )
      self.assertNotIn("c", data2 )
      self.assertNotIn("a-b", data2 )
      self.assertNotIn("a-c", data2 )
      self.assertNotIn("b-c", data2 )
      self.assertIn(   "a", data3 )
      self.assertIn(   "b", data3 )
      self.assertNotIn("c", data3 )
      self.assertNotIn("a-b", data3 )
      self.assertNotIn("a-c", data3 )
      self.assertNotIn("b-c", data3 )
      self.assertIn(   "a", data4 )
      self.assertIn(   "b", data4 )
      self.assertNotIn("c", data4 )
      self.assertIn(   "a-b", data4 )
      self.assertNotIn("a-c", data4 )
      self.assertNotIn("b-c", data4 )
      self.assertIn(   "a", data5 )
      self.assertIn(   "b", data5 )
      self.assertIn(   "c", data5 )
      self.assertIn(   "a-b", data5 )
      self.assertNotIn("a-c", data5 )
      self.assertNotIn("b-c", data5 )
      self.assertIn(   "a", data6 )
      self.assertIn(   "b", data6 )
      self.assertIn(   "c", data6 )
      self.assertIn(   "a-b", data6 )
      self.assertIn(   "a-c", data6 )
      self.assertIn(   "b-c", data6 )
      self.assertIn(   "a", data7 )
      self.assertIn(   "b", data7 )
      self.assertIn(   "c", data7 )
      self.assertIn(   "a-b", data7 )
      self.assertIn(   "a-c", data7 )
      self.assertIn(   "b-c", data7 )

