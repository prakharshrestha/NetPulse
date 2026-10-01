import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from fpdf import FPDF
import os

IMG_DIR = os.path.join(os.path.dirname(__file__), "progress")
os.makedirs(IMG_DIR, exist_ok=True)

# ─────────────────────────────────────────────────────────
# DIAGRAM 1 — System Architecture
# ─────────────────────────────────────────────────────────
def draw_system_architecture():
    fig, ax = plt.subplots(figsize=(11, 7))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 7)
    ax.axis('off')
    fig.patch.set_facecolor('white')

    def box(x, y, w, h, text, color, fontsize=9, bold=False):
        rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15",
                              facecolor=color, edgecolor='#333333', linewidth=1.5)
        ax.add_patch(rect)
        weight = 'bold' if bold else 'normal'
        ax.text(x + w/2, y + h/2, text, ha='center', va='center',
                fontsize=fontsize, fontweight=weight, wrap=True)

    def arrow(x1, y1, x2, y2, label='', color='#333333'):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color=color, lw=1.8))
        if label:
            mx, my = (x1+x2)/2, (y1+y2)/2
            ax.text(mx, my + 0.15, label, ha='center', va='bottom', fontsize=7,
                    color='#555555', fontstyle='italic')

    # Title
    ax.text(5.5, 6.7, "System Architecture Diagram", ha='center', va='center',
            fontsize=14, fontweight='bold', color='#1a1a2e')

    # ── Layer labels ──
    ax.text(0.15, 6.1, "NETWORK\nLAYER", fontsize=7, color='#888', fontweight='bold', va='center')
    ax.text(0.15, 4.5, "BACKEND\nENGINE", fontsize=7, color='#888', fontweight='bold', va='center')
    ax.text(0.15, 2.4, "DATA\nBRIDGE", fontsize=7, color='#888', fontweight='bold', va='center')
    ax.text(0.15, 0.8, "FRONTEND\nUI", fontsize=7, color='#888', fontweight='bold', va='center')

    # Horizontal separators
    for yy in [5.5, 3.4, 1.6]:
        ax.plot([0.8, 10.5], [yy, yy], color='#cccccc', linestyle='--', linewidth=0.8)

    # ── Network Layer ──
    box(3.5, 5.7, 4, 0.7, "Network Interface Card\n(Wi-Fi / Ethernet Adapter)", '#e3f2fd', 9, True)

    # ── Backend Engine ──
    box(1.2, 4.3, 2.5, 0.9, "Scapy\nPacket Capture\n(sniff loop)", '#fff3e0', 8)
    box(4.3, 4.3, 2.5, 0.9, "Packet Processor\n& Protocol Classifier\n(port mapping)", '#e8f5e9', 8)
    box(7.5, 4.3, 2.5, 0.9, "ARP Spoofing\nDetector\n(stateful check)", '#ffebee', 8)
    box(4.3, 3.5, 2.5, 0.6, "In-Memory State\n(stats, packets, alerts)", '#f3e5f5', 8)

    # ── Data Bridge ──
    box(2.0, 1.8, 2.5, 0.7, "traffic_data.json\n(packets, protocols, DNS)", '#fffde7', 8)
    box(5.5, 1.8, 2.0, 0.7, "status.json\n(running, count)", '#fffde7', 8)

    # ── Frontend ──
    box(1.5, 0.2, 2, 1.0, "Streamlit UI\n+ Plotly Charts", '#e8eaf6', 9, True)
    box(4.0, 0.2, 1.8, 1.0, "Overview\nTab", '#c5cae9', 8)
    box(6.0, 0.2, 1.8, 1.0, "Protocol\nAnalysis Tab", '#c5cae9', 8)
    box(8.0, 0.2, 1.4, 1.0, "DNS\nLogs Tab", '#c5cae9', 8)
    box(9.6, 0.2, 1.2, 1.0, "Security\nAlerts Tab", '#ffcdd2', 8)

    # ── Arrows ──
    arrow(5.5, 5.7, 2.5, 5.2, "Raw Frames")
    arrow(3.7, 4.75, 4.3, 4.75, "Parsed")
    arrow(6.8, 4.75, 7.5, 4.75, "ARP Replies")
    arrow(5.5, 4.3, 5.5, 4.1, "")
    arrow(8.75, 4.3, 7.0, 3.85, "Alerts")
    arrow(3.2, 3.5, 3.2, 2.5, "Write\nevery 2s")
    arrow(5.8, 3.5, 6.2, 2.5, "")
    arrow(3.2, 1.8, 2.5, 1.2, "Reads")
    arrow(6.5, 1.8, 6.9, 1.2, "Reads")

    plt.tight_layout()
    path = os.path.join(IMG_DIR, "architecture.png")
    plt.savefig(path, dpi=180, bbox_inches='tight', facecolor='white')
    plt.close()
    return path

