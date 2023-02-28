#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyangbind.lib.serialise import pybindIETFXMLEncoder
from ncclient import manager
from lxml import etree
import xmltodict
import json
#from huawei_debug import *

class Netconf:

    def __init__(self,*args,**kwargs):
        self.host = kwargs['host']
        self.port = kwargs.get('port')
        self.username = kwargs['username']
        self.passwd = kwargs['passwd']
        self.hostkey_verify=kwargs.get('hostkey_verify',False)
    def conn(self):
        try:
            netconf_conn =  manager.connect(host=self.host,port=self.port,username=self.username,password=self.passwd,hostkey_verify=self.hostkey_verify,
                                            timeout=120,look_for_keys=False, device_params={'name': 'huaweiyang'})
            return netconf_conn
        except Exception as a:
            print(a)
            print("""
            ---------------------------------------------------------------------------------------
            sample: Netconf(host='10.0.3.105',username='netconf-dark',passwd='1234567',port=830)
            """
            )

    def get_module_filter(self):
        huawei_obj = huawei_debug()
        xml = pybindIETFXMLEncoder.serialise(huawei_obj.debug)
        root = etree.fromstring(xml)
        configNode = etree.Element("filter", nsmap={None: "urn:ietf:params:xml:ns:netconf:base:1.0"})
        configNode.append(root)
        netconf_filter = etree.tostring(configNode, pretty_print=True).decode("utf8")
        return netconf_filter

    def get_allconfig(self):
        netconf_conn = self.conn()
        return netconf_conn.get_config(source='running').data_xml

    def get_xml(self,command=None):
        netconf_conn = self.conn()
        rpc_replay = netconf_conn.get_config('running',filter=command)
        return rpc_replay

    def server_capabilities(self):
        netconf_conn = self.conn()
        for capabilities in netconf_conn.server_capabilities:
            print(capabilities)

    def get_dic(self, command=None):
       netconf_conn = self.conn()
       rpc_replay = rpc_replay = netconf_conn.get(filter=command).data_xml
       rpc_dict = xmltodict.parse(rpc_replay)
       return rpc_dict

    def get_json(self, command=None):
        rpc_replay = self.get_dic(command)
        rpc_json = json.dumps(rpc_replay, indent=1)
        return rpc_json

    def edit(self, command=None, target='running'):
        netconf_conn = self.conn()
        res = netconf_conn.edit_config(target=target, config=command)
        return res

if __name__ == '__main__':
  host = ''
  username = ''
  password = ''
  port = 830
  conn = Netconf(host=host, username=username, passwd=password, port=port)
  capabilities = conn.server_capabilities()

  filter = conn.get_module_filter()

  detail_filter = '''<filter>
  <debug xmlns="urn:huawei:yang:huawei-debug">
      <cpu-infos>
        <cpu-info>
          <position>3</position>
        </cpu-info>
      </cpu-infos>
  </debug>
  </filter>'''

  config = '''<config>
  <debug xmlns="urn:huawei:yang:huawei-debug">
      <cpu-infos>
        <cpu-info xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0" xc:operation="merge">
          <position>3</position>
          <overload-threshold>80</overload-threshold>
          <unoverload-threshold>65</unoverload-threshold>
          <interval>10</interval>
        </cpu-info>
      </cpu-infos>
    </debug>
  </config>
  '''

  all_config = conn.get_allconfig()
  res_xml = conn.get_xml(filter)
  res_json = conn.get_json(filter)
  res_moredetails_xml = conn.get_xml(detail_filter)
  res_moredetails_json = conn.get_json(detail_filter)
  with open('allconfig.txt', 'w+') as file:
      file.write(all_config)
  with open('xml.txt', 'w+') as file:
      file.write(str(res_xml))
  with open('json.txt', 'w+') as file:
      file.write(str(res_json))
  with open('more_details_xml.txt', 'w+') as file:
      file.write(str(res_moredetails_xml))
  with open('more_details_json.txt', 'w+') as file:
      file.write(str(res_moredetails_json))
  #res = conn.edit(config)
  #print(res)
