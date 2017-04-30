class Group():

    def __init__(self, name):
        self.name = name
        self.hosts = set()
        self.variables = ''

    def add_host(self, host):
        if not isinstance(host, Host):
            raise Exception("Not a host")

        self.hosts.add(host)
        if self not in host.groups:
            host.add_group(self)

    def __eq__(self, other):
        return self.name == other

    def __hash__(self):
        return hash(self.name)

class Host():

    def __init__(self, name):
        self.name = name
        self.groups = set()
        self.variables = ''

    def add_group(self, group):
        if not isinstance(group, Group):
            raise Exception("Not a group")

        self.groups.add(group)
        if self not in group.hosts:
            group.add_host(self)

    def __eq__(self, other):
        return self.name == other

    def __hash__(self):
        return hash(self.name)

