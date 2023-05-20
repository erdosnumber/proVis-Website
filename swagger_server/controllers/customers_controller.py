import connexion
import six

from swagger_server.models.customers import Customers  # noqa: E501
from swagger_server.models.register_response import RegisterResponse  # noqa: E501
from swagger_server import util,db


def get_customer(queryid):  # noqa: E501
    """get a customer by id

    retrieves a specific customer by id. # noqa: E501

    :param queryid: ID of customer that needs to be fetched
    :type queryid: str

    :rtype: Customers
    """
    try:
        db.check_customer_exists(queryid)
    except NameError:
        return {"error":"Customer with given cus_uid doesn't exist","status":400}

    return db.get_customer_by_id(queryid)


def get_customers():  # noqa: E501
    """get a list of all customers

    retrieves all customers. # noqa: E501


    :rtype: List[Customers]
    """
    return db.get_all_customers()


def post_customers(body):  # noqa: E501
    """create a new customer

    create a new customer given all details of customer while signing up # noqa: E501

    :param body: creates a new customer
    :type body: dict | bytes

    :rtype: RegisterResponse
    """
    if connexion.request.is_json:
        body = Customers.from_dict(connexion.request.get_json())  # noqa: E501
        customer=Customers(name=body._name,emailid=body._emailid,phone_number=body._phone_number,password=body._password)
        try:
            db.add_customer(customer)
        except NameError:
             return  {"error":"Customer already exists in the database","status":400}
        
        return customer
