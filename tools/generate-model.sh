#!/usr/bin/env bash
# http://www.davekuhlman.org/generateDS.html#how-to-build-and-install-it
# make sure to download and extract generateDS project into ~/Downloads folder and/or adapt path
python3 ~/Downloads/generateDS-2.39.2/generateDS.py -f --export="write etree"  --member-specs=dict --always-export-default -o ../bids/model.py ../schema/bids.xsd