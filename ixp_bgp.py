#!/usr/bin/env python
import requests
import jinja2
import os

r = requests.get('https://portal.lonap.net/apiv1/member-list/list')
ixp_members = r.json()['member_list']

for ixp in ixp_members:
	print(ixp)