# ─────────────────────────────────────────────────────────
# DIAGRAM 2 — Data Flow (Step-by-step)
# ─────────────────────────────────────────────────────────
def draw_data_flow():
    fig, ax = plt.subplots(figsize=(11, 6))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 6)
    ax.axis('off')
    fig.patch.set_facecolor('white')

    ax.text(5.5, 5.7, "End-to-End Data Flow Diagram", ha='center',
            fontsize=14, fontweight='bold', color='#1a1a2e')

    steps = [
        ("User clicks\n'Start Live Capture'\non Streamlit UI", '#bbdefb'),
        ("Streamlit spawns\nsniffer.py as\nbackground process", '#c8e6c9'),
        ("Scapy binds to\nNIC and starts\ncapturing packets", '#fff9c4'),
        ("Each packet parsed:\nEthernet > IP >\nTCP/UDP > App Layer", '#ffe0b2'),
        ("Protocol identified\nvia port mapping\n(80=HTTP, 53=DNS...)", '#f8bbd0'),
        ("DNS queries extracted,\nARP replies checked\nfor spoofing", '#e1bee7'),
        ("Aggregated data\nwritten to JSON files\nevery 2 seconds", '#b2dfdb'),
        ("Streamlit reads JSON,\nrenders Plotly charts\nevery 3 seconds", '#d1c4e9'),
    ]

    positions = [
        (0.3, 3.8), (2.7, 3.8), (5.1, 3.8), (7.5, 3.8),
        (0.3, 1.0), (2.7, 1.0), (5.1, 1.0), (7.5, 1.0),
    ]

    for i, ((x, y), (text, color)) in enumerate(zip(positions, steps)):
        rect = FancyBboxPatch((x, y), 2.1, 1.5, boxstyle="round,pad=0.15",
                              facecolor=color, edgecolor='#444', linewidth=1.3)
        ax.add_patch(rect)
        ax.text(x + 1.05, y + 1.15, f"Step {i+1}", ha='center', fontsize=8,
                fontweight='bold', color='#333')
        ax.text(x + 1.05, y + 0.55, text, ha='center', va='center', fontsize=8)

        # Arrows
        if i < 3:
            ax.annotate('', xy=(positions[i+1][0], positions[i+1][1]+0.75),
                        xytext=(x+2.1, y+0.75),
                        arrowprops=dict(arrowstyle='->', color='#333', lw=1.5))
        elif i == 3:
            ax.annotate('', xy=(positions[4][0]+2.1, positions[4][1]+1.5),
                        xytext=(x+1.05, y),
                        arrowprops=dict(arrowstyle='->', color='#333', lw=1.5,
                                        connectionstyle='arc3,rad=0.3'))
        elif i >= 4 and i < 7:
            ax.annotate('', xy=(positions[i+1][0], positions[i+1][1]+0.75),
                        xytext=(x+2.1, y+0.75),
                        arrowprops=dict(arrowstyle='->', color='#333', lw=1.5))

    plt.tight_layout()
    path = os.path.join(IMG_DIR, "dataflow.png")
    plt.savefig(path, dpi=180, bbox_inches='tight', facecolor='white')
    plt.close()
    return path

# ─────────────────────────────────────────────────────────
# DIAGRAM 3 — OSI Layer Mapping
# ─────────────────────────────────────────────────────────
def draw_osi_mapping():
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.5)
    ax.axis('off')
    fig.patch.set_facecolor('white')

    ax.text(5, 5.2, "OSI / TCP-IP Layer Mapping in the Project", ha='center',
            fontsize=13, fontweight='bold', color='#1a1a2e')

    layers = [
        ("Application Layer\n(Layer 7)", "HTTP, DNS, FTP, SSH\nProtocol identification via ports", '#c8e6c9'),
        ("Transport Layer\n(Layer 4)", "TCP ports, UDP ports,\nTCP flags (SYN, ACK, FIN)", '#bbdefb'),
        ("Network Layer\n(Layer 3)", "IP source/destination,\nICMP (ping), ARP", '#fff9c4'),
        ("Data Link Layer\n(Layer 2)", "Ethernet frames,\nMAC addresses, ARP table", '#ffe0b2'),
        ("Physical Layer\n(Layer 1)", "Network Interface Card\n(Wi-Fi / Ethernet)", '#f8bbd0'),
    ]

    for i, (layer, detail, color) in enumerate(layers):
        y = 4.2 - i * 0.9
        # OSI box
        rect = FancyBboxPatch((0.5, y), 3.0, 0.7, boxstyle="round,pad=0.1",
                              facecolor=color, edgecolor='#444', linewidth=1.3)
        ax.add_patch(rect)
        ax.text(2.0, y + 0.35, layer, ha='center', va='center', fontsize=9, fontweight='bold')

        # Arrow
        ax.annotate('', xy=(4.5, y+0.35), xytext=(3.5, y+0.35),
                    arrowprops=dict(arrowstyle='->', color='#666', lw=1.2))

        # Detail box
        rect2 = FancyBboxPatch((4.5, y), 4.8, 0.7, boxstyle="round,pad=0.1",
                               facecolor='#f5f5f5', edgecolor='#999', linewidth=1)
        ax.add_patch(rect2)
        ax.text(6.9, y + 0.35, detail, ha='center', va='center', fontsize=8.5)

    plt.tight_layout()
    path = os.path.join(IMG_DIR, "osi.png")
    plt.savefig(path, dpi=180, bbox_inches='tight', facecolor='white')
    plt.close()
    return path

