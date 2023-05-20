import connexion
import six

from swagger_server.models.bookmark_request import BookmarkRequest  # noqa: E501
from swagger_server.models.bookmarks import Bookmarks  # noqa: E501
from swagger_server import util,db


def delete_customer_bookmark(queryid, bookmarkid):  # noqa: E501
    """deletes a specific customer&#x27;s bookmark by id of both

    deletes a specific customer&#x27;s bookmark by id of both # noqa: E501

    :param queryid: ID of customer whose bookmark needs to be deleted
    :type queryid: str
    :param bookmarkid: ID of bookmark that needs to be fetched
    :type bookmarkid: str

    :rtype: None
    """

    db.deletebookmark_fromid(queryid,bookmarkid)
   


def get_customer_bookmark(queryid, bookmarkid):  # noqa: E501
    """get a customer&#x27;s specific bookmark by id of both

    retrieves a specific bookmark by id of customer and order # noqa: E501

    :param queryid: ID of customer
    :type queryid: str
    :param bookmarkid: ID of bookmark that needs to be fetched
    :type bookmarkid: str

    :rtype: Bookmarks
    """
    try:
        return db.getbookmark_fromid(queryid,bookmarkid)
    except NameError:
        return {"error":"Bookmark with the given bookmarkid doesn't exist","status":400}


def get_customer_bookmarks(queryid):  # noqa: E501
    """get a list of all bookmarks of a specific customer

    fetches all bookmarks of a specific customer # noqa: E501

    :param queryid: ID of customer whose bookmark is needed
    :type queryid: str

    :rtype: List[Bookmarks]
    """
    return db.getbookmarks_fromcusid(queryid)


def post_bookmark(body, queryid):  # noqa: E501
    """create a new bookmark for a customer with given id

    create a new bookamark for a customer with given id # noqa: E501

    :param body: creates a new bookmark for a specific customer
    :type body: dict | bytes
    :param queryid: ID of customer for which new bookmark has to be added
    :type queryid: str

    :rtype: Bookmarks
    """
    if connexion.request.is_json:
        body = BookmarkRequest.from_dict(connexion.request.get_json())  # noqa: E501
        bookmark=BookmarkRequest(cus_uid=body._cus_uid,p_uid=body._p_uid)

        #queryid is same as bookmark.cus_uid
        try:
            db.check_customer_exists(body._cus_uid)
        except NameError:
            return {"error":"Customer with given cus_uid doesn't exist","status":400}
        
        try:
            db.check_product_exists(bookmark.p_uid)
        except NameError:
            return {"error":"Product with given p_uid doesn't exist","status":400}
        
        db.add_bookmarks(bookmark)
        
    return bookmark
