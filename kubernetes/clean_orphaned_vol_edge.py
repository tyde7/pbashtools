#!/usr/bin/env python3

# for kubeedge only.

import re, os

def delete(i):
    os.system("rm -rf /var/lib/edged/pods/" + i)
    print("delete %s" % i)

with os.popen("mount") as m:
    d_info = m.read().split("\n")

def umount(uuid):
    global d_info
    ret = tuple(filter(lambda u:uuid in u, d_info))
    if ret:
        drv = ret[0].split()[2]
        print("umounting %s" % drv)
        os.system("umount "+drv)
        

with open("log") as f:
    deleted = set()
    compiled = re.compile(r'Orphaned pod "([a-f0-9-]+)"')
    for line in f.readlines():
        g = compiled.search(line)
        if g is None:
            continue
        g = g.groups()
        if g[0] not in deleted and os.path.exists("/var/lib/edged/pods/"+g[0]):
            umount(g[0])
            delete(g[0])
            deleted.add(g[0])
print("%d volumes have been deleted." % len(deleted))
