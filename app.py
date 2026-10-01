import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os
import time
import subprocess
import sys

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="Advanced Network Analyzer",
    page_icon="🌐",
    layout="wide"
)

# Initialize session state for the capture process
if 'capture_process' not in st.session_state:
    st.session_state.capture_process = None

def get_status():
    try:
        if os.path.exists("data/status.json"):
            with open("data/status.json", "r") as f:
                return json.load(f)
    except:
        pass
    return {"running": False, "count": 0}

status = get_status()

# ============================================================
# LOAD NETWORK DATA
# ============================================================
@st.cache_data(ttl=2) # short TTL for live update feel
def load_data():
    try:
        with open("data/traffic_data.json", "r") as f:
            data = json.load(f)
            return data
    except:
        return {"packets": [], "protocols": {}, "dns_queries": [], "arp_alerts": []}

data = load_data()
df_packets = pd.DataFrame(data["packets"])

# ============================================================
# SIDEBAR
# ============================================================
st.sidebar.title("🌐 Advanced Network Analyzer")

if status["running"]:
    st.sidebar.success(f"🟢 Capture Running (Packets: {status.get('count', 0)})")
    if st.sidebar.button("Stop Capture", type="primary"):
        # Stop process
        if st.session_state.capture_process:
            st.session_state.capture_process.terminate()
            st.session_state.capture_process = None
        # Also clean up status
        try:
            with open("data/status.json", "w") as f:
                json.dump({"running": False, "count": status.get("count", 0)}, f)
        except: pass
        time.sleep(1)
        st.rerun()
else:
    st.sidebar.warning("🔴 Capture Stopped")
    if st.sidebar.button("Start Live Capture", type="primary"):
        # Launch background process
        process = subprocess.Popen([sys.executable, "core/sniffer.py"])
        st.session_state.capture_process = process
        time.sleep(2) # wait for startup
        st.rerun()

st.sidebar.markdown("---")
if not df_packets.empty:
    st.sidebar.header("🔎 Filters")
    protocols = sorted(df_packets["protocol"].dropna().unique())
    selected_protocols = st.sidebar.multiselect("Select Protocols", protocols, default=protocols)
    df_filtered = df_packets[df_packets["protocol"].isin(selected_protocols)].copy()
else:
    df_filtered = df_packets

# ============================================================
# MAIN DASHBOARD
# ============================================================
st.title("Network Traffic Dashboard")

tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Protocol Analysis", "Application Logs", "Security Alerts"])

if df_filtered.empty:
    st.info("No packets to display. Click 'Start Live Capture' from the sidebar to begin.")
else:
    with tab1:
        st.subheader("Network Overview")
        col1, col2, col3, col4 = st.columns(4)
        total_packets = len(df_filtered)
        total_bytes = df_filtered["length"].sum() if "length" in df_filtered else 0
        avg_size = df_filtered["length"].mean() if "length" in df_filtered and total_packets > 0 else 0
        
        unique_ips = len(set(df_filtered["src_ip"].dropna()) | set(df_filtered["dst_ip"].dropna()))

        col1.metric("📦 Total Packets", f"{total_packets:,}")
        col2.metric("💾 Total Traffic", f"{total_bytes:,} B")
        col3.metric("📏 Avg Packet Size", f"{avg_size:.2f} B")
        col4.metric("🌐 Unique IPs", f"{unique_ips:,}")
        
        st.divider()
        st.subheader("Recent Packets")
        # Show latest packets first
        st.dataframe(df_filtered.iloc[::-1].head(100), use_container_width=True)

    with tab2:
        st.subheader("Protocol Distribution")
        if data["protocols"]:
            prot_df = pd.DataFrame(list(data["protocols"].items()), columns=["Protocol", "Count"])
            fig = px.pie(prot_df, names="Protocol", values="Count", hole=0.5, title="Protocol Distribution")
            st.plotly_chart(fig, use_container_width=True)

            fig2 = px.bar(prot_df, x="Protocol", y="Count", text="Count", title="Packets by Protocol")
            st.plotly_chart(fig2, use_container_width=True)
            
    with tab3:
        st.subheader("DNS Queries")
        if data["dns_queries"]:
            dns_df = pd.DataFrame(data["dns_queries"])
            st.dataframe(dns_df.iloc[::-1], use_container_width=True)
        else:
            st.info("No DNS queries intercepted yet.")

    with tab4:
        st.subheader("Security Alerts (ARP Spoofing)")
        if data["arp_alerts"]:
            st.error(f"Detected {len(data['arp_alerts'])} ARP spoofing attempts!")
            arp_df = pd.DataFrame(data["arp_alerts"])
            st.dataframe(arp_df.iloc[::-1], use_container_width=True)
        else:
            st.success("No ARP spoofing detected. Network appears safe.")

# Auto refresh logic if running
if status["running"]:
    time.sleep(3)
    st.rerun()
