""" API annotations and assorted wrappers. """

import json
import traceback
import core

from core.common import WebSuccess, WebError, WebException, InternalException, SevereInternalException
from core.common import validate, flat_multi, error_get_message
from datetime import datetime
from functools import wraps
from flask import session, request, abort, Response, redirect, url_for, render_template



def log_action(f):
    """
    Logs a given request if available.
    """

    @wraps(f)
    def wrapper(*args, **kwds):
        """
        Provides contextual information to the logger.
        """

        log_information = {
            "name": "{}.{}".format(f.__module__, f.__name__),
            "args": args,
            "kwargs": kwds,
            "result": None,
        }

        try:
            log_information["result"] = f(*args, **kwds)
        except WebException as error:
            log_information["exception"] = error_get_message(error)
            raise
        finally:
            core.logger.info(log_information)

        return log_information["result"]

    return wrapper


def api_wrapper(f):
    """
    Wraps api routing and handles potential exceptions
    """

    @wraps(f)
    def wrapper(*args, **kwds):
        
        web_result = {}
        try:
            web_result = f(*args, **kwds)
            if type(web_result) is not dict or "status" not in web_result:
                web_result = WebSuccess(
                    message="Action performed successfully", data=web_result)
        except WebException as error:
            web_result = WebError(error_get_message(error), error.data)
        except InternalException as error:
            message = error_get_message(error)
            if type(error) == SevereInternalException:
                core.logger.critical(traceback.format_exc())
                web_result = WebError(
                    "There was a critical internal error. Contact an administrator.")
            else:
                core.logger.error(traceback.format_exc())
                web_result = WebError(message)
        except Exception as error:
            core.logger.error(traceback.format_exc())

        return Response(json.dumps(web_result), content_type='appication/json')

    return wrapper


def make_params(f):
    """
    Wraps routing functions that require a user to be an admin
    """

    @wraps(f)
    def wrapper(*args, **kwds):
        params = flat_multi(request.values)
        return f(params)
    return wrapper


def validation(schema): 

    def true_decorator(f):
        
        @wraps(f)
        def wrapped(*args, **kwargs): 
            validate(schema, args[0])
            return f(*args, **kwargs)
        return wrapped
    return true_decorator
 
