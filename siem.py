import streamlit as st # web development
import numpy as np # np mean, np random 
import pandas as pd # read csv, df manipulation
import time # to simulate a real time data, time loop 
import plotly.express as px # interactive charts 
import plotly.graph_objects as go # Needed if manually creating figures, but px is fine

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


# --- Layout Pre-allocation and Initial Chart Creation ---

# Create placeholders for KPIs
kpi1_ph, kpi2_ph, kpi3_ph = st.columns(3) 

# Create columns and placeholders for charts
chart_col1, chart_col2 = st.columns(2) 

with chart_col1:
    st.markdown("### First Chart")
    # Create an initial dummy figure or a figure with initial data
    # This figure object will be updated in the loop
    initial_fig1 = px.density_heatmap(data_frame=initial_filtered_df.head(1), y='logged_in', x='label', title="Loading...") # Use minimal data to start
    chart1_placeholder = st.plotly_chart(initial_fig1, use_container_width=True) 

with chart_col2:
    st.markdown("### Second Chart")
    # Create an initial dummy figure or a figure with initial data
    # This figure object will be updated in the loop
    initial_fig2 = px.histogram(data_frame=initial_filtered_df.head(1), x='logged_in', title="Loading...") # Use minimal data to start
    chart2_placeholder = st.plotly_chart(initial_fig2, use_container_width=True) 

# Placeholder for the top 10 data head
st.markdown("### Top 10 Data Head")
data_table_placeholder = st.empty()


# --- Near Real-Time / Live Feed Simulation ---

df_for_simulation = initial_filtered_df.copy()

for seconds in range(200):
    if df_for_simulation.empty:
        st.info("Filtered DataFrame is empty. No data to display or simulate.")
        time.sleep(1)
        continue

    # Simulate data changes (operate on the copy for simulation)
    # Ensure 'logged_in' and 'difficulty' are numeric before multiplication
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

    # --- Update Charts' Data ---
    # Generate new figures temporarily to extract updated traces and layout
    # This is a common pattern when you use px for convenience, then update go.Figure
    
    # Update Fig 1 (Density Heatmap)
    temp_fig1 = px.density_heatmap(data_frame=df_for_simulation, y='logged_in', x='label')
    initial_fig1.data = temp_fig1.data # Update data
    initial_fig1.layout = temp_fig1.layout # Update layout (important for axes, titles, etc.)

    # Update Fig 2 (Histogram)
    temp_fig2 = px.histogram(data_frame=df_for_simulation, x='logged_in')
    initial_fig2.data = temp_fig2.data # Update data
    initial_fig2.layout = temp_fig2.layout # Update layout

    # Re-render the existing Plotly chart objects
    chart1_placeholder.plotly_chart(initial_fig1, use_container_width=True)
    chart2_placeholder.plotly_chart(initial_fig2, use_container_width=True)

    # --- Update Top 10 Data Head ---
    if not df_for_simulation.empty:
        data_table_placeholder.dataframe(df_for_simulation.head(10), use_container_width=True)
    else:
        data_table_placeholder.info("No data to display.")
    
    time.sleep(1)
