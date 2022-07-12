from ncclient import manager
from ncclient.xml_ import to_ele
import logging
import xmltodict
import xml.dom.minidom as md
import lxml.etree as et
import sys

# logging.basicConfig(filename='debug_nxos.log',level=logging.DEBUG)

def create_netconf_session(host, username, password, netconf_port=830):
    """ creates netconf session with the remote device"""
    try:
        netconf_session = manager.connect(host=host,
                                        port=netconf_port,
                                        username=username,
                                        password=password,
                                        hostkey_verify=False)

    except Exception as error: 
        sys.exit(error)

    return netconf_session


def get_capabilities(netconf_session, host):
    """ print all NETCONF supported capabilities """

    print('\n~~~~~ Supported Capabilities for {} ~~~~~\n'.format(host))
    for capability in netconf_session.server_capabilities:
        print(capability.split('?')[0])

def get_device_config(netconf_session, config_filter):
    """ get device config for the specifi filter"""

    # Run a "get-config" RPC with the config_filter defined above
    config_resp = netconf_session.get_config(source="running", filter=("subtree", config_filter))

    return config_resp.xml


def get_device_opper(netconf_session, oper_filter):
    """ get device operational data for the specifi filter"""

    # Run a "get-config" RPC with the config_filter defined above
    oper_resp = netconf_session.get(oper_filter)

    return oper_resp.xml


def get_event_streams(netconf_session, xml_filter):
    """ Gets event streams with xml subtree filter """

    try:
        # To return the event streams in XML format (default)
        event_streams = netconf_session.get(xml_filter)

    except Exception as error: 
        sys.exit(error)

    return event_streams

def subs_event(netconf_session, sub_rpc):
    """ subcribe to specifc events or stream 
    """

    try:
        response = netconf_session.dispatch(to_ele(sub_rpc))
        print(response.xml)
        
    except Exception as error: 
        sys.exit(error)

    return response

if __name__ == '__main__':

    # Remote device parameters define in dictionary format 
    device = {
        'host': '10.100.5.205',
        'netconf_port': 830,
        'username': 'admin',
        'password': 'C1sco123'
    }

    # Get config using the subtree filter in the body of the xml rpc
    xml_filter = '''
        <filter type="subtree" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
            <netconf xmlns="urn:ietf:params:xml:ns:netmod:notification">
                <streams/>
            </netconf>
        </filter>
        '''

    # Create a netconf session 
    netconf_session = create_netconf_session(**device)

    # # Get the device netconf supported capabilities 
    # netconf_capabilities = get_capabilities(netconf_session, device['host'])
    # sys.exit(netconf_capabilities)

    # # Get the event_streams_response
    # event_streams_response = get_event_streams(netconf_session, xml_filter)
    # print(event_streams_response)

    # # Get configuration for the interfaces 
    # config_filter = """
    #     <interfaces xmlns="http://openconfig.net/yang/interfaces">
    #         <interface>
    #             <name>eth1/2</name>
    #         </interface>
    #     </interfaces>
    # """
    # print(get_device_config(netconf_session, config_filter))

    # Get operationl data with the config filter 
    # oper_filter = """
    #     <filter>
    #     <interfaces xmlns="http://openconfig.net/yang/interfaces">
    #         <interface>
    #         <name>eth1/2</name>
    #         <state>
    #             <type/>
    #             <mtu/>
    #             <enabled/>
    #             <admin-status/>
    #             <oper-status/>
    #         </state>
    #         <ethernet xmlns="http://openconfig.net/yang/interfaces/ethernet">
    #             <state/>
    #         </ethernet>
    #         </interface>
    #     </interfaces>
    #     </filter>
    # """
    # oper_filter = """
    #     <filter>
    #     <interfaces xmlns="http://openconfig.net/yang/interfaces">
    #         <interface>
    #         <name>eth1/2</name>
    #         <state/>
    #         </interface>
    #     </interfaces>
    #     </filter>
    # """
    # print(get_device_opper(netconf_session, oper_filter))

    # subscribes to interface event notifications
    sub_rpc = '''
        <create-subscription xmlns="urn:ietf:params:xml:ns:netconf:notification:1.0">
            <stream>NETCONF</stream>
            <filter xmlns:ns1="urn:ietf:params:xml:ns:netconf:base:1.0" type="subtree">
                <interfaces xmlns="http://openconfig.net/yang/interfaces">
                    <interface>
                        <name>eth1/2</name>
                            <state/>
                    </interface>
                </interfaces>
            </filter>
        </create-subscription>
        '''
        
    # event subscription response
    subs_event_resp = subs_event(netconf_session, sub_rpc)
    # print(subs_event_resp)

    # Receiving event notifications while subscribed YANG model
    while netconf_session.connected:
        print('Notification Recieved ....')
        sub_notif = netconf_session.take_notification(timeout = 10)
        
        if sub_notif != None:
            print(sub_notif.notification_xml)

        