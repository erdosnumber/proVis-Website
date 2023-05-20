import connexion
import six

from swagger_server.models.categories import Categories  # noqa: E501
from swagger_server import util,db


def categories_get():  # noqa: E501
    """get a list of all categories

    retrieves all categories. # noqa: E501


    :rtype: List[Categories]
    """
    return db.get_all_categories()
