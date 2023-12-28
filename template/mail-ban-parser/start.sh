#!/bin/bash


cd /opt/mail-ban-parser
source venv/bin/activate
python3 main.py
rm geckodriver.log
deactivate