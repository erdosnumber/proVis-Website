import connexion
import six

from swagger_server.models.locations import Locations  # noqa: E501
from swagger_server import util,db


def locations_get():  # noqa: E501
    """get a list of all locations

    retrieves all locations. # noqa: E501


    :rtype: List[Locations]
    """
    return db.get_all_locations()
