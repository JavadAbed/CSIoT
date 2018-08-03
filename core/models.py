from core import db
from sqlalchemy.orm import relationship

types = {
    "card2card": 10,
    "check": 20,
    "transfer": 30,
}

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), index=True, unique=True)
    password = db.Column(db.String(40), unique=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    national_code = db.Column(db.String(10), unique=True)
    address = db.Column(db.String(100))
    mobile = db.Column(db.String(12), unique=True)
    remeber_pass_token = db.Column(db.String(32))
    account = relationship("Account", uselist=False, back_populates="user")
    otp = relationship("OTP", uselist=False, back_populates="user")
    option = relationship("Option", uselist=False, back_populates="user")
    card = relationship("Card", uselist=False, back_populates="user")

    def __getitem__(self, items):
        if items.startswith("account."):
            return self.account[items[len("account."):]]
        elif items.startswith("option."):
            return self.option[items[len("option."):]]
        elif items.startswith("otp."):
            return self.otp[items[len("otp."):]]
        elif items.startswith("card."):
            return self.card[items[len("card."):]]
        else:
            return {
                "username": self.username,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "national_code": self.national_code,
                "address": self.address,
                "mobile": self.mobile
            }[items]


class Account(db.Model):
    __tablename__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account_number = db.Column(db.String(20), unique=True)
    balance = db.Column(db.Integer, unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = relationship("User", foreign_keys=user_id, back_populates="account")

    def __getitem__(self, items):
        if items.startswith("user."):
            return self.user[items[len("user."):]]
        else:
            return {
                "balance": self.balance,
                "account_number": self.account_number
            }[items]
    
class OTP(db.Model):
    __tablename__ = 'otps'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login_otp = db.Column(db.Integer, unique=False)
    login_otp_verification_code = db.Column(db.String(6), unique=False)
    transfer_otp = db.Column(db.Integer, unique=False)
    transfer_otp_verification_code = db.Column(db.String(6), unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = relationship("User", foreign_keys=user_id, back_populates="otp")

    def __getitem__(self, items):
        if items.startswith("user."):
            return self.user[items[len("user."):]]
        else:
            return {
                "login_otp": self.login_otp,
                "transfer_otp": self.transfer_otp
            }[items]


class Option(db.Model):
    __tablename__ = 'options'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    card_limit = db.Column(db.Integer, unique=False)
    transfer_limit = db.Column(db.Integer, unique=False)
    cheque_limit = db.Column(db.Integer, unique=False)
    enable_service_transfer = db.Column(db.Integer, unique=False)
    enable_service_debit = db.Column(db.Integer, unique=False)
    enable_service_check = db.Column(db.Integer, unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = relationship("User", foreign_keys=user_id, back_populates="option")

    def __getitem__(self, items):
        if items.startswith("user."):
            return self.user[items[len("user."):]]
        else:
            return {
                "card_limit": self.card_limit,
                "transfer_limit": self.transfer_limit,
                "cheque_limit": self.cheque_limit,
            }[items]


class Card(db.Model):
    __tablename__ = 'cards'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pan = db.Column(db.String(16), unique=True)
    pin = db.Column(db.String(40), unique=False)
    cvv2 = db.Column(db.String(40), unique=False)
    expire_date = db.Column(db.String(4), unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = relationship("User", foreign_keys=user_id, back_populates="card")

    def __getitem__(self, items):
        if items.startswith("user."):
            return self.user[items[5:]] 
        else:
            return {
                "pan": self.pan,
                "pin": self.pin,
                "cvv2": self.cvv2,
                "expire_date": self.expire_date
            }[items]

class Transfer(db.Model):
    __tablename__ = 'transfers'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    from_user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    from_user = relationship("User", foreign_keys=from_user_id)
    to_user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    to_user = relationship("User", foreign_keys=to_user_id)
    date = db.Column(db.Integer)
    type = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    description = db.Column(db.String(160))

class Flag(db.Model):
    __tablename__ = 'flags'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    flag = db.Column(db.String(50))
    point = db.Column(db.Integer) 
    price = db.Column(db.Integer)
    type = db.Column(db.Integer)    #1,2,3
    owner_id = db.Column(db.Integer)
