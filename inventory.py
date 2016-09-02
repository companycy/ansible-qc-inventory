#!/usr/bin/env python

"""
Example custom dynamic inventory script for Ansible, in Python.
"""

import os
import sys
import argparse
from optparse import OptionParser
import qingcloud.iaas

try:
    import json
except ImportError:
    import simplejson as json


class QcInventory(object):
    def __init__(self, args):
        parser = argparse.ArgumentParser()
        parser.add_argument("--list", action="store_true")
        parser.add_argument("--host", action="store")
        self.args = parser.parse_args()

        self.conn = qingcloud.iaas.connect_to_zone(
            "pek2",
            "xxx",
            "xxx"
        )

        self.inventory = {}
        if self.args.list:  # Called with `--list`.
            self.inventory = self.get_qingcloud_inventory()
        elif self.args.host:  # Called with `--host [hostname]`.
            self.inventory = self.empty_inventory()  # Not implemented, since we return _meta info `--list`.
        else:  # If no groups or vars are present, return an empty inventory.
            self.inventory = self.empty_inventory()

        print json.dumps(self.inventory);

    def get_qingcloud_inventory(self):
        ret = self.conn.describe_instances(
            instances=["i-eh9k5ntp", "i-p3xlqevp"],
        )
        if ret is None:
            return

        inventory_hosts = []
        instance_set = ret["instance_set"]
        for instance in instance_set:  # make up json required by inventory
            for vxnet in instance["vxnets"]:
                if vxnet["vxnet_name"] == "primary vxnet":
                    continue
                else:
                    private_ip = vxnet["private_ip"]
                    inventory_hosts.append(private_ip)

        inventory = {
            "group": {
                "hosts": inventory_hosts,
                "vars": {
                    "ansible_ssh_user": "root",
                    "ansible_ssh_private_key_file":
                        "/root/.ssh/id_rsa.pub",
                    "example_variable": "value"
                }
            },
            # "_meta": {
            #     "hostvars": {
            #         "192.168.103.10": {
            #             "host_specific_var": "foo"
            #         },
            #         "192.168.103.12": {
            #             "host_specific_var": "bar"
            #         }
            #     }
            # }
        }
        return inventory

    # Empty inventory for testing.
    @staticmethod
    def empty_inventory():
        return {"_meta": {"hostvars": {}}}


def main(args):
    QcInventory(args)


if __name__ == "__main__":
    main(sys.argv[1:])
