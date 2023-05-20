import connexion
import six
from email.message import EmailMessage
# create message object instance
from dotenv.main import load_dotenv
import os
import ssl
import smtplib

from swagger_server.models.order_request import OrderRequest  # noqa: E501
from swagger_server.models.orders import Orders  # noqa: E501
from swagger_server import util,db

load_dotenv()
our_secret_key = os.environ['JWTKEY']
our_id = os.environ['EMAIL']
our_pass = os.environ['MASTERPASSWORD']
algorithm = os.environ['ALGO']


def get_customer_order(queryid, orderid):  # noqa: E501
    """get a customer&#x27;s specific order by id of both

    retrieves a specific order by id of customer and order # noqa: E501

    :param queryid: ID of customer whose orders need to be fetched
    :type queryid: str
    :param orderid: ID of order that needs to be fetched
    :type orderid: str

    :rtype: Orders
    """
    try:
        return db.getorder_fromid(orderid)
    except NameError:
        return  {"error":"Order with given order id doesn't exist","status":400}


def get_customer_orders(queryid):  # noqa: E501
    """get a list of all orders of a specific customers

    fetches all orders of a specific customer # noqa: E501

    :param queryid: ID of customer whose orders need to be fetched
    :type queryid: str

    :rtype: List[Orders]
    """
    return db.getorders_fromcusid(queryid)


def post_order(body, queryid):  # noqa: E501
    """create a new order for a customer with given id

    create a new order for a customer with given id # noqa: E501

    :param body: creates a new order for a specific customer
    :type body: dict | bytes
    :param queryid: ID of customer for which new order is being added
    :type queryid: str

    :rtype: Orders
    """
    if connexion.request.is_json:
        body = OrderRequest.from_dict(connexion.request.get_json())  # noqa: E501
        order=Orders(cus_uid=body._cus_uid,order_date_time=body._order_date_time,p_uid=body._p_uid,message=body._message)

        try:
            db.check_customer_exists(order.cus_uid)
        except NameError:
            return {"error":"Customer with given cus_uid doesn't exist","status":400}
        
        try:
            db.check_product_exists(order.p_uid)
        except NameError:
            return {"error":"Product with given p_uid doesn't exist","status":400}
        
        contractorid=db.getcontractorid_frompuid(order.p_uid)
        contractor=db.get_contractor_by_id(contractorid)
        contractoremail=contractor.email
        customer=db.get_customer_by_id(order.cus_uid)
        customeremail=customer.emailid

        msg = EmailMessage()
        email_sender = our_id
        email_receiver = contractoremail
        msg['From'] = email_sender
        msg['To'] = contractoremail
        msg['Subject'] = "Request from proVis"
        body ="You have received a request to meet from user with email address "+customeremail+"\nTheir message is the following\n"+order.message+"\nPlease get in touch with them as soon as possible."
        msg.set_content(body)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
            smtp.login(email_sender,our_pass)
            smtp.sendmail(email_sender,email_receiver,msg.as_string())
            
        db.add_orders(order)

        return order
