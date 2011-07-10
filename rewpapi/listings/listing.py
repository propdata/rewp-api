from rewpapi.common.http import Request

import json
import sys


class RemoteListing(Request):
    """
    This object provides the remote interface to work with listings.
    """
    def get_all(self):
        """
        Returns a list of Listings
        """
        listings = self.execute()
        if listings:
            return listings
        return None

    def get(self, uuid):
        """
        Returns a single Listing instance, matching uuid.

        Raises a DoesNotExist exception if the object does not exist.
        """
        b = Branch()
        b.branch_name = "Foo"
        return b


class RemoteListingResidential(RemoteListing):
    def __init__(self, base_site, auth):
        super(RemoteListingResidential, self).__init__(auth)
        self.endpoint = base_site + "/api/listings/residential/"


class Listing(RemoteListing):
    """
    A Listing object represents a Listing. Once instantiated, you can:
     - Change its values and send an update()
     - Delete it
     - Create it if it doesn't exist
    """
    def update(self):
        """
        Update this listing.
        """
        pass

    def delete(self):
        """
        Delete this listing.
        """
        pass

    def create(self):
        """
        Create a new listing.
        """
        pass

