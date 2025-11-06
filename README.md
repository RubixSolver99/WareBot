# WareBot
## 🤖 SCUTTLE Autonomous Warehouse Robot
By: Thomas Kim, Tharun Nayar, Carson Perkins, Kevin Garcia Varon

An autonomous mobile robot designed to navigate a warehouse environment with obstacle avoidance, task monitoring, and manual control through a **Node-RED dashboard interface**.  
Built using the **SCUTTLE robotics platform** and powered by a **Raspberry Pi running RPiOS**, this project combines **computer vision (OpenCV)**, **LiDAR sensing**, and **local file I/O communication** to enable flexible, modular control.

---

## 📸 Project Overview

<div align="center">
  <img src="docs/images/system_overview.png" width="700">
  <br>
  <em>System-level overview of the SCUTTLE warehouse robot</em>
</div>

The robot autonomously navigates a mapped indoor area using LiDAR and ultrasonic sensing for obstacle avoidance, while visual data from a front-mounted camera supports lane and object detection.  
A Node-RED dashboard allows operators to view robot telemetry, task progress, and send simple control commands.

---

## 🧠 Core Objectives

- Develop a **functional autonomous navigation system** for a warehouse-like environment.
- Implement **real-time obstacle avoidance** using LiDAR and ultrasonic sensors.
- Create a **Node-RED dashboard** for control, logging, and monitoring.
- Use **Python** for onboard logic, computer vision (OpenCV), and data exchange through **local file I/O** (no MQTT dependency).
- Integrate an intuitive UI for demonstration and educational purposes.

---

## 🧩 System Architecture

<div align="center">
  <img src="docs/images/software_architecture.png" width="700">
  <br>
  <em>Software and communication architecture for SCUTTLE warehouse robot</em>
</div>

| Layer | Description |
|-------|--------------|
| **Hardware** | SCUTTLE base, Raspberry Pi 4/5, LiDAR sensor, Ultrasonic array, USB camera, motor controllers |
| **Firmware** | Motor drivers and low-level motion control |
| **Software Stack** | Python-based control and sensing nodes, OpenCV for vision processing, Node-RED dashboard UI |
| **Communication** | Local file I/O (JSON and CSV data exchange between Node-RED and Python) |
| **User Interface** | Web-accessible dashboard hosted by Node-RED for monitoring and control |

---

## 🧭 Navigation & Obstacle Avoidance

- **LiDAR sensor** continuously maps nearby objects within a predefined radius.  
- **Ultrasonic sensors** act as redundancy for close-range detection.  
- **OpenCV** processes camera input for path following, colored marker detection, or boundary recognition.  
- **Autonomous logic** in Python integrates these data streams to make directional decisions and speed adjustments in real-time.

---

## 🖥️ Node-RED Dashboard Design

<div align="center">
  <img src="docs/images/dashboard_mockup.png" width="700">
  <br>
  <em>Concept mockup of Node-RED dashboard interface</em>
</div>

The dashboard allows for:
- **Manual control** (forward, reverse, turn)  
- **Live telemetry** (speed, battery, distance sensors, CPU temperature)  
- **Log viewing** (mission progress, error logs)  
- **Mode switching** between *Autonomous* and *Manual*  

Data from Python scripts is stored as JSON/CSV in `/home/pi/scuttle_data/`, which Node-RED reads periodically to update the dashboard in real-time.

---

## 🧰 Technologies Used

| Category | Tools / Libraries |
|-----------|------------------|
| **Core Hardware** | SCUTTLE Robot, Raspberry Pi 4/5 |
| **Programming** | Python 3, Node-RED |
| **Computer Vision** | OpenCV |
| **Sensing** | LiDAR (RPLidar A1/A2), HC-SR04 Ultrasonic Sensors |
| **Data Handling** | Local File I/O (JSON, CSV) |
| **Operating System** | Raspberry Pi OS (Debian-based) |
| **Networking** | Configured via `wpa_supplicant.conf` for Wi-Fi connectivity and remote access |

---

## ⚙️ Setup & Installation

### 🧩 1. Clone the Repository
```bash
git clone https://github.com/yourusername/scuttle-warehouse-robot.git
cd scuttle-warehouse-robot
