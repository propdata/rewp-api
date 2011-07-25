from rewpapi.common.http import Request

import json
import sys


class RemoteAgent(Request):
    """
    This object provides the remote interface to work with agents.
    """
    def __init__(self, base_site, auth):
        super(RemoteAgent, self).__init__(auth)
        self._base_site = base_site
        self._auth = auth
        self._endpoint = base_site + "/api/agents/"

    def get_all(self):
        """
        Returns a list of agents
        """
        remote_agents = self.execute()
        agents = []
        if remote_agents:
            for a in remote_agents:
                new_agent = Agent(self._base_site, self._auth)
                new_agent.FIELDS = []
                for k, v in a.items():
                    setattr(new_agent, k, v)
                    new_agent.FIELDS.append(k)
                agents.append(new_agent)
            return agents
        return None

    def get(self, uuid):
        """
        Returns a single Agent instance, matching uuid.

        Raises a DoesNotExist exception if the object does not exist.
        """
        b = Agent()
        b.branch_name = "Foo"
        return b


class Agent(RemoteAgent):
    """
    An Agent object represents an Agent. Once instantiated, you can:
     - Change its values and send an update()
     - Delete it
     - Create it if it doesn't exist
    """
    def set_fields(self, agent_object):
        self.FIELDS = agent_object.FIELDS
        for field in agent_object.FIELDS:
            setattr(self, field, getattr(agent_object, field))

    def update(self):
        """
        Update this agent.
        """
        self._endpoint = self._base_site + "/api/agents/%s/" % self.uuid
        agent_dict = {}
        for a in self.FIELDS:
            agent_dict[a] = getattr(self, a)
        agent_dict['branch_name'] = agent_dict['branch']['branch_name']
        del agent_dict['branch']
        self.execute("PUT", agent_dict)

    def delete(self):
        """
        Delete this branch.
        """
        pass

    def create(self):
        """
        Create a new agent.
        """
        self._endpoint = self._base_site + "/api/agents/"
        agent_dict = {}
        for a in self.FIELDS:
            agent_dict[a] = getattr(self, a)
        agent_dict['branch_name'] = agent_dict['branch']['branch_name']
        del agent_dict['branch']
        self.execute("POST", agent_dict)
