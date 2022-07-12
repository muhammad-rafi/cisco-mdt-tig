from ncclient import manager
import xmltodict
import xml.dom.minidom

# Device params in dict format
device = {
   'host': '10.100.5.203',
   'netconf_port': '830',
   'username': 'admin',
   'password': 'C1sco123'
}

subscription_payload = '''
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
 <mdt-config-data xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-mdt-cfg">
  <mdt-subscription>
   <subscription-id>101</subscription-id>
   <base>
    <stream>yang-push</stream>
    <encoding>encode-kvgpb</encoding>
    <period>1000</period>
    <xpath>/process-cpu-ios-xe-oper:cpu-usage/cpu-utilization/five-seconds</xpath>
   </base>
   <mdt-receivers>
    <address>10.250.77.182</address>
    <port>57000</port>
    <protocol>grpc-tcp</protocol>
   </mdt-receivers>
  </mdt-subscription>
 </mdt-config-data>
</config>
'''

subtree_oper_filter = """
    <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
       <mdt-oper-data xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-mdt-oper">
         <mdt-subscriptions>
            <subscription-id>101</subscription-id>
        </mdt-subscriptions>
      </mdt-oper-data>
    </filter>
   """

subtree_config_filter = """
    <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
       <mdt-config-data xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-mdt-cfg">
         <mdt-subscription>
            <subscription-id></subscription-id>
        </mdt-subscription>
      </mdt-config-data>
    </filter>
"""


# subscription_payload = open('iosxe_mdt_sub_playload.xml').read()

with manager.connect(host=device['host'], 
                     port=device['netconf_port'], 
                     username=device['username'],
                     password=device['password'], 
                     device_params={'name':'csr'}, 
                     hostkey_verify=False,
                     look_for_keys=False) as m:

    response = m.edit_config(subscription_payload, target="running")

    if response.ok:
        print("Subscribed successfully")
    else: 
        print(response)

    # Get the telemetry config for subscription IDs
    mdt_config = m.get_config(source="running", filter=subtree_config_filter)
    print(xml.dom.minidom.parseString(mdt_config.xml).toprettyxml())

    # Get the telemetry state for specific subscription by ID
    mdt_oper = m.get(subtree_oper_filter)
    mdt_oper_xml = xml.dom.minidom.parseString(mdt_oper.xml)
    print(mdt_oper_xml.toprettyxml())