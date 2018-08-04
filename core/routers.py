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
   data = agent.new_agent(params);
   return WebSuccess(data = data);



@app.route('/uploadAgent', methods=['POST'])
@api_wrapper
def upload_agent():
   f = request.files['file']
   agent.upload_agent(f)
   return WebSuccess();


@app.route('/agents', methods=['GET'])
@api_wrapper
def agents():
   agents = agent.agents();
   return WebSuccess(data = agents);

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
    simulation.start(params)
    agents = agent.agents();
    return WebSuccess(data = agents);
