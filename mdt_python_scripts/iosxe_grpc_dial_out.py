from ncclient import manager
import xmltodict
import xml.dom.minidom 
from rich import print

# Device params in dict format
device = {
   'host': '10.100.5.202',
   'netconf_port': '830',
   'username': 'admin',
   'password': 'C1sco123'
}

# Netconf subtree filters for mdt config subscription
subtree_config_filter = """
    <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
       <mdt-config-data xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-mdt-cfg">
         <mdt-subscription>
            <subscription-id></subscription-id>
        </mdt-subscription>
      </mdt-config-data>
    </filter>
   """
subtree_oper_filter = """
    <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
       <mdt-oper-data xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-mdt-oper">
         <mdt-subscriptions>
            <subscription-id>101</subscription-id>
        </mdt-subscriptions>
      </mdt-oper-data>
    </filter>
   """
   
# Netconf xpath filters 
xpath_config_filter = "/mdt-config-data/mdt-subscription/subscription-id"
xpath_oper_filter = "/mdt-oper-data/mdt-subscriptions[subscription-id=101]"

with manager.connect(host=device['host'], 
                     port=device['netconf_port'], 
                     username=device['username'],
                     password=device['password'], 
                     device_params={'name':'iosxe'}, 
                     hostkey_verify=False,
                     look_for_keys=False) as m:

   # # Get the telemetry subscription configured IDs via xpath filter in XML format
   # tele_config = m.get_config(source='running', filter=('xpath', xpath_config_filter))
   # tele_config_xml = xml.dom.minidom.parseString(tele_config.xml)
   # print(tele_config_xml.toprettyxml())
   
   # # Get the telemetry state for specific subscription by ID via xpath filter in XML format
   # tele_oper = m.get(filter=('xpath', xpath_oper_filter))
   # tele_oper_xml = xml.dom.minidom.parseString(tele_oper.xml)
   # print(tele_oper_xml.toprettyxml())

   # # Get the telemetry subscription configured IDs via subtree filter in XML format
   # tele_config_ouput = m.get_config(source='running', filter=subtree_config_filter)
   # tele_config_ouput_xml = xml.dom.minidom.parseString(tele_config_ouput.xml)
   # print(tele_config_ouput_xml.toprettyxml())

   # # Get the telemetry state for specific subscription by ID via xpath filter in XML format
   # tele_oper_ouput = m.get(subtree_oper_filter)
   # tele_oper_ouput_xml = xml.dom.minidom.parseString(tele_oper_ouput.xml)
   # print(tele_oper_ouput_xml.toprettyxml())

   # Get the telemetry subscription configured IDs via xpath filter in python dict  format
   xpath_config_result = m.get_config(source='running', filter=('xpath', xpath_config_filter))
   xpath_result_config_dict = xmltodict.parse(xpath_config_result.xml)["rpc-reply"]["data"]["mdt-config-data"]["mdt-subscription"]
   print(xpath_result_config_dict)
    
   # # Get the telemetry state for specific subscription by ID via xpath filter in python dict format
   # xpath_result = m.get(filter=('xpath', xpath_oper_filter))
   # xpath_result_dict = xmltodict.parse(xpath_result.xml)["rpc-reply"]["data"]
   # print(xpath_result_dict)
   


