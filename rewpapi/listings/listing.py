from rewpapi.common.http import Request

import json
import sys


class RemoteListingResidential(Request):
    def __init__(self, base_site, auth):
        super(RemoteListingResidential, self).__init__(auth)
        self._base_site = base_site
        self._auth = auth
        self._endpoint = base_site + "/api/listings/residential/"

    def get_all(self):
        """
        Returns a list of Listings
        """
        remote_listings = self.execute()
        listings = []
        if remote_listings:
            for a in remote_listings:
                new_listing = ListingResidential(self._base_site, self._auth)
                new_listing.FIELDS = []
                for k, v in a.items():
                    setattr(new_listing, k, v)
                    new_listing.FIELDS.append(k)
                listings.append(new_listing)
            return listings
        return None

    def get(self, uuid):
        """
        Returns a single Listing instance, matching uuid.

        Raises a DoesNotExist exception if the object does not exist.
        """
        b = ListingResidential()
        b.branch_name = "Foo"
        return b


class ListingResidential(RemoteListingResidential):
    """
    A Listing object represents a Listing. Once instantiated, you can:
     - Change its values and send an update()
     - Delete it
     - Create it if it doesn't exist
    """
    def set_fields(self, listing_object):
        self.FIELDS = listing_object.FIELDS
        for field in listing_object.FIELDS:
            setattr(self, field, getattr(listing_object, field))

    def update(self):
        """
        Update this listing.
        """
        self._endpoint = self._base_site + "/api/listings/residential/%s/" % self.uuid
        listing_dict = {}
        for a in self.FIELDS:
            listing_dict[a] = getattr(self, a)
        listing_dict['country'] = listing_dict['location']['country']
        listing_dict['province'] = listing_dict['location']['province']
        listing_dict['area'] = listing_dict['location']['region']
        listing_dict['suburb'] = listing_dict['location']['suburb']
        del listing_dict['agent']
        del listing_dict['location']
        del listing_dict['website_url']
        del listing_dict['images']
        del listing_dict['floorplans']
        self.execute("PUT", listing_dict)

    def delete(self):
        """
        Delete this listing.
        """
        pass

    def create(self):
        """
        Create a new listing.
        """
        self._endpoint = self._base_site + "/api/listings/residential/"
        listing_dict = {}
        for a in self.FIELDS:
            listing_dict[a] = getattr(self, a)
        listing_dict['country'] = listing_dict['location']['country']
        listing_dict['province'] = listing_dict['location']['province']
        listing_dict['area'] = listing_dict['location']['region']
        listing_dict['suburb'] = listing_dict['location']['suburb']
        del listing_dict['agent']
        del listing_dict['location']
        del listing_dict['website_url']
        del listing_dict['images']
        del listing_dict['floorplans']
        self.execute("POST", listing_dict)
