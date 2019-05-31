#!/usr/bin/python3

from core.config import run
from core import app

app.run(debug=run["debug"], threaded=run["threaded"], host=run["host"], port=run["port"])
