import streamlit as st # web development
import numpy as np # np mean, np random 
import pandas as pd # read csv, df manipulation
import time # to simulate a real time data, time loop 
import plotly.express as px # interactive charts 


# read csv from a github repo


feature=["duration","protocol_type","service","flag","src_bytes","dst_bytes","land","wrong_fragment","urgent","hot",
          "num_failed_logins","logged_in","num_compromised","root_shell","su_attempted","num_root","num_file_creations","num_shells",
          "num_access_files","num_outbound_cmds","is_host_login","is_guest_login","count","srv_count","serror_rate","srv_serror_rate",
          "rerror_rate","srv_rerror_rate","same_srv_rate","diff_srv_rate","srv_diff_host_rate","dst_host_count","dst_host_srv_count", 
          "dst_host_same_srv_rate","dst_host_diff_srv_rate","dst_host_same_src_port_rate","dst_host_srv_diff_host_rate","dst_host_serror_rate",
          "dst_host_srv_serror_rate","dst_host_rerror_rate","dst_host_srv_rerror_rate","label","difficulty"]

df=pd.read_csv("KDDTrain+.txt",names=feature)



st.set_page_config(
    page_title = 'Real-Time Data  Dashboard',
    page_icon = '✅',
    layout = 'wide'
)

# dashboard title

st.title("Real-Time / Live Data  Dashboard")

# top-level filters 

Attack_filter = st.sidebar.selectbox("Attack", pd.unique(df['label']))


# creating a single-element container.
placeholder = st.empty()


# dataframe filter 

df = df[df['label']==Attack_filter]

# near real-time / live feed simulation 

for seconds in range(200):
#while True: 
    
    df['Logged_in'] = df['logged_in'] * np.random.choice(range(1,5))
    df['Difficulty'] = df['difficulty'] * np.random.choice(range(1,5))

    # creating KPIs 
    avg_log = np.mean(df['Logged_in']) 

    count_label = int(df[(df["label"]=='normal')]['label'].count() + np.random.choice(range(1,30)))
    
    balance = np.mean(df['Difficulty'])

    with placeholder.container():
        # create three columns
        kpi1, kpi2, kpi3 = st.columns(3)

        # fill in those three columns with respective metrics or KPIs 
        kpi1.metric(label="Logged__in", value=round(avg_log), delta= round(avg_log) - 10)
        kpi2.metric(label="Label count", value= int(count_label), delta= - 10 + count_label)


        # create two columns for charts 

        fig_col1, fig_col2 = st.columns(2)
        with fig_col1:
            st.markdown("### First Chart")
            fig = px.density_heatmap(data_frame=df, y = 'logged_in', x = 'label')
            st.write(fig)
        with fig_col2:
            st.markdown("### Second Chart")
            fig2 = px.histogram(data_frame = df, x = 'logged_in')
            st.write(fig2)
        st.markdown("### Detailed Data View")
        st.dataframe(df)
        time.sleep(1)
    #placeholder.empty()
