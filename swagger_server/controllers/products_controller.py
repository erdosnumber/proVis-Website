import connexion
import six

from swagger_server.models.products import Products  # noqa: E501
from swagger_server.models.locations import Locations 
from swagger_server.models.categories import Categories
from swagger_server import util,db


def get_product(queryid):  # noqa: E501
    """get a product by id

    retrieves a specific product by id. # noqa: E501

    :param queryid: ID of product that needs to be fetched
    :type queryid: str

    :rtype: Products
    """
    try:
        db.check_product_exists(queryid)
    except NameError:
        return  {"error":"Product with given p_uid doesn't exist","status":400}
    
    return db.getproduct_frompuid(queryid)


def get_product_by_tags(location=None, category=None):  # noqa: E501
    """gets all products matching the tags

    gets all products matching the tags # noqa: E501

    :param location: location name
    :type location: str
    :param category: category name
    :type category: str

    :rtype: Products
    """
    if(location!=None and category!=None):
        return db.getproduct_fromlocationandcategory(location,category)
    elif(location!=None and category==None):
        return db.getproduct_fromlocation(location)
    elif(location==None and category!=None):
        return db.getproduct_fromcategory(category)
    else:
        return db.get_all_products()


def get_products():  # noqa: E501
    """get a list of all products

    retrieves all products. # noqa: E501


    :rtype: List[Products]
    """
    return db.get_all_products()



def post_product(body):  # noqa: E501
    """create a new product

    create a new product # noqa: E501

    :param body: creates a new product
    :type body: dict | bytes

    :rtype: Products
    """
    if connexion.request.is_json:
        body = Products.from_dict(connexion.request.get_json())  # noqa: E501
        product=Products(location=body._location,category=body._category,product_img_url=body._product_img_url,product_description=body
                        ._product_description,company_name=body._company_name,company_img_url=body._company_img_url,contractor_id=body._contractor_id)
        location=Locations(name=body._location)
        category=Categories(name=body._category)
        db.add_locations(location)
        db.add_categories(category)

        try:
            db.check_contractor_exists(product.contractor_id)
        except NameError:
            return {"error":"Contractor with given contractor_id doesn't exist","status":400}
        
        try:
            db.add_products(product)
        except NameError:
            return  {"error":"Product already exists","status":400}

        return product
