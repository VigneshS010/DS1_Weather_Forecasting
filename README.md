# 5-Day Weather Forecast Dashboard with AI Chatbot: A Comprehensive Overview

URL - https://vigneshs010-ds1-weather-forecasting-app-8m0ta9.streamlit.app/

## Overview

This project is a comprehensive weather forecasting dashboard designed for a hackathon, offering users a 5-day weather forecast, detailed hourly weather data, and an interactive AI chatbot to answer weather-related queries. It leverages machine learning models for predictions, real-time data fetching, and an intuitive Streamlit interface.

## Key Features

-   **5-Day Weather Forecast:** Provides detailed weather predictions for selected cities, including temperature, humidity, pressure, wind speed, and weather conditions (Sunny, Cloudy, Rainy).
-   **Hourly Weather Details:** Displays hourly weather data in an easy-to-read format, allowing users to understand weather changes throughout the day.
-   **Interactive AI Chatbot:** Integrates an AI chatbot powered by OpenRouter, enabling users to ask questions about the weather and receive context-aware responses.
-   **Real-Time Data Fetching:** Fetches weather data using latitude and longitude coordinates, ensuring accurate and up-to-date information.
-   **City and Date Selection:** Allows users to select a city and a specific day to view weather forecasts.
-   **Visualizations:** Presents weather data through interactive charts and graphs using Plotly, enhancing user understanding.
-   **News Integration:** Displays recent weather and climate news in the sidebar, keeping users informed about current events.
-   **Caching Mechanism:** Implements a caching system to minimize API calls and improve performance.
-   **Streamlit Interface:** Provides a user-friendly and responsive web interface using Streamlit.

## Project Structure

-   `app.py`: The main Streamlit application that handles the user interface, data fetching, and model predictions.
-   `chatbot.py`: Contains functions for interacting with the AI chatbot API and processing user queries.
-   `automate forecast.py`: Script to automate the forecast generation.
-   `utils.py`: Contains utility functions for fetching weather data.
-   `forecast_weather_features.csv`: Stores predicted weather features (temperature, humidity, pressure, wind speed).
-   `forecast_weather_condition.csv`: Stores predicted weather conditions (Sunny, Cloudy, Rainy).
-   `model_1_180_rain.h5`: Machine learning model for predicting weather conditions.
-   `model_1_180_rain.pkl`: Scaler for the weather condition prediction model.
-   `model_2_temp_hum_press.h5`: Machine learning model for predicting weather features.
-   `model_2_scaler.pkl`: Scaler for the weather feature prediction model.
-   `weather_cache.pkl`: Caches weather data to minimize redundant API calls.

## Technologies Used

-   **Streamlit:** For building the web application.
-   **Pandas:** For data manipulation and analysis.
-   **Plotly:** For creating interactive charts and graphs.
-   **TensorFlow/Keras:** For machine learning model implementation.
-   **Joblib:** For saving and loading machine learning models and scalers.
-   **Requests:** For making HTTP requests to fetch weather data.
-   **OpenRouter API:** For integrating the AI chatbot.
-   **NumPy:** For numerical computations.
-   **Datetime:** For handling date and time operations.
-   **Pytz:** for timezone conversions.

## Machine Learning Models

-   **Model 1 (Weather Conditions Prediction):** A deep learning model that predicts weather conditions (Sunny, Cloudy, Rainy) based on temperature, humidity, pressure, wind speed, and city.
-   **Model 2 (Weather Features Prediction):** A deep learning model that predicts temperature, humidity, pressure, and wind speed based on historical weather data and city.

## Setup and Installation

1.  **Clone the Repository:**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```
2.  **Create a Virtual Environment (Optional):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On macOS/Linux
    venv\Scripts\activate  # On Windows
    ```
3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Set up OpenRouter API Key:**
    -   Create a `secrets.toml` file in the `.streamlit` directory.
    -   Add your OpenRouter API key:
        ```toml
        OPENROUTER_API_KEY = "your_api_key_here"
        ```
5.  **Run the Streamlit Application:**
    ```bash
    streamlit run app.py
    ```

## Usage

1.  Open the Streamlit application in your web browser.
2.  Select a city from the dropdown menu.
3.  Select a date to view the weather forecast for that day.
4.  View the current weather information, hourly weather details, and weather feature charts.
5.  Click the "Chat with AI" button to interact with the chatbot.
6.  Explore the recent weather and climate news in the sidebar.

## Future Improvements

-   Implement a more robust caching mechanism with expiration policies.
-   Integrate more advanced weather data sources and APIs.
-   Enhance the AI chatbot with more sophisticated natural language processing capabilities.
-   Add user authentication and personalization features.
-   Deploy the application to a cloud platform for wider accessibility.
-   Add more cities and improve model accuracy.
-   Add more robust error checking, and improve the API responses.
-   Improve the UI/UX.

**Core Philosophy:** The project aims to bridge the gap between complex meteorological data and everyday user accessibility. By leveraging machine learning for accurate predictions and an intuitive AI chatbot, it simplifies weather interpretation, making it relevant and actionable for users.

**Data-Driven Predictions:** At the heart of this application are two machine learning models, trained on extensive weather datasets.

-   **Model 1: Weather Conditions Prediction:** This model classifies weather conditions (Sunny, Cloudy, Rainy) based on key atmospheric variables (temperature, humidity, pressure, wind speed) and city-specific data. It's crucial for providing a quick, understandable overview of the weather.
-   **Model 2: Weather Features Prediction:** This model delves deeper, predicting numerical weather features like temperature, humidity, pressure, and wind speed. These predictions are essential for detailed, hourly forecasts, allowing users to plan their activities with precision.

**Real-Time Data Integration:** The application's accuracy is bolstered by real-time weather data fetching. By utilizing latitude and longitude coordinates, it ensures that the forecasts are based on the latest available information. To reduce API calls and improve load times, a caching mechanism is implemented, storing frequently accessed data for a defined period.

**Interactive AI Chatbot:** The integration of an AI chatbot, powered by the OpenRouter API, transforms the application from a passive display to an interactive tool. Users can engage in natural language conversations, asking specific weather-related questions and receiving context-aware responses. This feature adds a layer of personalized interaction, making the application more engaging and user-friendly.

**User-Centric Interface:** The Streamlit framework is employed to create a seamless and responsive web interface. The dashboard is designed to be intuitive, with clear visualizations and easy-to-navigate features.

-   **City and Date Selection:** Users can easily switch between different cities and select specific dates to view forecasts.
-   **Hourly Weather Details:** Weather data is presented in a detailed, hourly format, allowing users to track changes throughout the day.
-   **Visualizations:** Interactive charts and graphs, created using Plotly, provide a visual representation of weather patterns, making it easier to understand trends and variations.
-   **News Integration:** A sidebar displays recent weather and climate news, keeping users informed about current events and their impact.

**Technical Architecture:**

-   **Backend:** Python is the primary language, with libraries like Pandas, NumPy, and TensorFlow/Keras handling data processing and machine learning tasks.
-   **Frontend:** Streamlit provides the web interface, while Plotly handles visualizations.
-   **API Integration:** The OpenRouter API is used for the AI chatbot functionality, and external APIs are used for weather data retrieval.
-   **Data Storage:** CSV files store forecast data, and a pickle file is used for caching.

## Contribution

Contributions to this project are welcome. Please feel free to submit pull requests or open issues to suggest improvements or report bugs.
