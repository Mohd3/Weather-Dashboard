import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
import random

# Load the dataset (replaced with actual live robot data in production)
data_path = "GlobalWeatherRepository.csv"
df = pd.read_csv(data_path)

robot_types = ["Ocean", "Mountains", "Desert"]
df["robot_source"] = [random.choice(robot_types) for _ in range(len(df))]

df = df[["robot_source", "temperature_celsius", "humidity", "wind_kph", "pressure_mb", "uv_index", 
         "air_quality_Carbon_Monoxide", "air_quality_Ozone", "air_quality_PM2.5", "wind_direction"]]

def main():
    st.title("AI-Powered Climate Monitoring Dashboard")
    st.markdown("Real-time climate data collected by AI-powered robots.")
    
    # Sidebar for robot selection
    st.sidebar.header("Filter Data")
    robot_filter = st.sidebar.selectbox("Select Robot Source", ["All"] + robot_types)
    
    filtered_df = df if robot_filter == "All" else df[df["robot_source"] == robot_filter]
    
    if not filtered_df.empty:
        random_record = filtered_df.sample(n=1).iloc[0]
    else:
        random_record = {col: 'N/A' for col in df.columns}
    
    # Key Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Temperature (°C)", f"{random_record['temperature_celsius']}")
    col2.metric("Humidity (%)", f"{random_record['humidity']}")
    col3.metric("Wind Speed (kph)", f"{random_record['wind_kph']}")
    
    st.subheader("Air Quality Metrics")
    aq_cols = ["air_quality_Carbon_Monoxide", "air_quality_Ozone", "air_quality_PM2.5"]
    st.bar_chart(filtered_df[aq_cols].mean())

    
    # 3D Scatter Plot
    st.subheader("3D Scatter Plot of Weather Data")
    scatter_fig = go.Figure(data=[
        go.Scatter3d(
            x=filtered_df["temperature_celsius"],
            y=filtered_df["humidity"],
            z=filtered_df["wind_kph"],
            mode='markers',
            marker=dict(size=5, color=filtered_df["temperature_celsius"], colorscale='Viridis', opacity=0.8)
        )
    ])
    scatter_fig.update_layout(
        scene=dict(
            xaxis_title='Temperature (°C)',
            yaxis_title='Humidity (%)',
            zaxis_title='Wind Speed (MPH)'
        ),
        title="3D Scatter Plot of Weather Data"
    )
    st.plotly_chart(scatter_fig)
    
    # Countplot for Wind Direction
    st.subheader("Wind Direction Distribution")
    fig, ax = plt.subplots()
    sns.countplot(x=filtered_df["wind_direction"], ax=ax, palette="viridis")
    ax.set_xlabel("Wind Direction")
    ax.set_ylabel("Count")
    ax.set_title("Count of Wind Directions")
    st.pyplot(fig)

if __name__ == "__main__":
    main()
