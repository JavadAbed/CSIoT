from flask import session, redirect, url_for, render_template
from core import app,agent
from core.common import WebException, error_get_message, WebSuccess
from core.annotations import make_params, api_wrapper



# @app.errorhandler(RequireLoginException)
# def handle_login_required(exception):
#     return redirect(url_for("login_page"))


@app.route('/', methods=['GET'])
def index_page():
    return render_template("index.html")

@app.route('/newAgent', methods=['POST'])
@api_wrapper
@make_params
def new_agent(params):
   agent.new_agent(params);
   return WebSuccess();



@app.route('/uploadAgent', methods=['POST'])
@api_wrapper
def upload_agent():
   f = request.files['file']
   agent.upload_agent(f)
   return WebSuccess();


