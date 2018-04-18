# -*- coding: utf-8 -*-

from salt.utils import which


def test():
    if __utils__['path.which']("ls"):
        return True
    return False


class Node(object):

    def __init__(self):
        self.members = self.get_member()
        self.cluster_name = self.get_cluster_name()

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
            cmd = __salt__['pillar.get']('get_nodes_cmd')
            return __salt__['cmd.run_all'](cmd)
        elif self.is_ha_node():
            pass
        else:
            return None

    def get_cluster_name(self):
        pass

def get_member():
    node = Node()
    return node.get_member()
