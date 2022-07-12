from ncclient import manager
import json
import xmltodict
import xml.dom.minidom as md
import lxml.etree as et
from rich import print

# Device params in dict format
device = {
   'host': 'sandbox-iosxe-latest-1.cisco.com',
   'netconf_port': '830',
   'username': 'developer',
   'password': 'C1sco12345'
}

# List of subscriptions for the collector interested to subscribe to
subscriptions = ['/process-cpu-ios-xe-oper:cpu-usage/cpu-utilization/five-seconds',
                '/memory-ios-xe-oper:memory-statistics']

# subscriptions = ['/memory-ios-xe-oper:memory-statistics/memory-statistic']

with manager.connect(host=device['host'], 
                     port=device['netconf_port'], 
                     username=device['username'],
                     password=device['password'], 
                     device_params={'name':'csr'}, 
                     hostkey_verify=False,
                     look_for_keys=False) as m:

    for subscription in subscriptions:
        sub_rpc = f'''
                <establish-subscription xmlns="urn:ietf:params:xml:ns:yang:ietf-event-notifications">
                    <stream xmlns:yp="urn:ietf:params:xml:ns:yang:ietf-yang-push">yp:yang-push</stream>
                    <encoding>encode-xml</encoding>
                    <xpath-filter xmlns="urn:ietf:params:xml:ns:yang:ietf-yang-push">{subscription}</xpath-filter>
                    <period xmlns="urn:ietf:params:xml:ns:yang:ietf-yang-push">500</period>
                </establish-subscription>
                '''
        response = m.dispatch(et.fromstring(sub_rpc))
        response_dict = xmltodict.parse(response.xml)

        # print rpc-reply from the device for above subscriptions
        subscription_id = response_dict['rpc-reply']['subscription-id']['#text']
        print(f'subscription id {subscription_id} has been created')

    while True:
        sub_notif = m.take_notification()
        print('Notification Recieved ....')
        # sub_notif_xml = md.parseString(sub_notif.notification_xml)
        
        # print notifications in pretty xml format
        # print(sub_notif_xml.toprettyxml())

        # print notifications in python dictionary format as json string
        sub_notif_dict = xmltodict.parse(sub_notif.notification_xml)
        print(json.dumps(sub_notif_dict, indent=2, sort_keys = False))


