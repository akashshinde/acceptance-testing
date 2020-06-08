import common
import subprocess
import os
import configs
from robot.api import logger

ROBOT_LIBRARY_SCOPE = 'SUITE'


def auth_wrap(cmd):
    logger.debug("Cluster auth requested " + configs.AUTH_COMMAND)
    return configs.AUTH_COMMAND+' && '+cmd


def load_script(provider):
    path = 'scripts/cluster_providers/'
    return path + provider + '.sh'


def setup_cluster(provider, metadata):
    return SetupCluster(provider, metadata)


class SetupCluster():
    def __init__(self, provider, metadata):
        self.provider = provider
        self.metadata = metadata
        self.base_cmd = 'bash -c'
        self.cluster_name = 'helm-acceptance-test-' + self.metadata

    def setup_cluster(self):
        self.call_cluster_provisioner_script('create_cluster')
        configs.AUTH_COMMAND = self.call_cluster_provisioner_script(
            'get_cluster_auth')
        logger.debug("Cluster auth set: " + configs.AUTH_COMMAND)

    def delete_cluster(self):
        self.call_cluster_provisioner_script('delete_cluster')

    def get_cluster_auth(self):
        configs.AUTH_COMMAND = self.call_cluster_provisioner_script(
            'get_cluster_auth')
        logger.debug("Cluster auth requested " + configs.AUTH_COMMAND)
        return configs.AUTH_COMMAND

    def call_cluster_provisioner_script(self, cmd, detach=False):
        c = f'source {load_script(self.provider)}; {cmd} {self.metadata} {self.cluster_name}'
        process = subprocess.Popen(['/bin/bash', '-c', c],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
        if not detach:
            stdout = process.communicate()[0].strip().decode()
            self.rc = process.returncode
            tmp = []
            for x in stdout.split('\n'):
                logger.debug(x)
                if not x.startswith('+ '):  # Remove debug lines that start with "+ "
                    tmp.append(x)
            self.stdout = '\n'.join(tmp)
        return self.stdout