# ─────────────────────────────────────────────────────────
# DIAGRAM 4 — Protocol Detection Flowchart
# ─────────────────────────────────────────────────────────
def draw_protocol_flowchart():
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis('off')
    fig.patch.set_facecolor('white')

    ax.text(5, 6.7, "Protocol Detection Flowchart", ha='center',
            fontsize=13, fontweight='bold', color='#1a1a2e')

    def diamond(x, y, text, color='#fff9c4'):
        pts = [(x, y+0.45), (x+1.3, y), (x, y-0.45), (x-1.3, y)]
        poly = plt.Polygon(pts, facecolor=color, edgecolor='#444', linewidth=1.3)
        ax.add_patch(poly)
        ax.text(x, y, text, ha='center', va='center', fontsize=8, fontweight='bold')

    def rbox(x, y, w, h, text, color='#c8e6c9'):
        rect = FancyBboxPatch((x-w/2, y-h/2), w, h, boxstyle="round,pad=0.08",
                              facecolor=color, edgecolor='#444', linewidth=1.2)
        ax.add_patch(rect)
        ax.text(x, y, text, ha='center', va='center', fontsize=8)

    def arr(x1, y1, x2, y2, label=''):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color='#333', lw=1.3))
        if label:
            mx, my = (x1+x2)/2, (y1+y2)/2
            ax.text(mx+0.1, my, label, fontsize=7, color='green', fontweight='bold')

    # Start
    rbox(5, 6.2, 2.2, 0.5, "Incoming Packet", '#bbdefb')
    arr(5, 5.95, 5, 5.6)

    diamond(5, 5.2, "Has ARP?")
    arr(5, 4.75, 5, 4.3)
    ax.text(5.15, 4.55, "No", fontsize=7, color='red')
    arr(7.3, 5.2, 8.5, 5.2)
    ax.text(7.5, 5.35, "Yes", fontsize=7, color='green')
    rbox(9.2, 5.2, 1.2, 0.4, "ARP", '#ffcdd2')

    diamond(5, 3.9, "Has IP?")
    arr(5, 3.45, 5, 3.1)
    ax.text(5.15, 3.3, "Yes", fontsize=7, color='green')
    arr(7.3, 3.9, 8.5, 3.9)
    ax.text(7.5, 4.05, "No", fontsize=7, color='red')
    rbox(9.2, 3.9, 1.2, 0.4, "SKIP", '#eeeeee')

    diamond(5, 2.7, "Has TCP?")
    arr(5, 2.25, 5, 1.9)
    ax.text(5.15, 2.1, "No", fontsize=7, color='red')
    arr(3.7, 2.7, 2.0, 2.7)
    ax.text(2.7, 2.85, "Yes", fontsize=7, color='green')

    # TCP branch
    rbox(1.2, 2.7, 1.6, 0.4, "Check TCP Ports", '#e8eaf6')
    arr(1.2, 2.5, 1.2, 2.0)
    rbox(1.2, 1.7, 2.2, 0.45, "80->HTTP  443->HTTPS\n22->SSH  21->FTP", '#c8e6c9')

    diamond(5, 1.5, "Has UDP?")
    arr(5, 1.05, 5, 0.7)
    ax.text(5.15, 0.9, "No", fontsize=7, color='red')
    arr(6.3, 1.5, 7.5, 1.5)
    ax.text(6.5, 1.65, "Yes", fontsize=7, color='green')

    rbox(8.5, 1.5, 1.6, 0.4, "Check UDP Ports", '#e8eaf6')
    arr(8.5, 1.3, 8.5, 0.8)
    rbox(8.5, 0.5, 2.2, 0.45, "53->DNS  67/68->DHCP\n123->NTP  161->SNMP", '#c8e6c9')

    rbox(5, 0.35, 1.4, 0.4, "ICMP", '#ffe0b2')

    plt.tight_layout()
    path = os.path.join(IMG_DIR, "protocol_flow.png")
    plt.savefig(path, dpi=180, bbox_inches='tight', facecolor='white')
    plt.close()
    return path

