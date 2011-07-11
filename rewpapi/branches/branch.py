from rewpapi.common.http import Request

import json
import sys


class RemoteBranch(Request):
    """
    This object provides the remote interface to work with branches.
    """
    def __init__(self, base_site, auth):
        super(RemoteBranch, self).__init__(auth)
        self._base_site = base_site
        self._auth = auth
        self._endpoint = base_site + "/api/branches/"

    def get_all(self):
        """
        Returns a list of <Branch>'s
        """
        remote_branches = self.execute()
        branches = []
        if remote_branches:
            for b in remote_branches:
                new_branch = Branch(self._base_site, self._auth)
                new_branch.FIELDS = []
                for k, v in b.items():
                    setattr(new_branch, k, v)
                    new_branch.FIELDS.append(k)
                branches.append(new_branch)
            return branches
        return None

    def get(self, uuid):
        """
        Returns a single Branch instance, matching uuid.

        Raises a DoesNotExist exception if the object does not exist.
        """
        b = Branch()
        b.branch_name = "Foo"
        return b


class Branch(RemoteBranch):
    """
    A Branch object represents a Branch. Once instantiated, you can:
     - Change its values and send an update()
     - Delete it
     - Create it if it doesn't exist
    """
    def _set_fields(self, branch_object):
        self.FIELDS = branch_object.FIELDS
        for field in branch_object.FIELDS:
            setattr(self, field, getattr(branch_object, field))

    def update(self):
        """
        Update this branch.
        """
        self._endpoint = self._base_site + "/api/branches/%s/" % self.uuid
        branch_dict = {}
        for a in self.FIELDS:
            branch_dict[a] = getattr(self, a)
        self.execute("PUT", branch_dict)

    def delete(self):
        """
        Delete this branch.
        """
        pass

    def create(self):
        """
        Create a new branch.
        """
        self._endpoint = self._base_site + "/api/branches/"
        branch_dict = {}
        for a in self.FIELDS:
            branch_dict[a] = getattr(self, a)
        self.execute("POST", branch_dict)
