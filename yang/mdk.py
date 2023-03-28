#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lxml.etree import QName
from pyangbind.lib.serialise import *
from ncclient import manager
from lxml import etree
import parsejson

class MDK:

    def __init__(self):
        netconf_data = parsejson.get_config_data()
        host = netconf_data.get('host')
        port = netconf_data.get('port')
        username = netconf_data.get('username')
        password = netconf_data.get('password')
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def conn(self):
        try:
            conn = manager.connect(host=self.host, port=self.port, username=self.username, password=self.password,
                                hostkey_verify=False, timeout=120, look_for_keys=False, device_params={'name': 'huaweiyang'})
            return conn
        except Exception as a:
            print(a)

    def merge(self, python_obj, xpath=None, namespace=None):
        conn = self.conn()
        xml = pybindIETFXMLEncoder.serialise(python_obj)
        config_node = etree.Element("config", nsmap={None: "urn:ietf:params:xml:ns:netconf:base:1.0"})
        root = etree.fromstring(xml.encode("UTF-8"))
        data = root.xpath(xpath, namespaces=namespace)
        target_node = data[0]
        target_node.attrib[QName("urn:ietf:params:xml:ns:netconf:base:1.0", "operation")] = "merge"
        config_node.append(root)
        edit_xml = etree.tostring(config_node, pretty_print=True).decode("utf8")
        print("edit_xml:", edit_xml)
        rpc_reply = conn.edit_config(target="running", config=edit_xml)
        print("rpc_reply:", rpc_reply)
        return rpc_reply

    def create(self, python_obj, xpath=None, namespace=None):
        conn = self.conn()
        xml = pybindIETFXMLEncoder.serialise(python_obj)
        config_node = etree.Element("config", nsmap={None: "urn:ietf:params:xml:ns:netconf:base:1.0"})
        root = etree.fromstring(xml.encode("UTF-8"))
        data = root.xpath(xpath, namespaces=namespace)
        target_node = data[0]
        target_node.attrib[QName("urn:ietf:params:xml:ns:netconf:base:1.0", "operation")] = "create"
        config_node.append(root)
        edit_xml = etree.tostring(config_node, pretty_print=True).decode("utf8")
        print("edit_xml:", edit_xml)
        rpc_reply = conn.edit_config(target="running", config=edit_xml)
        print("rpc_reply:", rpc_reply)
        return rpc_reply

    def delete(self, python_obj, xpath=None, namespace=None):
        conn = self.conn()
        xml = pybindIETFXMLEncoder.serialise(python_obj)
        config_node = etree.Element("config", nsmap={None: "urn:ietf:params:xml:ns:netconf:base:1.0"})
        root = etree.fromstring(xml.encode("UTF-8"))
        data = root.xpath(xpath, namespaces=namespace)
        target_node = data[0]
        target_node.attrib[QName("urn:ietf:params:xml:ns:netconf:base:1.0", "operation")] = "delete"
        config_node.append(root)
        edit_xml = etree.tostring(config_node, pretty_print=True).decode("utf8")
        print("edit_xml:", edit_xml)
        rpc_reply = conn.edit_config(target="running", config=edit_xml)
        print("rpc_reply:", rpc_reply)
        return rpc_reply

    def replace(self, python_obj, xpath=None, namespace=None):
        conn = self.conn()
        xml = pybindIETFXMLEncoder.serialise(python_obj)
        config_node = etree.Element("config", nsmap={None: "urn:ietf:params:xml:ns:netconf:base:1.0"})
        root = etree.fromstring(xml.encode("UTF-8"))
        data = root.xpath(xpath, namespaces=namespace)
        target_node = data[0]
        target_node.attrib[QName("urn:ietf:params:xml:ns:netconf:base:1.0", "operation")] = "replace"
        config_node.append(root)
        edit_xml = etree.tostring(config_node, pretty_print=True).decode("utf8")
        print("edit_xml:", edit_xml)
        rpc_reply = conn.edit_config(target="running", config=edit_xml)
        print("rpc_reply:", rpc_reply)
        return rpc_reply

    def getconfig(self, python_obj, binding, entrance_name):
        conn = self.conn()
        xml = pybindIETFXMLEncoder.serialise(python_obj)
        root = etree.fromstring(xml)
        config_node = etree.Element("filter", nsmap={None: "urn:ietf:params:xml:ns:netconf:base:1.0"})
        config_node.append(root)
        get_xml = etree.tostring(config_node, pretty_print=True).decode("utf8")
        res = conn.get_config(source="running", filter=get_xml)
        print("res:", res)
        rpc_reply = etree.fromstring(str(res).encode("UTF-8"))
        ns = {"nc": "urn:ietf:params:xml:ns:netconf:base:1.0"}
        path = "/nc:rpc-reply/nc:data"
        data = rpc_reply.xpath(path, namespaces=ns)
        py_obj = pybindIETFXMLDecoder.decode(etree.tostring(data[0]), binding, entrance_name)
        return py_obj
