# -*- coding: utf-8 -*-

import os
from salt.utils import which


class Node(object):

    def __init__(self):
        self.get_nodes_cmd = __salt__['pillar.get']('get_nodes_cmd')
        self.get_cib_cmd = __salt__['pillar.get']('get_cib_cmd')

    def is_ha_node(self):
        if which("pacemakerd") and which("corosync"):
            return True
        return False

    def is_live_node(self):
        if __utils__['crmshutils.is_process']("crmd"):
            return True
        return False

    def get_member(self):
        if self.is_live_node():
            return __salt__['cmd.run_all'](self.get_nodes_cmd)['stdout']
        elif self.is_ha_node():
            cib_dir = __salt__['pillar.get']('cib_dir')
            cib_file = __salt__['pillar.get']('cib_file')
            _env = {"CIB_file": os.path.join(cib_dir, cib_file)}
            return __salt__['cmd.run_all'](self.get_nodes_cmd, env=_env)['stdout']
        else:
            return None

    def get_cluster_name(self):
        if self.is_live_node():
            cmd = self.get_cib_cmd + " -o crm_config"
            return __salt__['cmd.run_all'](cmd)['stdout']


def get_member():
    node = Node()
    ret = node.get_member()
    if ret:
        return ret.split()

def get_cluster_name():
    node = Node()
    return node.get_cluster_name()
