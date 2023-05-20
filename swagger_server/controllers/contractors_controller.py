import connexion
import six

from swagger_server.models.contractor_request import ContractorRequest  # noqa: E501
from swagger_server.models.contractors import Contractors  # noqa: E501
from swagger_server import util,db


def get_contractor(queryid:str):  # noqa: E501
    """get a contractor by id

    retrieves a specific contractor by id. # noqa: E501

    :param queryid: ID of contractor that needs to be fetched
    :type queryid: str

    :rtype: Contractors
    """
    try:
        db.check_contractor_exists(queryid)
    except NameError:
        return  {"error":"Contractor with given contractor_id doesn't exist","status":400}
    return db.get_contractor_by_id(queryid)


def get_contractors():  # noqa: E501
    """get a list of all contractors

    retrieves all contractors. # noqa: E501


    :rtype: List[Contractors]
    """
    return db.get_all_contractors()


def post_contractor(body):  # noqa: E501
    """create a new contractor

    create a new contractor given all details # noqa: E501

    :param body: creates a new contractor
    :type body: dict | bytes

    :rtype: Contractors
    """
    if connexion.request.is_json:
        body = ContractorRequest.from_dict(connexion.request.get_json())  # noqa: E501
        contractor=Contractors(name=body._name,email=body._email,address=body._address,phone_no=body._phone_no,company_id=body._company_id)
        try:
            db.check_company_exists(contractor.company_id)
        except NameError:
            return {"error":"Company with given company_id doesn't exist","status":400}
    
        try:
            db.add_contractors(contractor)
        except NameError:
            return {"error":"Contractor already exists in the database","status":400}

        return contractor
