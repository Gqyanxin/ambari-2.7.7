class Script(object):

    def execute(self):
        pass

    @staticmethod
    def get_config():
        return {'configurations':
                {'node.properties': {},
                 'jvm.config': {'jvm.config': ''},
                 'config.properties': {},
                 'connectors.properties': {'connectors.to.add': '{}', 'connectors.to.delete': '{}'}},
                 'clusterHostInfo': {'trino_worker_hosts': [], 'trino_coordinator_hosts': []},
                 'hostLevelParams': {'java_home': '/some/fake/path'}}