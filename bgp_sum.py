from jnpr.junos import Device 
from lxml import etree

def get_bgp():
    device = Device()

    device.open()

    bgp_sum_xml = device.rpc.get_bgp_summary_information()
    bgp_neighbors_xml = device.rpc.get_bgp_neighbor_information()
    config_bgp_xml = device.rpc.get_config(filter_xml=etree.XML('<configuration><protocols><bgp/></protocols></configuration>'))
    
    device.close()

    return bgp_sum_xml, bgp_neighbors_xml, config_bgp_xml

def main():
    bgp_sum_xml, bgp_neighbors_xml, config_bgp_xml = get_bgp()

    # Get BGP peer advertised routes and peer group from bgp_neighbors_xml 
    bgp_info = {}
    for bgp_peer_info in bgp_neighbors_xml.getiterator(tag='bgp-peer'):
        bgp_info_address = bgp_peer_info.find('peer-address').text.split('+')[0]
        bgp_info_rib = bgp_peer_info.find("bgp-rib")

        if bgp_peer_info.find('peer-group').text is None:
            bpg_info_group = ""
        else:
            bpg_info_group = bgp_peer_info.find('peer-group').text

        if bgp_info_rib is None:
            bpg_info_adv_prefixes = bgp_info[bgp_info_address] = 0
        else:
            bpg_info_adv_prefixes = bgp_info_rib.find("advertised-prefix-count").text

        bgp_info[bgp_info_address] = [bpg_info_adv_prefixes, bpg_info_group]

    for summ in bgp_sum_xml:
        for peer in summ.getiterator(tag='bgp-peer'):
            peer_state = peer.find('peer-state').text
            peer_address = peer.find('peer-address').text
            peer_advertised_prefixes = bgp_info[peer_address][0]
            peer_group = bgp_info[peer_address][1]

            if peer_advertised_prefixes is None:
                print(f"Error while get peer_advertised_prefixes")
                peer_advertised_prefixes = "None"

            peer_description = peer.find('description')

            # Get BGP peer description
            if peer_description is None:
                peer_description = ""
            else:
                peer_description = peer_description.text

            # Get BGP peer state
            if peer_state == "Established":
                bgp_rib = peer.find("bgp-rib")
                routes = bgp_rib.find("active-prefix-count").text + "/" + bgp_rib.find("received-prefix-count").text + "/" + bgp_rib.find("accepted-prefix-count").text + " | "+ str(peer_advertised_prefixes)
            else:
                routes = ""

            print(peer.find('peer-address').text + "\t"  + peer.find('peer-as').text + "\t" + peer_state + "\t" + routes + "\t" + peer.find('elapsed-time').text + "\t" + peer_group + "\t" + peer_description + "\t" +" flaps: " + peer.find('flap-count').text)
            
            
if __name__ == '__main__':
    main()