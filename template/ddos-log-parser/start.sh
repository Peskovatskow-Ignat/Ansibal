#!/bin/bash

source /opt/ddos-log-parser/venv/bin/activate
cd /opt/ddos-log-parser/new_parser
python3 unpacket_arcive.py
deactivate
