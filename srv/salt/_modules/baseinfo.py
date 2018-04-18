# -*- coding: utf-8 -*-

import os
from salt.utils import which


def test():
    if __utils__['path.which']("ls"):
        return True
    return False


class Node(object):

    def __init__(self):
        self.cmd = __salt__['pillar.get']('get_nodes_cmd')

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
            return __salt__['cmd.run_all'](self.cmd)
        elif self.is_ha_node():
            cib_dir = __salt__['pillar.get']('cib_dir')
            cib_file = __salt__['pillar.get']('cib_file')
            _env = {"CIB_file": os.path.join(cib_dir, cib_file)}
            return __salt__['cmd.run_all'](self.cmd, env=_env)
        else:
            return None

    def get_cluster_name(self):
        pass

def get_member():
    node = Node()
    return node.get_member()
