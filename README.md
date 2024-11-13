
# Activity Prediction Using KNN

This project aims to predict physical activities based on sensor data using a K-Nearest Neighbors (KNN) model. The sensor data consists of 3-axis accelerometer readings from wearable devices such as sensors placed on the thigh and back. These readings are used to predict various physical activities like walking, running, sitting, or standing.

The application is built using **Streamlit** for the web interface, allowing users to either upload data or manually input sensor values for real-time predictions. The model predicts the activity based on the input and displays an activity label along with a related GIF.

### Features:
- **Manual Data Entry**: Users can enter accelerometer data from 6 features (X, Y, Z axes for both back and thigh sensors) and receive an activity prediction.
- **File Upload**: Users can upload a CSV file with sensor data, and the system will predict the activities based on that data.
- **Prediction Output**: For each activity prediction, the app displays a label and a related GIF for better visualization.
  
---

## Setup and Usage

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/visionjain/HARTH-Activity-Detection
   cd HARTH-Activity-Detection
   ```

2. **Install Dependencies**:

   Install all required dependencies from `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit App**:

   After the dependencies are installed, you can start the app using:

   ```bash
   streamlit run app.py
   ```

4. **Using the App**:

   - **Manual Data Entry**: Enter values for the accelerometer data in the input fields for each of the 6 features. After entering the data, click the "Predict Activity" button to get the predicted activity and a related GIF.
   - **Upload CSV**: If you have a dataset in CSV format with sensor data, you can upload it to get predictions for each row.

---

## Data Format

For the file upload functionality, the CSV should contain the following columns:

- `feature_1`: Back sensor X-axis acceleration (g)
- `feature_2`: Back sensor Y-axis acceleration (g)
- `feature_3`: Back sensor Z-axis acceleration (g)
- `feature_4`: Thigh sensor X-axis acceleration (g)
- `feature_5`: Thigh sensor Y-axis acceleration (g)
- `feature_6`: Thigh sensor Z-axis acceleration (g)

---

## Model Description

The core of the prediction system is a K-Nearest Neighbors (KNN) model that is trained using data from a Human Activity Recognition (HAR) dataset. The model uses 6 features (3 for back sensor and 3 for thigh sensor) to predict the type of activity the user is performing.

The KNN model works by comparing the input feature vector with the stored labeled data and finding the most common activity in the nearest neighbors.

### Activity Labels:

- **1.0**: Walking
- **2.0**: Running
- **3.0**: Shuffling
- **4.0**: Stairs (ascending)
- **5.0**: Stairs (descending)
- **6.0**: Standing
- **7.0**: Sitting
- **8.0**: Lying
- **13.0**: Cycling (sit)
- **14.0**: Cycling (stand)
- **130.0**: Cycling (sit, inactive)
- **140.0**: Cycling (stand, inactive)

---

## License

This project is licensed under the MIT License.
