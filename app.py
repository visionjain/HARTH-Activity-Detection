import streamlit as st
import joblib
import numpy as np
import pandas as pd
import time



hide_streamlit_style = """
<style>
    footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
# Load the pre-trained KNN model
model_filename = '/mount/src/harth-activity-detection/knn_harth_model.joblib'
knn_model = joblib.load(model_filename)

# Map activity codes to activity names as per HARTH dataset
activity_mapping = {
    1.0: "Walking",
    2.0: "Running",
    3.0: "Shuffling",
    4.0: "Stairs (ascending)",
    5.0: "Stairs (descending)",
    6.0: "Standing",
    7.0: "Sitting",
    8.0: "Lying",
    13.0: "Cycling (sit)",
    14.0: "Cycling (stand)",
    130.0: "Cycling (sit, inactive)",
    140.0: "Cycling (stand, inactive)"
}

# GIF links for each activity (replace with your own GIF links)
gif_links = {
    "Walking": "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNzd5c2Q1c3NqaDBvaXFjNXkxMGp5NHp5YjQ2bHBkMzQzY3JpODZsaiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/NA9Mqor2nRiLI7dY5t/giphy.webp",
    "Running": "https://www.clipartbest.com/cliparts/4c9/ogd/4c9ogdBgi.gif",
    "Shuffling": "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExdm9yY3o0MjNsenV5bGM2dTRqaDNwZ2RiMDl3d3gyZnpiMDI2cnR6eiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/IliT50DlHgLhAAW72R/giphy.webp",
    "Stairs (ascending)": "https://i.pinimg.com/originals/cf/ee/0d/cfee0d4359dafc18d61191ffcd13eb35.gif",
    "Stairs (descending)": "https://i.pinimg.com/originals/03/ef/71/03ef7162172ebc4d9d0fb6d8f5fce73c.gif",
    "Standing": "https://i.pinimg.com/originals/fb/69/b0/fb69b0b94fd3e40bf041be3db4b8b5e9.gif",
    "Sitting": "https://media3.giphy.com/avatars/luciewallart/V0NcIyixVeqY.gif",
    "Lying": "https://media.tenor.com/4bsdqD25bD8AAAAj/netflix-tired.gif",
    "Cycling (sit)": "https://media.tenor.com/cf1Z2f13iEwAAAAj/transparent-bike.gif",
    "Cycling (stand)": "https://media.tenor.com/cf1Z2f13iEwAAAAj/transparent-bike.gif",
    "Cycling (sit, inactive)": "https://media.tenor.com/cf1Z2f13iEwAAAAj/transparent-bike.gif",
    "Cycling (stand, inactive)": "https://media.tenor.com/cf1Z2f13iEwAAAAj/transparent-bike.gif"
}

# Set up Streamlit app title and description
st.title("HARTH Activity Detection App")

# Sidebar for mode selection
mode = st.sidebar.selectbox("Select Mode", ["Manual Data Entry", "Live Data Mode"])

if mode == "Manual Data Entry":
    # Create a 3x2 grid of input fields for manual data entry
    col1, col2, col3 = st.columns(3)

    with col1:
        feature_1 = st.number_input("Back sensor X (g) - Acceleration in down direction", 
                                    min_value=-10.0, max_value=10.0, step=0.01, 
                                    value=-1.028626, format="%.10f")

    with col2:
        feature_2 = st.number_input("Back sensor Y (g) - Acceleration in left direction", 
                                    min_value=-10.0, max_value=10.0, step=0.01, 
                                    value=-0.105919, format="%.10f")

    with col3:
        feature_3 = st.number_input("Back sensor Z (g) - Acceleration in forward direction", 
                                    min_value=-10.0, max_value=10.0, step=0.01, 
                                    value=-0.264525, format="%.10f")

    # Second row of inputs
    col4, col5, col6 = st.columns(3)

    with col4:
        feature_4 = st.number_input("Thigh sensor X (g) - Acceleration in down direction", 
                                    min_value=-10.0, max_value=10.0, step=0.01, 
                                    value=-1.235359, format="%.10f")

    with col5:
        feature_5 = st.number_input("Thigh sensor Y (g) - Acceleration in right direction", 
                                    min_value=-10.0, max_value=10.0, step=0.01, 
                                    value=-0.162986, format="%.10f")

    with col6:
        feature_6 = st.number_input("Thigh sensor Z (g) - Acceleration in backward direction", 
                                    min_value=-10.0, max_value=10.0, step=0.01, 
                                    value=-0.483125, format="%.10f")

    # Predict activity based on inputs
    if st.button("Predict Activity"):
        # Prepare feature array for prediction
        input_features = np.array([[feature_1, feature_2, feature_3, feature_4, feature_5, feature_6]])

        # Predict the activity code
        predicted_activity_code = knn_model.predict(input_features)[0]
        predicted_activity_name = activity_mapping.get(predicted_activity_code, "Unknown Activity")

        # Display prediction
        st.write(f"Predicted Activity: {predicted_activity_code} - {predicted_activity_name}")

        # Get the GIF link based on the predicted activity
        gif_url = gif_links.get(predicted_activity_name, "https://your-default-gif-link.com")

        # Display the GIF
        st.image(gif_url, caption=f"{predicted_activity_name}", width=120)


elif mode == "Live Data Mode":
    # File uploader for CSV file
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    
    if uploaded_file is not None:
        # Read the CSV file
        live_data = pd.read_csv(uploaded_file)

        # Display a progress bar
        progress_bar = st.progress(0)

        # Create placeholders for dynamic updates
        row_placeholder = st.empty()
        activity_placeholder = st.empty()

        # Start the prediction process for each row in the CSV
        for i, row in live_data.iterrows():
            # Extract the feature values from the row
            feature_1, feature_2, feature_3 = row['Back_X'], row['Back_Y'], row['Back_Z']
            feature_4, feature_5, feature_6 = row['Thigh_X'], row['Thigh_Y'], row['Thigh_Z']

            # Prepare feature array for prediction
            input_features = np.array([[feature_1, feature_2, feature_3, feature_4, feature_5, feature_6]])

            # Predict the activity code
            predicted_activity_code = knn_model.predict(input_features)[0]
            predicted_activity_name = activity_mapping.get(predicted_activity_code, "Unknown Activity")

            # Create a DataFrame with Feature names in the first row and corresponding values in the second row
            row_data = pd.DataFrame({
                "Feature": ["Back_X", "Back_Y", "Back_Z", "Thigh_X", "Thigh_Y", "Thigh_Z"],
                "Value": [feature_1, feature_2, feature_3, feature_4, feature_5, feature_6]
            }).transpose()

            # Display the row data with features and values as rows, not columns
            row_placeholder.table(row_data)  # This will display in the transposed format
            activity_placeholder.text(f"Predicted Activity: {predicted_activity_name} ({predicted_activity_code})")
            # Get the GIF link based on the predicted activity
            gif_url = gif_links.get(predicted_activity_name, "https://your-default-gif-link.com")
            
            # Display the GIF
            activity_placeholder.image(gif_url, caption=f"{predicted_activity_name}", width=120)

            # Update the progress bar
            progress_bar.progress((i + 1) / len(live_data))

            # Wait for 1 second before processing the next row
            time.sleep(3)
        
        st.write("Live data processing complete.")