# ─────────────────────────────────────────────────────────
# DIAGRAM 5 — ARP Spoofing Detection
# ─────────────────────────────────────────────────────────
def draw_arp_detection():
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis('off')
    fig.patch.set_facecolor('white')

    ax.text(5, 4.7, "ARP Spoofing Detection Mechanism", ha='center',
            fontsize=13, fontweight='bold', color='#1a1a2e')

    def rbox(x, y, w, h, text, color):
        rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                              facecolor=color, edgecolor='#444', linewidth=1.3)
        ax.add_patch(rect)
        ax.text(x+w/2, y+h/2, text, ha='center', va='center', fontsize=8.5)

    def arr(x1, y1, x2, y2, label=''):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color='#333', lw=1.5))
        if label:
            mx, my = (x1+x2)/2, (y1+y2)/2
            ax.text(mx, my+0.15, label, ha='center', fontsize=7, fontstyle='italic', color='#555')

    # Normal flow (top)
    ax.text(0.2, 4.1, "Normal Scenario:", fontsize=9, fontweight='bold', color='#2e7d32')
    rbox(0.2, 3.2, 2.0, 0.7, "Router\nIP: 192.168.1.1\nMAC: AA:BB:CC", '#c8e6c9')
    arr(2.2, 3.55, 3.0, 3.55, "ARP Reply")
    rbox(3.0, 3.2, 2.2, 0.7, "Analyzer stores:\nIP->MAC mapping\nin arp_table{}", '#e8eaf6')
    arr(5.2, 3.55, 6.0, 3.55, "Match!")
    rbox(6.0, 3.2, 2.2, 0.7, "MAC matches\nstored record\n= SAFE", '#c8e6c9')

    # Attack flow (bottom)
    ax.text(0.2, 2.3, "Attack Scenario:", fontsize=9, fontweight='bold', color='#c62828')
    rbox(0.2, 1.2, 2.0, 0.8, "Attacker sends\nfake ARP Reply:\nIP: 192.168.1.1\nMAC: XX:YY:ZZ", '#ffcdd2')
    arr(2.2, 1.6, 3.0, 1.6, "ARP Reply")
    rbox(3.0, 1.3, 2.2, 0.6, "Analyzer checks:\nStored MAC != \nReceived MAC", '#fff3e0')
    arr(5.2, 1.6, 6.0, 1.6, "Mismatch!")
    rbox(6.0, 1.2, 2.8, 0.8, "ARP SPOOFING\nDETECTED!\nAlert pushed to\nSecurity Tab", '#ef9a9a')

    plt.tight_layout()
    path = os.path.join(IMG_DIR, "arp_detection.png")
    plt.savefig(path, dpi=180, bbox_inches='tight', facecolor='white')
    plt.close()
    return path


# =============================================================
# PDF GENERATION
# =============================================================
class ProjectPDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 8, 'Advanced Network Analyzer - Project Documentation', align='C')
        self.ln(5)
        self.set_draw_color(200, 200, 200)
        self.line(10, 13, 200, 13)
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')

    def section_title(self, num, title):
        self.set_font('helvetica', 'B', 14)
        self.set_text_color(26, 26, 46)
        self.set_fill_color(230, 240, 255)
        self.cell(0, 10, f'  {num}. {title}', fill=True, new_x="LMARGIN", new_y="NEXT")
        self.ln(4)

    def sub_title(self, title):
        self.set_font('helvetica', 'B', 11)
        self.set_text_color(50, 50, 80)
        self.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def body_text(self, text):
        self.set_font('helvetica', '', 10)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 6, text)
        self.ln(3)

    def bullet(self, text):
        self.set_font('helvetica', '', 10)
        self.set_text_color(40, 40, 40)
        self.cell(8)
        self.cell(5, 6, "-")
        self.multi_cell(0, 6, text)
        self.ln(1)

    def add_diagram(self, path, caption):
        w = 185
        self.image(path, x=12, w=w)
        self.ln(3)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 5, caption, align='C', new_x="LMARGIN", new_y="NEXT")
        self.ln(5)


