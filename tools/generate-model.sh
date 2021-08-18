#!/usr/bin/env bash
# http://www.davekuhlman.org/generateDS.html#how-to-build-and-install-it
# make sure to download and extract generateDS project into ~/Downloads folder and/or adapt path
python3 ~/Downloads/generateDS-2.39.2/generateDS.py -f --export="etree validate"  --member-specs=dict --always-export-default -o ../ancpbids/model.py ../ancpbids/data/schema-files/bids.xsd