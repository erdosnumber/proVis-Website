import connexion
import six

from swagger_server.models.companies import Companies  # noqa: E501
from swagger_server.models.company_request import CompanyRequest  # noqa: E501
from swagger_server import util,db


def companies_get():  # noqa: E501
    """get a list of all companies

    retrieves all companies. # noqa: E501


    :rtype: List[Companies]
    """
    return db.get_all_companies()


def companies_post(body):  # noqa: E501
    """create a new Company

    create a new Company given all details # noqa: E501

    :param body: creates a new Company
    :type body: dict | bytes

    :rtype: Companies
    """
    if connexion.request.is_json:
        body = CompanyRequest.from_dict(connexion.request.get_json())  # noqa: E501
        company=Companies(name=body._name,company_img_url=body._company_img_url,about_us=body._about_us,website_link=body._website_link)
        try:
            db.add_companies(company)
        except NameError:
            return  {"error":"Company already exists in the database","status":400}

        return company


def companies_queryid_get(queryid):  # noqa: E501
    """get a company by id

    retrieves a specific company by id. # noqa: E501

    :param queryid: ID of company that needs to be fetched
    :type queryid: str

    :rtype: Companies
    """
    try:
        db.check_company_exists(queryid)
    except NameError:
        return  {"error":"Company with given company_id doesn't exist","status":400}
    
    return db.get_company_by_id(queryid)
