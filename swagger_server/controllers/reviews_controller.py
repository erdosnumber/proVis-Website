import connexion
import six

from swagger_server.models.review_request import ReviewRequest  # noqa: E501
from swagger_server.models.reviews import Reviews  # noqa: E501
from swagger_server import util,db


def products_queryid_reviews_get(queryid):  # noqa: E501
    """get a list of all Reviews of a specific product

    fetches all Reviews of a specific product # noqa: E501

    :param queryid: ID of product whose bookmark is needed
    :type queryid: str

    :rtype: List[Reviews]
    """
    return db.getreviews_frompuid(queryid)


def products_queryid_reviews_post(body, queryid):  # noqa: E501
    """create a new review for a product with given id

    create a new bookamark for a customer with given id # noqa: E501

    :param body: creates a new review for a specific product
    :type body: dict | bytes
    :param queryid: ID of product for which new review has to be added
    :type queryid: str

    :rtype: Reviews
    """
    if connexion.request.is_json:
        body = ReviewRequest.from_dict(connexion.request.get_json())  # noqa: E501
        review=Reviews(cus_uid=body._cus_uid,p_uid=body._p_uid,review=body._review)

        #queryid is same as review.p_uid
        try:
            db.check_customer_exists(review.cus_uid)
        except NameError:
            return {"error":"Customer with given cus_uid doesn't exist","status":400}
        
        try:
            db.check_product_exists(review.p_uid)
        except NameError:
            return {"error":"Product with given p_uid doesn't exist","status":400}
        
        db.add_reviews(review)

        return review


def products_queryid_reviews_reviewid_delete(queryid, reviewid):  # noqa: E501
    """deletes a specific product&#x27;s review by id of both

    deletes a specific product&#x27;s review by id of both # noqa: E501

    :param queryid: ID of product whose review needs to be deleted
    :type queryid: str
    :param reviewid: ID of review that needs to be fetched
    :type reviewid: str

    :rtype: None
    """
    db.deletereviews_fromreviewid(reviewid)
