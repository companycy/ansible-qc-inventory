# add dynamic inventory from qingcloud

- setup qingcloud sdk
https://docs.qingcloud.com/api/common/sdk/python/index.html

- create inventory.py which can accept '--list' and give required json
http://www.jeffgeerling.com/blog/creating-custom-dynamic-inventories-ansible

root@i-t1y8c2ur:~# more inventory
[group]
192.168.103.10
192.168.103.12

root@i-t1y8c2ur:~#  ansible group -i inventory -m ping
192.168.103.10 | SUCCESS => {
    "changed": false, 
    "ping": "pong"
}
192.168.103.12 | SUCCESS => {
    "changed": false, 
    "ping": "pong"
}

so ensure inventory.py runs as below:

root@i-t1y8c2ur:~# ./inventory.py --list
{"group": {"hosts": ["192.168.103.10", "192.168.103.12"]}}


then it works as below:

root@i-t1y8c2ur:~#  ansible group -i inventory.py -m ping
192.168.103.10 | SUCCESS => {
    "changed": false, 
    "ping": "pong"
}
192.168.103.12 | SUCCESS => {
    "changed": false, 
    "ping": "pong"
}






