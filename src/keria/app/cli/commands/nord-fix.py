# -*- encoding: utf-8 -*-
"""
KERI
keri.kli.commands module

"""
import argparse

from hio import help
from hio.base import doing
from keri import kering
from keri.db import basing as kbase
from keria.db import basing

logger = help.ogler.getLogger()

parser = argparse.ArgumentParser(description='Fix NordLEI database')
parser.set_defaults(handler=lambda args: handler(args),
                    transferable=True)
parser.add_argument('--base', '-b', help='additional optional prefix to file location of KERI keystore',
                    required=False, default="")
parser.add_argument('--force', action="store_true", required=False,
                    help='True means perform fix without prompting the user')


def handler(args):
    if not args.force:
        print()
        print("This command will remove entries from your reply database that have no corresponding eans entry.")
        print("This action cannot be undone.")
        print()
        yn = input("Are you sure you want to continue? [y|N]: ")

        if yn not in ("y", "Y"):
            print("...exiting")
            return []

    kwa = dict(args=args)
    return [doing.doify(fix, **kwa)]


def fix(tymth, tock=0.0, **opts):
    _ = (yield tock)
    args = opts["args"]

    adb = basing.AgencyBaser(name="TheAgency", base=args.base, reopen=True, temp=False)

    for ((caid,), _) in adb.agnt.getItemIter():
        print(f"{caid}")
        db = kbase.Baser(name=caid,
                         base=args.base,
                         temp=False,
                         reopen=False)
        try:
            db.reopen()
        except kering.DatabaseError:
            return -1

        # fix eans
        to_delete = []
        for k, v in db.eans.getItemIter():
            if db.rpys.get(keys=(v.qb64,)) is None:
                to_delete.append(k)

        print(f"Removing {to_delete}")
        for k in to_delete:
            db.eans.rem(k)

        # fix ends
        to_delete = []
        for k, v in db.ends.getItemIter():
            if db.eans.get(keys=k) is None:
                to_delete.append(k)

        print(f"Removing {to_delete}")
        for k in to_delete:
            db.ends.rem(k)
