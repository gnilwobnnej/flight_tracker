# ✈️ Flight Tracker

A real-time flight tracking application built with Python and Streamlit. This tool provides a visual and interactive way to monitor aircraft positions and flight data across the globe.

### 🔗 Live Demo
Check out the live application here: **[trin-flight-tracker.streamlit.app](https://trin-flight-tracker.streamlit.app)**

## 📖 Overview
The **Flight Tracker** project leverages real-time aviation data to display aircraft movements on an interactive map. It is designed to be lightweight, fast, and easy to deploy, making it a great starting point for developers interested in geospatial data and API integrations.

## ✨ Features
* **Real-time Map Visualization:** View aircraft positions on a global or regional map.
* **Flight Search:** Filter or search for specific flights by flight number or callsign.
* **Live Metrics:** Access data points such as altitude, velocity, and heading.
* **Streamlit Powered:** A clean, responsive user interface that works in any modern web browser.

## 🛠️ Built With
* [Python](https://www.python.org/) - The core programming language.
* [Streamlit](https://streamlit.io/) - Used for creating the web interface.
* [Pandas](https://pandas.pydata.org/) - For data manipulation and processing.
* [OpenSky API](https://opensky-network.org/) - Providing the live flight state vectors.

flight_tracker/
├── app.py              # Main Streamlit application file
├── requirements.txt    # List of Python dependencies
├── data/               # (Optional) Static datasets or geo-json files
└── README.md           # Project documentation
