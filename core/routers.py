from flask import session, redirect, url_for, render_template, Response, request
from core import app,agent,simulation
from core.common import WebException, error_get_message, WebSuccess
from core.annotations import make_params, api_wrapper


@app.route('/', methods=['GET'])
def index_page():
    return render_template("index.html")

@app.route('/newAgent', methods=['POST'])
@api_wrapper
@make_params
def new_agent(params):
   ts = simulation.find_ts(do_update=False)
   data = agent.new_agent(ts,params)
   return WebSuccess(data = data)

@app.route('/uploadAgent', methods=['POST'])
@api_wrapper
def upload_agent():
   f = request.files['file']
   agent.upload_agent(f)
   return WebSuccess();


@app.route('/agents', methods=['GET'])
@api_wrapper
@make_params
def agents(params):
   ts_real = simulation.find_ts(do_update=False)
   ts_requested = params.get("ts")
   data = agent.agents(ts_real,ts_requested);
   return WebSuccess(data = data);

@app.route('/exportData', methods=['GET'])
def export_agents():
   csv = agent.makeCSVString()
   return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=agents.csv"})

@app.route('/startSimulation', methods=['POST'])
@api_wrapper
@make_params
def start_simulation(params):
    numberOfSteps = int(params["numberOfSteps"])
    simulation.start(numberOfSteps)
    ts = simulation.find_ts(do_update=False)
    agents = agent.agents(ts,ts);
    #logs = simulation.logs_for_ts(params["numberOfSteps"])
    return WebSuccess(data = agents )

@app.route('/deleteAll', methods=['POST'])
@api_wrapper
def delete_all():
    agent.deleteAll()
    simulation.clear_all_messages()
    simulation.reset_ts()
    agents = agent.agents(0,0)
    return WebSuccess(data = agents);

@app.route('/lastMessages', methods=['GET'])
@api_wrapper
def last_messages():
    return WebSuccess(data= simulation.last_messages(1000))