def build_pdf():
    # Generate all diagrams
    arch_img = draw_system_architecture()
    flow_img = draw_data_flow()
    osi_img = draw_osi_mapping()
    proto_img = draw_protocol_flowchart()
    arp_img = draw_arp_detection()

    pdf = ProjectPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    # ════════════════════════════════════════════════════════
    # COVER PAGE
    # ════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.ln(50)
    pdf.set_font('helvetica', 'B', 28)
    pdf.set_text_color(26, 26, 46)
    pdf.cell(0, 15, 'Advanced Network Analyzer', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    pdf.set_font('helvetica', '', 14)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, 'Comprehensive Project Documentation', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    pdf.set_draw_color(70, 130, 220)
    pdf.set_line_width(0.8)
    pdf.line(60, pdf.get_y(), 150, pdf.get_y())
    pdf.ln(15)
    pdf.set_font('helvetica', '', 11)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 8, 'Subject: Computer Networks', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, 'Technologies: Python, Scapy, Streamlit, Plotly, Pandas', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(30)
    pdf.set_font('helvetica', 'I', 9)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 8, 'Real-Time Packet Capture | Interactive Dashboard | ARP Spoofing Detection', align='C', new_x="LMARGIN", new_y="NEXT")

    # ════════════════════════════════════════════════════════
    # TABLE OF CONTENTS
    # ════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.set_font('helvetica', 'B', 16)
    pdf.set_text_color(26, 26, 46)
    pdf.cell(0, 12, 'Table of Contents', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    toc = [
        ("1", "Introduction and Project Overview"),
        ("2", "Project Structure and File Organization"),
        ("3", "System Architecture"),
        ("4", "OSI / TCP-IP Layer Mapping"),
        ("5", "Detailed Component Breakdown"),
        ("6", "Protocol Detection Mechanism"),
        ("7", "Security Module: ARP Spoofing Detection"),
        ("8", "End-to-End Data Flow"),
        ("9", "Technologies Used"),
        ("10", "Educational Outcomes and Conclusion"),
    ]
    for num, title in toc:
        pdf.set_font('helvetica', '', 11)
        pdf.set_text_color(40, 40, 40)
        pdf.cell(0, 8, f'    {num}.  {title}', new_x="LMARGIN", new_y="NEXT")

    # ════════════════════════════════════════════════════════
    # SECTION 1 — INTRODUCTION
    # ════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("1", "Introduction and Project Overview")

    pdf.sub_title("What is the Advanced Network Analyzer?")
    pdf.body_text(
        "The Advanced Network Analyzer is a full-stack, real-time network monitoring application "
        "built entirely in Python. It combines low-level packet sniffing with a modern, interactive "
        "web-based dashboard to provide comprehensive visibility into local network traffic."
    )
    pdf.body_text(
        "In production and enterprise environments, network administrators use heavyweight tools like "
        "Wireshark or tcpdump for packet-level analysis. This project offers a lightweight, extensible, "
        "and visually appealing alternative that is ideal for educational environments and demonstrations."
    )

    pdf.sub_title("What Does the Project Do?")
    pdf.body_text("The application performs the following core functions:")
    pdf.bullet("Captures live network packets in real-time from the host machine's network interface (Wi-Fi or Ethernet).")
    pdf.bullet("Classifies each packet by identifying its protocol at both the transport layer (TCP, UDP, ICMP) and the application layer (HTTP, HTTPS, DNS, SSH, FTP, DHCP, NTP, SNMP, etc.) using port-number mapping.")
    pdf.bullet("Extracts DNS queries to show exactly which domain names the machine is resolving (e.g., www.google.com, api.github.com).")
    pdf.bullet("Detects ARP Spoofing attacks on the local network by maintaining a stateful IP-to-MAC address mapping table and checking for anomalies.")
    pdf.bullet("Visualizes all captured data through an interactive Streamlit web dashboard with Plotly charts, including protocol distribution pie charts, bar charts, packet size histograms, and traffic volume analysis.")
    pdf.bullet("Provides real-time monitoring with auto-refreshing views and the ability to start/stop captures directly from the browser-based UI.")

    pdf.sub_title("Why This Project Matters for Computer Networks")
    pdf.body_text(
        "This project directly demonstrates the following fundamental Computer Networks concepts: "
        "the TCP/IP protocol stack, packet encapsulation and decapsulation across OSI layers, "
        "IP addressing and routing, the role of transport-layer ports in multiplexing, the DNS "
        "resolution process, ARP protocol mechanics and its vulnerabilities, and network traffic "
        "analysis techniques. By building this system, one gains practical, hands-on experience "
        "with concepts that are typically only studied theoretically in textbooks."
    )

    # ════════════════════════════════════════════════════════
    # SECTION 2 — PROJECT STRUCTURE
    # ════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("2", "Project Structure and File Organization")

    pdf.body_text("The project follows a clean, modular directory structure that separates concerns between the backend engine and the frontend UI:")
    pdf.ln(3)
    pdf.set_font('courier', '', 9)
    pdf.set_text_color(40, 40, 40)
    tree = (
        "Advanced Network Analyzer/\n"
        "|\n"
        "|-- core/\n"
        "|   |-- sniffer.py          # Backend packet capture engine\n"
        "|\n"
        "|-- data/\n"
        "|   |-- traffic_data.json   # Live packet data (auto-generated)\n"
        "|   |-- status.json         # Capture status (auto-generated)\n"
        "|\n"
        "|-- progress/               # Build context and tracking files\n"
        "|\n"
        "|-- app.py                  # Streamlit frontend dashboard\n"
        "|-- requirements.txt        # Python dependencies\n"
        "|-- generate_pdf.py         # This PDF generator script\n"
    )
    pdf.multi_cell(0, 5, tree)
    pdf.ln(5)
    pdf.set_font('helvetica', '', 10)

    pdf.sub_title("File Responsibilities:")
    pdf.bullet("core/sniffer.py: The heart of the application. Contains the NetworkSniffer class that uses Scapy to capture packets, a Packet Processor that classifies protocols, an ARP Spoofing Detector, and a background thread that serializes data to disk.")
    pdf.bullet("app.py: The Streamlit web application that serves as the visual control center. It reads the JSON data files, renders interactive Plotly visualizations, and provides controls to start/stop the capture engine.")
    pdf.bullet("data/traffic_data.json: The shared data bridge between backend and frontend. Contains the list of captured packets, protocol distribution counts, DNS query logs, and ARP spoofing alerts.")
    pdf.bullet("data/status.json: A lightweight file indicating whether the capture engine is currently running and how many packets have been captured so far.")
    pdf.bullet("requirements.txt: Lists the four core Python dependencies: scapy, pandas, streamlit, and plotly.")

    # ════════════════════════════════════════════════════════
    # SECTION 3 — SYSTEM ARCHITECTURE
    # ════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("3", "System Architecture")

    pdf.body_text(
        "The system is designed as a decoupled, two-process architecture. The backend capture "
        "engine and the frontend dashboard run as completely separate processes that communicate "
        "through a shared file-based data bridge. This decoupling provides several important benefits:"
    )
    pdf.bullet("Reliability: If the UI crashes or is restarted, the backend continues capturing packets without interruption.")
    pdf.bullet("Performance: Heavy packet processing does not block UI rendering, and UI interactions (filtering, scrolling) do not affect capture performance.")
    pdf.bullet("Simplicity: Using JSON files as the communication layer avoids the complexity of databases, message queues, or socket-based IPC.")
    pdf.ln(3)

    pdf.add_diagram(arch_img, "Figure 1: Complete System Architecture Diagram showing all components and data flow")

    pdf.body_text(
        "As shown in Figure 1, the architecture is organized into four layers: "
        "(1) The Network Layer provides raw Ethernet frames from the NIC. "
        "(2) The Backend Engine processes these frames through Scapy, classifies protocols, and checks for ARP anomalies. "
        "(3) The Data Bridge (JSON files) acts as the asynchronous communication channel. "
        "(4) The Frontend UI reads this data and renders it through interactive Plotly charts organized across four specialized tabs."
    )

    # ════════════════════════════════════════════════════════
    # SECTION 4 — OSI MAPPING
    # ════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("4", "OSI / TCP-IP Layer Mapping")

    pdf.body_text(
        "One of the key educational aspects of this project is how it interacts with nearly every "
        "layer of the OSI model. The diagram below maps each OSI layer to the specific data that "
        "the analyzer extracts and processes at that layer."
    )
    pdf.ln(2)

    pdf.add_diagram(osi_img, "Figure 2: How the project maps to each layer of the OSI / TCP-IP model")

    pdf.body_text(
        "Physical Layer (Layer 1): The project relies on the host's Network Interface Card (NIC) to convert "
        "electrical or radio signals into digital frames. Scapy binds to this interface to receive raw data."
    )
    pdf.body_text(
        "Data Link Layer (Layer 2): Ethernet frames contain source and destination MAC addresses. The ARP "
        "protocol operates at this layer. Our ARP spoofing detector maintains an IP-to-MAC mapping table "
        "and monitors ARP replies for inconsistencies."
    )
    pdf.body_text(
        "Network Layer (Layer 3): IP packets carry source and destination IP addresses. The project extracts "
        "these addresses for traffic analysis, showing top source IPs and destination IPs. ICMP (ping) also "
        "operates at this layer and is captured and displayed."
    )
    pdf.body_text(
        "Transport Layer (Layer 4): TCP and UDP segments carry port numbers that enable multiplexing. "
        "The project uses these port numbers as the primary mechanism for identifying application-layer "
        "protocols (e.g., port 80 = HTTP, port 443 = HTTPS)."
    )
    pdf.body_text(
        "Application Layer (Layer 7): For specific protocols like DNS, the project performs deep packet "
        "inspection. It reads the DNS Question Record (DNSQR) inside UDP port 53 packets to extract the "
        "actual domain name being queried."
    )

    # ════════════════════════════════════════════════════════
    # SECTION 5 — COMPONENTS
    # ════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("5", "Detailed Component Breakdown")

    pdf.sub_title("5.1 Backend Capture Engine (core/sniffer.py)")
    pdf.body_text(
        "The NetworkSniffer class is the core of the application. When instantiated and started, it launches "
        "two daemon threads: a capture thread and a save thread."
    )
    pdf.body_text(
        "The Capture Thread calls Scapy's sniff() function in a continuous loop. Scapy uses Berkeley Packet "
        "Filter (BPF) at the kernel level for efficient, low-overhead packet interception. Each captured packet "
        "is passed to the _process_packet() callback method, which dissects it layer by layer:"
    )
    pdf.bullet("First, it checks for ARP packets (Layer 2). If found, it extracts the ARP operation (Request or Reply), the source IP, and the destination IP.")
    pdf.bullet("Next, it checks for an IP layer (Layer 3). If absent, the packet is a non-IP frame and is skipped.")
    pdf.bullet("It then checks for TCP (extracting source/destination ports and mapping them to known services), UDP (similarly mapping ports, with special handling for DNS packets), or ICMP (identifying ping requests and replies).")
    pdf.bullet("For DNS packets specifically, it decodes the DNSQR query name to reveal the domain being resolved.")
    pdf.ln(3)

    pdf.body_text(
        "The Save Thread wakes up every 2 seconds and writes the entire in-memory state (packets list, "
        "protocol counts, DNS queries, and ARP alerts) to traffic_data.json. It also updates status.json "
        "with the current running state and packet count. This periodic flush ensures the frontend always "
        "has fresh data without requiring a direct network connection between the processes."
    )
    pdf.body_text(
        "Memory Management: To prevent unbounded memory growth during long capture sessions, the engine "
        "maintains a sliding window of the last 5,000 packets and the last 500 DNS queries. Older entries "
        "are automatically discarded."
    )

    pdf.sub_title("5.2 Frontend Dashboard (app.py)")
    pdf.body_text(
        "The Streamlit dashboard is organized into a sidebar (for controls and filters) and a main content "
        "area with four tabs. Here is a detailed explanation of each component:"
    )
    pdf.bullet("Sidebar - Process Controls: Contains 'Start Live Capture' and 'Stop Capture' buttons. When Start is clicked, the app uses Python's subprocess.Popen to launch core/sniffer.py as an independent background process. The process reference is stored in Streamlit's session state so it can be terminated later.")
    pdf.bullet("Sidebar - Protocol Filters: A multi-select widget populated dynamically from the captured data. Users can select specific protocols (e.g., only DNS and HTTPS) and the entire dashboard re-renders to show only traffic matching those filters.")
    pdf.bullet("Overview Tab: Shows four KPI metric cards (Total Packets, Total Traffic in bytes, Average Packet Size, Unique IPs) and a scrollable table of the most recent 100 captured packets.")
    pdf.bullet("Protocol Analysis Tab: Renders an interactive Plotly donut chart showing protocol distribution and a bar chart showing packet counts per protocol.")
    pdf.bullet("Application Logs Tab: Displays a reverse-chronological table of all intercepted DNS queries, showing timestamp, source IP, and the queried domain name.")
    pdf.bullet("Security Alerts Tab: If ARP spoofing is detected, shows a red alert banner with the count of attacks and a detailed table listing each alert with timestamp, IP, original MAC, and spoofed MAC.")

    # ════════════════════════════════════════════════════════
    # SECTION 6 — PROTOCOL DETECTION
    # ════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("6", "Protocol Detection Mechanism")

    pdf.body_text(
        "One of the distinguishing features of this project is its ability to identify application-layer "
        "protocols rather than simply reporting 'TCP' or 'UDP'. This is achieved through a port-number "
        "mapping system. The flowchart below illustrates the decision tree used to classify each packet."
    )
    pdf.ln(2)

    pdf.add_diagram(proto_img, "Figure 3: Protocol Detection Flowchart showing the classification decision tree")

    pdf.body_text(
        "The classifier works as follows: First, the packet is checked for an ARP layer. If present, it is "
        "immediately classified as ARP. Otherwise, the IP layer is checked. If no IP layer exists, the packet "
        "is skipped. For IP packets, the transport layer determines the next step."
    )
    pdf.body_text(
        "For TCP packets, the source and destination ports are checked against a dictionary of 18+ known "
        "services. For example: Port 80 maps to HTTP, Port 443 to HTTPS, Port 22 to SSH, Port 21 to FTP, "
        "Port 3306 to MySQL, Port 3389 to RDP, and Port 8080 to HTTP-ALT. If no known port is matched, "
        "the packet is labeled simply as 'TCP'."
    )
    pdf.body_text(
        "For UDP packets, a similar dictionary is used: Port 53 maps to DNS, Ports 67/68 to DHCP, Port 123 "
        "to NTP, and Port 161 to SNMP. Additionally, if a UDP packet on port 53 contains a DNS Question "
        "Record (DNSQR), the analyzer performs deep packet inspection to decode the queried domain name."
    )

    # ════════════════════════════════════════════════════════
    # SECTION 7 — ARP SPOOFING
    # ════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("7", "Security Module: ARP Spoofing Detection")

    pdf.sub_title("What is ARP Spoofing?")
    pdf.body_text(
        "Address Resolution Protocol (ARP) is used on local area networks to map IP addresses to physical "
        "MAC addresses. When a device wants to communicate with another device on the same network, it sends "
        "an ARP Request asking 'Who has IP X.X.X.X?'. The device with that IP responds with an ARP Reply "
        "containing its MAC address. The requesting device caches this mapping in its ARP table."
    )
    pdf.body_text(
        "ARP is a stateless, trust-based protocol. It accepts ARP Replies even if it never sent a corresponding "
        "Request. An attacker can exploit this by sending unsolicited ARP Replies to a victim, claiming that the "
        "attacker's MAC address belongs to the router's IP. This redirects all of the victim's internet traffic "
        "through the attacker's machine, enabling a Man-In-The-Middle (MITM) attack."
    )

    pdf.sub_title("How the Analyzer Detects ARP Spoofing")
    pdf.body_text("The detection mechanism is based on stateful inspection of ARP Reply packets:")
    pdf.bullet("Step 1 - State Building: When an ARP Reply is first seen for a given IP, the analyzer stores the IP-to-MAC mapping in an internal dictionary (arp_table).")
    pdf.bullet("Step 2 - Continuous Monitoring: For every subsequent ARP Reply, the analyzer extracts the claimed IP and MAC address from the packet.")
    pdf.bullet("Step 3 - Anomaly Detection: The extracted MAC is compared against the stored MAC for that IP. If they differ, it means someone is attempting to change the routing path.")
    pdf.bullet("Step 4 - Alert Generation: An alert object is created containing the timestamp, the affected IP, the original (legitimate) MAC, and the new (spoofed) MAC. This alert is pushed to the shared JSON state.")
    pdf.bullet("Step 5 - Visual Notification: The Streamlit frontend reads the alerts and displays them prominently in the Security Alerts tab with a red warning banner.")
    pdf.ln(3)

    pdf.add_diagram(arp_img, "Figure 4: ARP Spoofing Detection - Normal vs Attack scenario comparison")

    # ════════════════════════════════════════════════════════
    # SECTION 8 — DATA FLOW
    # ════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("8", "End-to-End Data Flow")

    pdf.body_text(
        "The following diagram illustrates the complete chronological sequence of events from the moment "
        "the user initiates a capture session to the visual rendering of network traffic data on the dashboard."
    )
    pdf.ln(2)

    pdf.add_diagram(flow_img, "Figure 5: End-to-End Data Flow showing all 8 steps from user action to visualization")

    pdf.body_text(
        "Step 1: The user opens the Streamlit dashboard in their browser (typically at http://localhost:8501) "
        "and clicks the 'Start Live Capture' button in the sidebar."
    )
    pdf.body_text(
        "Step 2: The Streamlit application executes subprocess.Popen() to spawn core/sniffer.py as an "
        "independent background process. This ensures the capture runs independently of the UI."
    )
    pdf.body_text(
        "Step 3: The sniffer initializes Scapy and binds to the default network interface. Scapy configures "
        "a raw socket to receive copies of all packets flowing through the NIC."
    )
    pdf.body_text(
        "Step 4: As each packet arrives, it is dissected layer by layer - from Ethernet frame to IP header "
        "to TCP/UDP segment to application-layer payload."
    )
    pdf.body_text(
        "Step 5: Port numbers are mapped to known services (HTTP, DNS, SSH, etc.). Special handling extracts "
        "DNS query names and checks ARP packets against the stored state."
    )
    pdf.body_text(
        "Step 6: The DNS queries extracted from the packets are appended to a list. ARP Reply packets are "
        "cross-referenced with the arp_table dictionary to detect any MAC address changes."
    )
    pdf.body_text(
        "Step 7: Every 2 seconds, a dedicated save-thread writes the complete aggregated state (packets, "
        "protocol counts, DNS logs, and security alerts) to traffic_data.json on disk."
    )
    pdf.body_text(
        "Step 8: The Streamlit UI is on a 3-second auto-refresh cycle. Each cycle, it reads the updated JSON "
        "file, loads it into a Pandas DataFrame, applies any active protocol filters, and re-renders all Plotly "
        "charts and data tables."
    )

    # ════════════════════════════════════════════════════════
    # SECTION 9 — TECHNOLOGIES
    # ════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.section_title("9", "Technologies Used")

    pdf.body_text("The project uses the following technologies, all of which are free and open-source:")
    pdf.ln(2)

    # Simple table
    pdf.set_font('helvetica', 'B', 10)
    pdf.set_fill_color(70, 130, 220)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(45, 8, ' Technology', fill=True, border=1)
    pdf.cell(145, 8, ' Purpose and Role in the Project', fill=True, border=1, new_x="LMARGIN", new_y="NEXT")

    rows = [
        ("Python 3", "Core programming language for both backend and frontend."),
        ("Scapy", "Packet capture and deep packet inspection library. Uses raw sockets to sniff live traffic from the NIC."),
        ("Streamlit", "Reactive web framework for building the interactive dashboard. Handles UI rendering and process management."),
        ("Plotly", "Interactive charting library for pie charts, bar charts, and histograms displayed on the dashboard."),
        ("Pandas", "Data manipulation library. Converts JSON data into DataFrames for filtering, aggregation, and display."),
        ("JSON (stdlib)", "Serialization format for the data bridge between backend and frontend processes."),
        ("Threading (stdlib)", "Python's threading module runs the capture loop and save loop concurrently in daemon threads."),
        ("Subprocess (stdlib)", "Launches and manages the backend sniffer as an independent child process from the Streamlit UI."),
    ]
    pdf.set_font('helvetica', '', 9)
    pdf.set_text_color(40, 40, 40)
    for tech, purpose in rows:
        pdf.set_font('helvetica', 'B', 9)
        pdf.cell(45, 12, f' {tech}', border=1)
        pdf.set_font('helvetica', '', 9)
        pdf.cell(145, 12, f' {purpose}', border=1, new_x="LMARGIN", new_y="NEXT")

    # ════════════════════════════════════════════════════════
    # SECTION 10 — CONCLUSION
    # ════════════════════════════════════════════════════════
    pdf.ln(10)
    pdf.section_title("10", "Educational Outcomes and Conclusion")

    pdf.body_text("By building and studying this project, one gains deep, practical insights into:")
    pdf.bullet("Packet Structure: Understanding Ethernet frames, IP headers, TCP/UDP segments, and application-layer payloads through hands-on dissection.")
    pdf.bullet("Protocol Identification: Learning how port numbers enable multiplexing and how applications are identified at the transport layer.")
    pdf.bullet("DNS Resolution: Observing the actual DNS queries generated by a machine and understanding the role of recursive resolvers.")
    pdf.bullet("Network Security: Understanding how ARP's trust-based design creates vulnerabilities and how stateful inspection can detect attacks.")
    pdf.bullet("Asynchronous Systems: Learning how multi-threaded Python programs coordinate work using daemon threads and shared state.")
    pdf.bullet("Inter-Process Communication: Understanding how two separate processes (sniffer and UI) can communicate through a decoupled file-based data bridge.")
    pdf.bullet("Data Visualization: Using Plotly and Streamlit to transform raw network data into actionable, human-readable insights.")
    pdf.ln(5)

    pdf.body_text(
        "The Advanced Network Analyzer successfully transforms an abstract, high-speed stream of binary "
        "network data into structured, visual, and actionable insights. It serves as both a powerful learning "
        "tool for understanding network protocols at every layer of the OSI model, and a practical utility for "
        "monitoring local network health and security. The entire system operates 100% locally with zero cloud "
        "dependencies, demonstrating that powerful network analysis can be achieved efficiently with Python "
        "and free, open-source libraries."
    )

    # Save
    out_path = os.path.join(os.path.dirname(__file__), "Advanced_Network_Analyzer_Complete_Guide.pdf")
    pdf.output(out_path)
    print(f"PDF generated successfully: {out_path}")
    print(f"Total pages: {pdf.page_no()}")


if __name__ == "__main__":
    build_pdf()
