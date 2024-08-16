# -*- encoding: utf-8 -*-
"""
KERI
keri.kli.commands module

"""
import argparse

from hio import help
from hio.base import doing
from keri import kering
from keri.db import basing, koming
from keria.db import basing as abase
from keri.app import habbing
from keri.app.cli.common import existing

logger = help.ogler.getLogger()

parser = argparse.ArgumentParser(description='Copy HabitatRecord smid and rmid data')
parser.set_defaults(handler=lambda args: handler(args),
                    transferable=True)
parser.add_argument('--base', '-b', help='additional optional prefix to file location of KERI keystore',
                    required=False, default="")
parser.add_argument('--force', action="store_true", required=False,
                    help='True means perform fix without prompting the user')


def handler(args):
    if not args.force:
        print()
        print("This command will copy data from existing HabitatRecords to the corresponding SignifyGroupHab.")
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

    adb = abase.AgencyBaser(name="TheAgency", base=args.base, reopen=True, temp=False)

    for ((caid,), _) in adb.agnt.getItemIter():
        print(f"{caid}")
        db = basing.Baser(name=caid,
                          base=args.base,
                          temp=False,
                          reopen=False)
        try:
            db.reopen()
        except kering.DatabaseError:
            return -1

        habs = koming.Komer(db=db,
                            subkey='habs.',
                            schema=basing.HabitatRecord, )

        hbr = habs.get(keys=(caid,))
        print(hbr.hid)
        print(hbr.smids)
        print(hbr.rmids)

        with existing.existingHby(name=caid, base=args.base) as hby:
            hab = hby.habByName(caid)
            if isinstance(hab, habbing.SignifyGroupHab):
                hab.smids = hbr.smids
                hab.rmids = hbr.rmids
                print(f"{caid} is a sig group hab")
                continue


