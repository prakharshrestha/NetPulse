# NetPulse - Real-Time Network Traffic Analyzer & Security Monitor

A full-stack, real-time network monitoring application that combines low-level packet sniffing with a modern interactive web dashboard. Built to demonstrate core Computer Networks concepts including protocol analysis, deep packet inspection, and network security.

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)
![Scapy](https://img.shields.io/badge/Scapy-Packet%20Capture-green)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red?logo=streamlit)
![Plotly](https://img.shields.io/badge/Plotly-Visualization-blue?logo=plotly)

---

## Features

- **Live Packet Capture** — Continuous, real-time sniffing with no fixed packet limit. Start and stop captures directly from the browser-based dashboard.
- **Smart Protocol Detection** — Identifies 18+ application-layer protocols (HTTP, HTTPS, DNS, SSH, FTP, SMTP, MySQL, RDP, etc.) using port-number mapping instead of just reporting TCP/UDP.
- **DNS Query Extraction** — Performs deep packet inspection on UDP port 53 traffic to decode and display the actual domain names being resolved.
- **ARP Spoofing Detection** — Maintains a stateful IP-to-MAC mapping table and monitors ARP replies to detect Man-In-The-Middle attacks on the local network.
- **Interactive Dashboard** — Four-tab Streamlit UI with Plotly charts: Overview (KPIs + live feed), Protocol Analysis (pie/bar charts), Application Logs (DNS queries), and Security Alerts (ARP spoofing).
- **Decoupled Architecture** — Backend sniffer and frontend dashboard run as separate processes communicating through a JSON-based data bridge, ensuring reliability and performance.

---

## Project Architecture

```
                    Network Interface Card
                            |
                            v
                   Scapy Packet Capture
                            |
                            v
                Packet Processor & Classifier
               /            |            \
              v              v              v
        Protocol         DNS Query      ARP Spoofing
        Mapping          Extraction      Detection
              \              |              /
               v             v             v
                   In-Memory Data State
                            |
                            v
                  traffic_data.json (Data Bridge)
                            |
                            v
                   Streamlit + Plotly Dashboard
                  /      |       |        \
                 v       v       v         v
            Overview  Protocol  DNS     Security
              Tab    Analysis   Logs    Alerts Tab
```

---

## Tech Stack

| Technology | Purpose |
|---|---|
| **Python 3** | Core language for backend and frontend |
| **Scapy** | Raw packet capture and deep packet inspection |
| **Streamlit** | Interactive web dashboard framework |
| **Plotly** | Interactive charts (pie, bar, histogram) |
| **Pandas** | Data manipulation and filtering |

---

## Project Structure

```
NetPulse/
|
|-- core/
|   |-- sniffer.py              # Backend capture engine (multi-threaded)
|
|-- data/                       # Auto-generated at runtime
|   |-- traffic_data.json       # Live packet data
|   |-- status.json             # Capture status
|
|-- progress/                   # Build context files
|-- docs/
|   |-- Advanced_Network_Analyzer_Complete_Guide.pdf
|
|-- app.py                      # Streamlit dashboard (frontend)
|-- generate_pdf.py             # Documentation generator
|-- requirements.txt            # Python dependencies
```

---

## Installation

### Prerequisites
- Python 3.8+
- [Npcap](https://npcap.com/#download) (Windows) — check "Install in WinPcap API-compatible Mode" during setup
- Linux/macOS: Run with `sudo` for raw socket access

### Setup

```bash
git clone https://github.com/prakharshrestha/NetPulse.git
cd NetPulse
pip install -r requirements.txt
```

---

## Usage

### Launch the Dashboard

```bash
streamlit run app.py
```

This opens the interactive dashboard at `http://localhost:8501`. From the sidebar:
1. Click **Start Live Capture** to begin sniffing network traffic
2. Browse the web normally to generate traffic
3. Watch the charts and tables update in real-time
4. Click **Stop Capture** when done

### Standalone Capture (CLI)

```bash
python core/sniffer.py
```

Runs the sniffer in the terminal. Press `Ctrl+C` to stop.

---

## Dashboard Tabs

| Tab | What It Shows |
|---|---|
| **Overview** | Total packets, traffic volume, avg packet size, unique IPs, live packet feed |
| **Protocol Analysis** | Protocol distribution donut chart + bar chart |
| **Application Logs** | Table of intercepted DNS queries (timestamp, source, domain) |
| **Security Alerts** | ARP spoofing detection alerts with original vs spoofed MAC addresses |

---

## How It Works

1. **Capture**: Scapy binds to the NIC and captures raw Ethernet frames in a daemon thread
2. **Classify**: Each packet is dissected layer-by-layer (Ethernet → IP → TCP/UDP → Application) and classified using port mapping
3. **Inspect**: DNS packets undergo deep inspection to extract queried domain names. ARP replies are checked against a stateful IP-to-MAC table
4. **Persist**: Every 2 seconds, aggregated data is flushed to JSON files on disk
5. **Visualize**: Streamlit polls the JSON every 3 seconds and renders interactive Plotly charts

---

## Computer Networks Concepts Demonstrated

- TCP/IP Protocol Stack and OSI Layer interactions
- Packet encapsulation and decapsulation
- IP addressing and transport-layer port multiplexing
- DNS resolution process
- ARP protocol mechanics and MITM vulnerabilities
- Stateful vs stateless packet inspection
- Inter-Process Communication via shared data state

---

## License

This project is open source and available under the [MIT License](LICENSE).
