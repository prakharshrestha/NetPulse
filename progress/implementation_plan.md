# Advanced Network Traffic Analyzer & Dashboard

This plan details the combination of **NetScope** (CLI packet sniffer) and **Network Traffic Monitor** (Streamlit dashboard) to create a single, comprehensive Computer Networks project. 

## Analysis of Existing Projects

1. **NetScope**: A powerful CLI packet sniffer utilizing `scapy`. It excels at deep packet inspection. It can detect specific application-layer protocols (HTTP, SSH, DNS, FTP, etc.) based on ports, extract DNS queries, parse HTTP requests, and importantly, detect ARP spoofing attacks. It exports a JSON summary.
2. **Network Traffic Monitor**: A visual project using `scapy`, `pandas`, `plotly`, and `streamlit`. It captures a fixed amount of packets (500), saves basic details (Protocol: TCP/UDP/ICMP, IPs, Ports, Size) to a CSV, and visualizes this data in an interactive web dashboard.

## Goal Description

By merging these two, we will get the "best of both worlds": the deep packet inspection and security features of NetScope, visualized beautifully on the interactive Streamlit dashboard of the Network Traffic Monitor. 

### Extra Features to Make it Better (Bonus Additions)
* **Real-time Live Capture**: Instead of freezing the UI to capture exactly 500 packets and then analyzing them, we can run the capture engine in a background thread. The dashboard will auto-refresh, providing a truly "live" monitoring experience.
* **Security & Threat Dashboard**: A dedicated tab/section in the dashboard for ARP Spoofing alerts and suspicious traffic.
* **Application Data View**: A section specifically showing intercepted DNS queries and HTTP requests in real-time tables.

## User Review Required

> [!IMPORTANT]
> Since we are combining two separate projects, I propose creating a **new directory** called `Advanced Network Analyzer` on your Desktop to hold the combined project cleanly, rather than overwriting the existing ones. Do you agree with this approach?

> [!TIP]
> I also propose changing the capture mechanism from a "click to capture 500 packets and wait" approach to a "Start/Stop Live Capture" toggle in the dashboard. Is this acceptable?

## Proposed Changes

We will create a new directory structure for the combined project.

### Core Capture Engine
We will extract the `NetScope` logic and adapt it to output both CSV (for standard traffic) and JSON (for security alerts/DNS logs) that the Streamlit app can continuously read.

#### [NEW] Advanced Network Analyzer/core/sniffer.py
- Will contain the `scapy` sniffing logic from `netscope.py`.
- Instead of just printing to the CLI, it will actively write packet stats, DNS queries, and ARP alerts to data files or a local SQLite database for the dashboard to read.

### Data Visualization (Dashboard)
We will heavily upgrade `app.py` from the Network Monitor to consume the enriched data.

#### [NEW] Advanced Network Analyzer/app.py
- Re-styled Streamlit dashboard with tabs: **Overview**, **Protocol Analysis**, **Application Logs** (DNS/HTTP), and **Security Alerts** (ARP Spoofing).
- Read from the new data sources outputted by `sniffer.py`.
- Interactive start/stop buttons for packet capture.

### Setup and Configuration
#### [NEW] Advanced Network Analyzer/requirements.txt
- Combined dependencies: `scapy`, `pandas`, `streamlit`, `plotly`, `colorama`.

## Verification Plan

### Manual Verification
1. Run `streamlit run app.py` in the new project folder.
2. Click "Start Capture" on the dashboard.
3. Browse the web (generate HTTP/DNS/TCP/UDP traffic).
4. Verify that the Streamlit charts update with rich protocol names (like HTTPS, DNS, rather than just TCP/UDP).
5. Verify that DNS queries are populated in the Application Logs tab.
