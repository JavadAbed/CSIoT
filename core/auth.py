from flask import session, url_for
from core.models import User, Account, OTP, Option, Card
from core.common import check, WebException, random_digits, hash, mask_phone, check_password, build_password
from voluptuous import Required, Length, Schema
from core.annotations import log_action, validation, transaction
from core.utils import send_sms
from core import db


login_schema = Schema({
    Required('password'):
        check(("Passwords must be between 3 and 20 characters.", [str, Length(min=3, max=20)])
              )
}, extra=True)

register_schema = Schema({
    Required('username'): check(
        ("Usernames must be between 3 and 20 characters.",
         [str, Length(min=3, max=20)])
    ),
    Required('password'):
        check(("Passwords must be between 3 and 20 characters.", [str, Length(min=3, max=20)])
              ),
    Required('first_name'):
        check(("first_name must be between 2 and 20 characters.", [str, Length(min=2, max=20)])
              ),
    Required('last_name'):
        check(("last_name must be between 3 and 20 characters.", [str, Length(min=2, max=20)])
              ),
    Required('national_code'):
        check(("national_code must be 10 characters.", [str, Length(min=10, max=10)])
              ),
    Required('mobile'):
        check(("mobile must be 11 characters.", [str, Length(min=11, max=11)])
              ),
    Required('account_number'):
        check(("account_number must be between 3 and 20 characters.", [str, Length(min=3, max=20)])
              ),
    Required('balance'):
        check(("balance must be between 1 and 20 characters.", [str, Length(min=1, max=20)])
              )
}, extra=True)

def is_logged_in():
    return  "uid" in session

def is_admin():
    return "isAdmin" in session

def prepare_login_step1(params):
    user = User.query.filter_by(username= params["username"]).first()
    if user is None:
        raise WebException("Username is not valid")
    session["username"] = params["username"]
    if user.otp.login_otp == 1:
        session["has_login_OTP"] = True
        otp = random_digits(6)
        user.otp.login_otp_verification_code = otp
        db.session.commit()
        send_sms(user.mobile,otp)
    session["mobile"] = mask_phone(user.mobile)

@validation(schema=login_schema)
def prepare_login_step2(params):
    user = User.query.filter_by(username= session["username"]).first() 
    if user is None:
        raise  WebException("Invalid username, password")
    if user.otp.login_otp == 1:
        if not (user.otp.login_otp_verification_code == params['otp']):
            raise WebException("Invalid OTP")
        user.otp.login_otp_verification_code = ""
        db.session.commit()
    if not check_password(params['password'], user.password):
        raise WebException("Invalid username, password")
    session.clear()
    session.permanent = True
    # app.permanent_session_lifetime = timedelta(minutes=20)
    session['uid'] = user.id

def logout():
    session.clear()



def remember_step2(params):
    if params['username'] is None:
        raise WebException("Username is required.")
    user = User.query.filter_by(username= params["username"]).first() 
    if user is None:
        raise  WebException("Invalid username")
    token = hash(random_digits(50))
    user.remeber_pass_token = token
    db.session.commit()
    text =  url_for('remember_step3',username = params["username"], token = token ,_external=True)
    send_sms(user.mobile,text)
    return mask_phone(user.mobile)

def remember_step3(params):
    if params['username'] is None:
        raise WebException("Username is required.")
    if params['token'] is None:
        raise WebException("Token is required.")
    user = User.query.filter_by(username= params["username"]).first() 
    if user is None:
        raise  WebException("Invalid username")
    if user.remeber_pass_token != params["token"].strip():
        raise  WebException("Invalid token value")
    user.remeber_pass_token = ""
    db.session.commit()
    session["username"] = params["username"]


def remember_step4(params):
    if params['password1'] is None:
        raise WebException("password1 is required.")
    if params['password2'] is None:
        raise WebException("password2 is required.")
    if params['password1'] != params['password2']:
        raise WebException("passwords not match.")
    if "username" not in session:
        raise WebException( "Not allowed." )
    user = User.query.filter_by(username= session["username"]).first() 
    if user is None:
        raise  WebException("Invalid username, password")
    session.pop["username"]
    user.password = build_password(params['password1'])
    db.session.commit()


@validation(schema=register_schema)
def register(params): 
    user = User(
        username=params["username"],
        password=build_password(params["password"]),
        first_name=params["first_name"],
        last_name=params["last_name"],
        national_code=params["national_code"],
        address=params["address"],
        mobile=params["mobile"]
    )
    db.session.add(user)
    db.session.flush()
    account = Account(
        account_number=params["account_number"],
        balance=params["balance"],
        user_id=user.id
    )
    db.session.add(account)
    otp = OTP(
        login_otp=params["login_otp"],
        transfer_otp=params["transfer_otp"],
        user_id=user.id
    )
    db.session.add(otp)
    option = Option(
        card_limit=params["card_limit"],
        transfer_limit=params["transfer_limit"],
        cheque_limit= params["cheque_limit"],
        user_id=user.id
    )
    db.session.add(option)
    card = Card(
        pan=params["pan"],
        pin=build_password(params["pin"]),
        cvv2=build_password( params["cvv2"]),
        expire_date=params["expire_date"],
        user_id=user.id
    )
    db.session.add(card)
    db.session.commit()


def update_profile(params):
    user = User.query.get(session["uid"])
    user.address = params["address"]
    db.session.commit()

def change_password(params):
    user = User.query.get(session["uid"])
    if params["password2"] != params["password3"]:
        raise WebException("New password and confirm is not matched.")
    if not check_password(params['password1'], user.password):
        raise WebException("Current password is not correct.")
    user.password = build_password(params["password2"])
    db.session.commit()