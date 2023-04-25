#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import json

def get_config_data():
    if os.path.exists(os.path.abspath(os.path.join(os.path.dirname(__file__), "../conf", "mdk.json"))):
        conf_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../conf", "mdk.json"))
        with open(conf_path, 'r') as f:
            try:
                data = json.load(f)
            except Exception as e:
                sys.stderr.write(": Error : netconf.json format error !\n")
        return data
    else:
        sys.stderr.write(": Error : netconf.json is not found !\n")
