import threading
import json
import os
import time
from datetime import datetime
from collections import defaultdict

try:
    from scapy.all import sniff, IP, TCP, UDP, ICMP, DNS, DNSQR, ARP
except ImportError:
    pass

class NetworkSniffer:
    def __init__(self, interface=None):
        self.interface = interface
        self.running = False
        self.data_dir = "data"
        os.makedirs(self.data_dir, exist_ok=True)
        
        self.stats = {
            "packets": [],
            "protocols": defaultdict(int),
            "dns_queries": [],
            "arp_alerts": [],
            "arp_table": {}
        }
        
    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._sniff_loop)
        self.thread.daemon = True
        self.thread.start()
        
        self.save_thread = threading.Thread(target=self._save_loop)
        self.save_thread.daemon = True
        self.save_thread.start()

    def stop(self):
        self.running = False
        if hasattr(self, 'thread'):
            self.thread.join(timeout=2)
        if hasattr(self, 'save_thread'):
            self.save_thread.join(timeout=2)
        
        # update status on exit
        try:
            with open(os.path.join(self.data_dir, "status.json"), "w") as f:
                json.dump({"running": False, "count": len(self.stats["packets"])}, f)
        except:
            pass
            
    def _sniff_loop(self):
        try:
            sniff(iface=self.interface, prn=self._process_packet, store=False, stop_filter=lambda x: not self.running)
        except Exception as e:
            with open(os.path.join(self.data_dir, "error.log"), "w") as f:
                f.write(str(e))

    def _process_packet(self, packet):
        if not self.running: return
        
        info = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "protocol": "UNKNOWN",
            "src_ip": "Unknown",
            "dst_ip": "Unknown",
            "src_port": "",
            "dst_port": "",
            "length": len(packet)
        }

        if packet.haslayer(ARP):
            info["protocol"] = "ARP"
            info["src_ip"] = packet[ARP].psrc
            info["dst_ip"] = packet[ARP].pdst
            
            if packet[ARP].op == 2: # Reply
                src_ip = packet[ARP].psrc
                src_mac = packet[ARP].hwsrc
                if src_ip in self.stats["arp_table"] and self.stats["arp_table"][src_ip] != src_mac:
                    alert = {
                        "timestamp": info["timestamp"],
                        "ip": src_ip,
                        "original_mac": self.stats["arp_table"][src_ip],
                        "spoofed_mac": src_mac
                    }
                    self.stats["arp_alerts"].append(alert)
                else:
                    self.stats["arp_table"][src_ip] = src_mac

        if packet.haslayer(IP):
            info["src_ip"] = packet[IP].src
            info["dst_ip"] = packet[IP].dst
            
            if packet.haslayer(TCP):
                tcp = packet[TCP]
                info["src_port"] = tcp.sport
                info["dst_port"] = tcp.dport
                info["protocol"] = self._identify_tcp_protocol(tcp.sport, tcp.dport)
                
            elif packet.haslayer(UDP):
                udp = packet[UDP]
                info["src_port"] = udp.sport
                info["dst_port"] = udp.dport
                info["protocol"] = self._identify_udp_protocol(udp.sport, udp.dport)
                
                if packet.haslayer(DNS) and packet.haslayer(DNSQR):
                    info["protocol"] = "DNS"
                    qname = packet[DNSQR].qname.decode(errors='ignore').rstrip('.')
                    self.stats["dns_queries"].append({
                        "timestamp": info["timestamp"],
                        "source": info["src_ip"],
                        "query": qname
                    })
                    
            elif packet.haslayer(ICMP):
                info["protocol"] = "ICMP"
        
        self.stats["packets"].append(info)
        self.stats["protocols"][info["protocol"]] += 1
        
        if len(self.stats["packets"]) > 5000:
            self.stats["packets"] = self.stats["packets"][-5000:]
            
        if len(self.stats["dns_queries"]) > 500:
            self.stats["dns_queries"] = self.stats["dns_queries"][-500:]

    def _identify_tcp_protocol(self, sport, dport):
        known_ports = {21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS", 80: "HTTP", 443: "HTTPS", 3306: "MySQL"}
        return known_ports.get(dport, known_ports.get(sport, "TCP"))
        
    def _identify_udp_protocol(self, sport, dport):
        known_ports = {53: "DNS", 67: "DHCP", 68: "DHCP", 123: "NTP", 161: "SNMP"}
        return known_ports.get(dport, known_ports.get(sport, "UDP"))
        
    def _save_loop(self):
        while self.running:
            time.sleep(2)
            try:
                with open(os.path.join(self.data_dir, "traffic_data.json"), "w") as f:
                    json.dump({
                        "packets": self.stats["packets"],
                        "protocols": dict(self.stats["protocols"]),
                        "dns_queries": self.stats["dns_queries"],
                        "arp_alerts": self.stats["arp_alerts"]
                    }, f)
                with open(os.path.join(self.data_dir, "status.json"), "w") as f:
                    json.dump({"running": True, "count": len(self.stats["packets"])}, f)
            except:
                pass

if __name__ == "__main__":
    # If run standalone, run indefinitely
    sniffer = NetworkSniffer()
    sniffer.start()
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        sniffer.stop()
