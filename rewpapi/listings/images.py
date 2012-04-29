from rewpapi.common.http import Request
from rewpapi.listings.listing import ListingResidential


class RemoteListingImages(Request):
    def __init__(self, base_site, auth, listing_type, listing_uuid):
        super(RemoteListingImages, self).__init__(auth)
        self._base_site = base_site
        self._auth = auth
        self._listing_type = listing_type
        self._listing_uuid = listing_uuid
        self._endpoint = base_site + "/api/listings/%s/%s/images/" % (
                listing_type, listing_uuid)

    def get_all(self):
        """
        Returns a list of Listing images
        """
        remote_listing_images = self.execute()
        listing_images = []
        if remote_listing_images:
            for a in remote_listing_images:
                new_listing_images = ListingImages(self._base_site, self._auth,
                        self._listing_type, self._listing_uuid)
                new_listing_images.FIELDS = []
                for k, v in a.items():
                    setattr(new_listing_images, k, v)
                    new_listing_images.FIELDS.append(k)
                listing_images.append(new_listing_images)
            return listing_images
        return None

    def get(self, uuid):
        """
        Returns a single ListingImage instance, matching uuid.

        Raises a DoesNotExist exception if the object does not exist.
        """
        b = ListingResidential()
        b.branch_name = "Foo"
        return b


class ListingImages(RemoteListingImages):
    """
    A ListingImages object represents a Listing's images. Once instantiated,
    you can:
     - Change its values and send an update()
     - Create it if it doesn't exist
    """
    def set_fields(self, images):
        self.images = images

    def update(self):
        """
        Update this listing's images.
        """
        self._endpoint = self._base_site + "/api/listings/%s/%s/images/" % (
                self._listing_type, self._listing_uuid)
        images = []
        for image in self.images:
            image_dict = {}
            image_dict['image'] = image.image
            image_dict['caption'] = image.caption
            image_dict['sha1'] = image.sha1
            images.append(image_dict)
        self.execute("PUT", images)
