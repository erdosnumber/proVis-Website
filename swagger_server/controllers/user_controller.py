import connexion
import six
from email.message import EmailMessage
# create message object instance
from dotenv.main import load_dotenv
import os
import ssl
import pyotp
import smtplib
from swagger_server.models.customers import Customers
from swagger_server.models.register_response import RegisterResponse,RegisterResponseInfo  # noqa: E501
from swagger_server.models.user_login import UserLogin  # noqa: E501
from swagger_server.models.user_register import UserRegister  # noqa: E501
from swagger_server.models.verify_email import VerifyEmail  # noqa: E501
from swagger_server import util,db
from werkzeug.security import check_password_hash, generate_password_hash
import jwt
load_dotenv()
our_secret_key = os.environ['JWTKEY']
our_id = os.environ['EMAIL']
our_pass = os.environ['MASTERPASSWORD']
algorithm = os.environ['ALGO']

def email_login(body):  # noqa: E501
    """email login

     # noqa: E501

    :param body: logs in the user
    :type body: dict | bytes

    :rtype: RegisterResponse
    """
    if connexion.request.is_json:
        body = UserLogin.from_dict(connexion.request.get_json())  # noqa: E501
        email = body.email_id
        passwd = body.password

        cusid = db.getcusid_fromemail(email)
        if cusid is None:
            return "Invalid Username"
        print(type(cusid))
        print(cusid) 
        hasedpasswd = db.getpassword_fromemail(email)
        verify = check_password_hash(hasedpasswd,passwd)
        if verify:
            name = db.getusername_fromemail(email)
            info = RegisterResponseInfo(cusid,name)
            tokdict = {'username':name,'email':email}
            secret_key = our_secret_key
            token = jwt.encode(tokdict,secret_key,algorithm)
            #response = RegisterResponse(token,info)
            response = {"info":{"cus_uid":cusid,"username":name},"token":token,"status":200}
            return response
        return "Invalid Password"


def email_register(body):  # noqa: E501
    """registration

     # noqa: E501

    :param body: registers the user
    :type body: dict | bytes

    :rtype: RegisterResponse
    """
    if connexion.request.is_json:

        body = UserRegister.from_dict(connexion.request.get_json())  # noqa: E501
        name = body._name
        email = body._email_id
        password = body._password
        hashedpasswd = generate_password_hash(password)
        tokdict = {'user_id':name,'email':email}
        secret_key = our_secret_key
        token = jwt.encode(tokdict,secret_key,algorithm=algorithm)
        customer = Customers(name=name,emailid=email,password=hashedpasswd)
        try:
            db.add_customer(customer)
        except NameError:
            return  {"error":"User with given email already exists","status":400}
        cus_id = customer._cus_id
        # secret = pyotp.random_base32()
        # totp = pyotp.TOTP(secret)
        # otp = totp.now()
        # print("otp :" ,otp)
        # msg = EmailMessage()
        # email_sender = our_id
        # email_receiver = email
        # msg['From'] = email_sender
        # msg['To'] = email
        # msg['Subject'] = "OTP!! Here is your OTP generated OTP"
        # body ="Here is your generated OTP "+ otp
        # msg.set_content(body)
        # context = ssl.create_default_context()
        # with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
        #     smtp.login(email_sender,our_pass)
        #     smtp.sendmail(email_sender,email_receiver,msg.as_string())
        # db.addotp(otp,email)

    return {"info":{"cus_uid":cus_id,"username":name},"token":token,"status":200}


def send_verification_mail(authorization):  # noqa: E501
    """verification email

     # noqa: E501

    :param authorization: an authorization header
    :type authorization: str

    :rtype: None
    """
    return None


def verify_email(body):  # noqa: E501
    """verify email

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: str
    """

    if connexion.request.is_json:
        body = (connexion.request.get_json())  # noqa: E501
        token = body["token"]
        otp = body["otp"]
        tokdict= jwt.decode(token,key=our_secret_key,algorithms=[algorithm])
        mail= tokdict["email"]
        requiredotp = db.getotp_frommail(mail)
        if (otp == requiredotp):
            return {"verification_status":"true","status":200}
        else:
            return {"verification_status":"false","status":400}

        
    return "True"
