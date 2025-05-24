import streamlit as st # web development
import numpy as np # np mean, np random 
import pandas as pd # read csv, df manipulation
import time # to simulate a real time data, time loop 
import plotly.express as px # interactive charts 

# --- Data Loading (outside the loop, as it's static) ---
feature=["duration","protocol_type","service","flag","src_bytes","dst_bytes","land","wrong_fragment","urgent","hot",
          "num_failed_logins","logged_in","num_compromised","root_shell","su_attempted","num_root","num_file_creations","num_shells",
          "num_access_files","num_outbound_cmds","is_host_login","is_guest_login","count","srv_count","serror_rate","srv_serror_rate",
          "rerror_rate","srv_rerror_rate","same_srv_rate","diff_srv_rate","srv_diff_host_rate","dst_host_count","dst_host_srv_count", 
          "dst_host_same_srv_rate","dst_host_diff_srv_rate","dst_host_same_src_port_rate","dst_host_srv_diff_host_rate","dst_host_serror_rate",
          "dst_host_srv_serror_rate","dst_host_rerror_rate","dst_host_srv_rerror_rate","label","difficulty"]

try:
    df_original = pd.read_csv("KDDTrain+.txt",names=feature) # Load once
except FileNotFoundError:
    st.error("Error: 'KDDTrain+.txt' not found. Please ensure the file is in the same directory as the script.")
    st.stop()

# --- Streamlit Page Configuration ---
st.set_page_config(
    page_title = 'Real-Time Data Dashboard',
    page_icon = '✅',
    layout = 'wide'
)

# --- Dashboard Title ---
st.title("Real-Time / Live Data Dashboard")

# --- Top-level Filters ---
if not df_original.empty:
    Attack_filter = st.sidebar.selectbox("Attack", pd.unique(df_original['label']))
    # Filter once based on the selectbox choice
    initial_filtered_df = df_original[df_original['label']==Attack_filter].copy()
else:
    st.warning("Original DataFrame is empty. Cannot apply filter.")
    st.stop()


# --- Layout Pre-allocation (Crucial for avoiding duplicate IDs) ---

# Create placeholders for KPIs
kpi1_ph, kpi2_ph, kpi3_ph = st.columns(3) # These column objects are created once

# Create placeholders for charts
chart_col1, chart_col2 = st.columns(2) # These column objects are created once

with chart_col1:
    st.markdown("### First Chart")
    chart1_placeholder = st.empty() # Placeholder for the first chart within its column

with chart_col2:
    st.markdown("### Second Chart")
    chart2_placeholder = st.empty() # Placeholder for the second chart within its column

st.markdown("### Detailed Data View")
data_table_placeholder = st.empty() # Placeholder for the dataframe


# --- Near Real-Time / Live Feed Simulation ---

# Use the initial filtered_df to start the simulation
df_for_simulation = initial_filtered_df.copy()

for seconds in range(200):
    if df_for_simulation.empty:
        st.info("Filtered DataFrame is empty. No data to display or simulate.")
        time.sleep(1)
        continue

    # Simulate data changes (operate on the copy for simulation)
    if pd.api.types.is_numeric_dtype(df_for_simulation['logged_in']) and \
       pd.api.types.is_numeric_dtype(df_for_simulation['difficulty']):
        df_for_simulation.loc[:, 'Logged_in'] = df_for_simulation['logged_in'] * np.random.choice(range(1,5))
        df_for_simulation.loc[:, 'Difficulty'] = df_for_simulation['difficulty'] * np.random.choice(range(1,5))
    else:
        st.warning("Columns 'logged_in' or 'difficulty' are not numeric. Skipping random multiplication.")
        df_for_simulation.loc[:, 'Logged_in'] = df_for_simulation['logged_in']
        df_for_simulation.loc[:, 'Difficulty'] = df_for_simulation['difficulty']

    # --- Update KPIs ---
    avg_log = np.mean(df_for_simulation['Logged_in']) 
    count_label = int(df_for_simulation[df_for_simulation["label"]=='normal']['label'].count() + np.random.choice(range(1,30)))
    balance = np.mean(df_for_simulation['Difficulty'])

    kpi1_ph.metric(label="Logged__in", value=round(avg_log), delta= round(avg_log) - 10)
    kpi2_ph.metric(label="Label count", value= int(count_label), delta= - 10 + count_label)
    kpi3_ph.metric(label="Difficulty", value=round(balance), delta= round(balance) - 5)

    # --- Update Charts ---
    # Generate new figures with updated data
    fig = px.density_heatmap(data_frame=df_for_simulation, y = 'logged_in', x = 'label')
    fig2 = px.histogram(data_frame = df_for_simulation, x = 'logged_in')
    
    # Update the charts using their respective placeholders
    chart1_placeholder.plotly_chart(fig, use_container_width=True)
    chart2_placeholder.plotly_chart(fig2, use_container_width=True)

    # --- Update Detailed Data View ---
    data_table_placeholder.dataframe(df_for_simulation, use_container_width=True)
    
    time.sleep(1)
