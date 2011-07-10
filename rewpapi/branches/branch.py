from rewpapi.common.http import Request

import json
import sys


class RemoteBranch(Request):
    """
    This object provides the remote interface to work with branches.
    """
    def __init__(self, base_site, auth):
        super(RemoteBranch, self).__init__(auth)
        self.endpoint = base_site + "/api/branches/"

    def get_all(self):
        """
        Returns a list of <Branch>'s
        """
        branches = self.execute()
        if branches:
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
    def update(self):
        """
        Update this branch.
        """
        pass

    def delete(self):
        """
        Delete this branch.
        """
        pass

    def create(self):
        """
        Create a new branch.
        """
        pass


def run(branch_uuid=None):
    url = "http://www.yoursite.co.za/api/branches/"
    if branch_uuid:
        url += "%s/" % branch_uuid
    host, path, headers = build_request(url)
    response = request_response(host, path, "GET", headers)

    if branch_uuid:
        branch = json.loads(response)
        print branch['branch_manager']
    else:
        branches = json.loads(response)
        for branch in branches:
            print branch['branch_name'], branch['uuid']


if __name__ == "__main__":
    b = RemoteBranch()

    print "Current Branches:"
    branches = b.get_all()
    print branches

    print "First Branch:"
    branch = b.get(branches[0].uuid)
    print branch # This is an <object 'Branch'>

    print "Update First Branch:"
    branch.branch_name = "Foo"
    print branch.update()

    print "Create a new Branch"
    b = Branch()
    b.branch_name = "Foo bar"
    b.create()

