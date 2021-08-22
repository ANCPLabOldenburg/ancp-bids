#!/usr/bin/env bash
# http://www.davekuhlman.org/generateDS.html#how-to-build-and-install-it
# adapt path to generateDS.py to your own installation path
python3 ../../../hg-repos/generateds-code/generateDS.py -f --export="etree validate generator" --member-specs=dict --always-export-default -o ../ancpbids/model.py ../ancpbids/data/schema-files/bids.xsd