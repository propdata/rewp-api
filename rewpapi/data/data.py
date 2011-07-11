from rewpapi.common.http import Request

import json
import sys


class Data(Request):
    """
    This object provides the remote interface to collect data.
    """
    def __init__(self, base_site, auth):
        super(Data, self).__init__(auth)
        self._base_site = base_site

    def get_listing_types(self):
        """
        Returns a list of possible Listing Types.
        """
        self._endpoint = self._base_site + "/api/listing-types/"
        listing_types = self.execute()
        if listing_types:
            return listing_types
        return None

    def get_property_types(self, listing_type_slug):
        """
        Returns a list of possible Property Types for a specific Listing Type.
        """
        self._endpoint = "%s/api/property-types/%s/" % (self.base_site,
                listing_type_slug)
        property_types = self.execute()
        if property_types:
            return property_types
        return None
