# Autonomous AI Mapping Drone 🚁

An intelligent, autonomous drone system designed to navigate and map environments where GPS is unavailable. This project was developed as a final year Master of Computer Applications (MCA) project, focusing on the intersection of artificial intelligence, custom hardware integration, and spatial computing. 

## ✨ Key Features

* **GPS-Denied Navigation:** Utilizes advanced sensor fusion and AI to maintain stable flight and positioning without relying on satellite signals.
* **Real-Time Environmental Mapping:** Processes sensor data on the fly to generate accurate maps of the drone's surroundings.
* **Autonomous Flight & AI:** Implements intelligent path planning to navigate complex environments autonomously.
* **Laptop Ground Control Station:** A custom-built interface allowing full system monitoring, telemetry visualization, and control directly from a laptop.
* **Custom Hardware Integrations:** Engineered using strategic hardware modifications and hacks to optimize processing power and sensor payload weight.

## 🛠️ Technology Stack

* **Languages:** Python, Java
* **Concepts & Frameworks:** Artificial Intelligence, Machine Learning, IoT Protocols, Design and Analysis of Algorithms (DAA)
* **Hardware & Communication:** Custom modified flight controllers, onboard companion computer, wireless telemetry




## 📂 Project Structure

```text
drone_ai_pilot/
│
├── models/                   # Stores AI weights and trained models
│   └── yolov8n.pt            # YOLOv8 object detection model weights
│
├── vision/                   # Computer vision and camera processing logic
│   └── eyes.py               # Handles visual input and object recognition
│
├── control/                  # Flight commands and drone communication
│   └── flight_bridge.py      # Bridges AI decisions to physical flight controls
│
├── map/                      # Real-time mapping output directory
│   └── [generated_maps].jpg  # Stores saved flight path JPEGs
│
├── utils/                    # Helper scripts and calculations
│   └── zone_math.py          # Mathematical utilities for spatial calculations
│
├── requirements.txt          # List of Python dependencies to install
└── main.py                   # Main execution script to launch the AI pilot system
