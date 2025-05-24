import streamlit as st
import numpy as np
import pandas as pd
import time
import plotly.express as px

# ... (your existing code for reading data and setting page config) ...

feature=["duration","protocol_type","service","flag","src_bytes","dst_bytes","land","wrong_fragment","urgent","hot",
           "num_failed_logins","logged_in","num_compromised","root_shell","su_attempted","num_root","num_file_creations","num_shells",
           "num_access_files","num_outbound_cmds","is_host_login","is_guest_login","count","srv_count","serror_rate","srv_serror_rate",
           "rerror_rate","srv_rerror_rate","same_srv_rate","diff_srv_rate","srv_diff_host_rate","dst_host_count","dst_host_srv_count", 
           "dst_host_same_srv_rate","dst_host_diff_srv_rate","dst_host_same_src_port_rate","dst_host_srv_diff_host_rate","dst_host_serror_rate",
           "dst_host_srv_serror_rate","dst_host_rerror_rate","dst_host_srv_rerror_rate","label","difficulty"]

df=pd.read_csv("KDDTrain+.txt",names=feature)

st.set_page_config(
    page_title = 'Real-Time Data Dashboard',
    page_icon = '✅',
    layout = 'wide'
)

# dashboard title
st.title("Real-Time / Live Data Dashboard")

# top-level filters 
Attack_filter = st.sidebar.selectbox("Attack", pd.unique(df['label']))

# creating a single-element container.
placeholder = st.empty()

# dataframe filter 
df = df[df['label']==Attack_filter]

# Initialize chart placeholders outside the loop
# Create columns for charts
fig_col1, fig_col2 = st.columns(2)

with fig_col1:
    st.markdown("### First Chart")
    chart1_placeholder = st.empty() # Placeholder for the first chart

with fig_col2:
    st.markdown("### Second Chart")
    chart2_placeholder = st.empty() # Placeholder for the second chart

# Placeholder for the detailed data view
data_table_placeholder = st.empty()

# near real-time / live feed simulation 
for seconds in range(200):
    df['Logged_in'] = df['logged_in'] * np.random.choice(range(1,5))
    df['Difficulty'] = df['difficulty'] * np.random.choice(range(1,5))

    # creating KPIs 
    avg_log = np.mean(df['Logged_in']) 
    count_label = int(df[(df["label"]=='normal')]['label'].count() + np.random.choice(range(1,30)))
    balance = np.mean(df['Difficulty']) # This KPI wasn't displayed, but included for completeness

    with placeholder.container():
        # create three columns for KPIs
        kpi1, kpi2, kpi3 = st.columns(3)

        # fill in those three columns with respective metrics or KPIs 
        kpi1.metric(label="Logged__in", value=round(avg_log), delta= round(avg_log) - 10)
        kpi2.metric(label="Label count", value= int(count_label), delta= - 10 + count_label)
        kpi3.metric(label="Difficulty", value=round(balance), delta= round(balance) - 5) # Adding a metric for balance

        # Generate new figures with updated data
        fig = px.density_heatmap(data_frame=df, y = 'logged_in', x = 'label')
        fig2 = px.histogram(data_frame = df, x = 'logged_in')
        
        # Update the charts using their respective placeholders
        chart1_placeholder.plotly_chart(fig, use_container_width=True)
        chart2_placeholder.plotly_chart(fig2, use_container_width=True)

        st.markdown("### Detailed Data View")
        data_table_placeholder.dataframe(df, use_container_width=True)
    
    time.sleep(1)
