import streamlit as st # web development
import numpy as np # np mean, np random 
import pandas as pd # read csv, df manipulation
import time # to simulate a real time data, time loop 
import plotly.express as px # interactive charts 


# read csv from a github repo
# Make sure 'KDDTrain+.txt' is in the same directory or provide the full path
feature=["duration","protocol_type","service","flag","src_bytes","dst_bytes","land","wrong_fragment","urgent","hot",
          "num_failed_logins","logged_in","num_compromised","root_shell","su_attempted","num_root","num_file_creations","num_shells",
          "num_access_files","num_outbound_cmds","is_host_login","is_guest_login","count","srv_count","serror_rate","srv_serror_rate",
          "rerror_rate","srv_rerror_rate","same_srv_rate","diff_srv_rate","srv_diff_host_rate","dst_host_count","dst_host_srv_count", 
          "dst_host_same_srv_rate","dst_host_diff_srv_rate","dst_host_same_src_port_rate","dst_host_srv_diff_host_rate","dst_host_serror_rate",
          "dst_host_srv_serror_rate","dst_host_rerror_rate","dst_host_srv_rerror_rate","label","difficulty"]

try:
    df=pd.read_csv("KDDTrain+.txt",names=feature)
except FileNotFoundError:
    st.error("Error: 'KDDTrain+.txt' not found. Please ensure the file is in the same directory as the script.")
    st.stop() # Stop the script if the file isn't found

st.set_page_config(
    page_title = 'Real-Time Data Dashboard',
    page_icon = '✅',
    layout = 'wide'
)

# dashboard title
st.title("Real-Time / Live Data Dashboard")

# top-level filters 
# Ensure unique values for the selectbox
if not df.empty:
    Attack_filter = st.sidebar.selectbox("Attack", pd.unique(df['label']))
    # dataframe filter 
    filtered_df = df[df['label']==Attack_filter].copy() # Use .copy() to avoid SettingWithCopyWarning
else:
    st.warning("DataFrame is empty. Please check your data source.")
    st.stop()


# creating a single-element container for the entire dynamic content.
placeholder = st.empty()


# near real-time / live feed simulation 

for seconds in range(200):
    # It's crucial to operate on a copy if you're modifying the DataFrame within the loop
    # to avoid unexpected side effects if the original df is used elsewhere.
    # Also, ensure 'logged_in' and 'difficulty' columns exist in filtered_df
    if not filtered_df.empty:
        # Check if 'logged_in' and 'difficulty' are numeric before multiplication
        if pd.api.types.is_numeric_dtype(filtered_df['logged_in']) and pd.api.types.is_numeric_dtype(filtered_df['difficulty']):
            filtered_df.loc[:, 'Logged_in'] = filtered_df['logged_in'] * np.random.choice(range(1,5))
            filtered_df.loc[:, 'Difficulty'] = filtered_df['difficulty'] * np.random.choice(range(1,5))
        else:
            st.warning("Columns 'logged_in' or 'difficulty' are not numeric. Skipping random multiplication.")
            filtered_df.loc[:, 'Logged_in'] = filtered_df['logged_in'] # keep original if not numeric
            filtered_df.loc[:, 'Difficulty'] = filtered_df['difficulty'] # keep original if not numeric
    else:
        st.info("Filtered DataFrame is empty. No data to display or simulate.")
        time.sleep(1)
        continue # Skip the rest of the loop if df is empty

    # creating KPIs 
    # Ensure calculations handle potential empty data after filtering
    if not filtered_df.empty:
        avg_log = np.mean(filtered_df['Logged_in']) 
        count_label = int(filtered_df[filtered_df["label"]=='normal']['label'].count() + np.random.choice(range(1,30)))
        balance = np.mean(filtered_df['Difficulty'])
    else:
        avg_log = 0
        count_label = 0
        balance = 0

    with placeholder.container():
        # create three columns for KPIs
        kpi1, kpi2, kpi3 = st.columns(3)

        # fill in those three columns with respective metrics or KPIs 
        kpi1.metric(label="Logged__in", value=round(avg_log), delta= round(avg_log) - 10)
        kpi2.metric(label="Label count", value= int(count_label), delta= - 10 + count_label)
        kpi3.metric(label="Difficulty", value=round(balance), delta= round(balance) - 5)

        # create two columns for charts inside the container
        fig_col1, fig_col2 = st.columns(2)
        
        with fig_col1:
            st.markdown("### First Chart")
            # Ensure data is not empty before creating chart
            if not filtered_df.empty:
                fig = px.density_heatmap(data_frame=filtered_df, y = 'logged_in', x = 'label')
                st.plotly_chart(fig, use_container_width=True) # Use plotly_chart directly on the column
            else:
                st.info("No data for first chart.")

        with fig_col2:
            st.markdown("### Second Chart")
            if not filtered_df.empty:
                fig2 = px.histogram(data_frame = filtered_df, x = 'logged_in')
                st.plotly_chart(fig2, use_container_width=True) # Use plotly_chart directly on the column
            else:
                st.info("No data for second chart.")

        st.markdown("### Detailed Data View")
        if not filtered_df.empty:
            st.dataframe(filtered_df, use_container_width=True)
        else:
            st.info("No detailed data to display.")

    time.sleep(1)
