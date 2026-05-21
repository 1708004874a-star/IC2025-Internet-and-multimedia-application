# Smart Campus IoT Monitoring System

An IoT project that monitors temperature, humidity, light, and sound across campus spaces. Sensor devices automatically collect and transmit data via MQTT. Data is stored and presented through a Django web dashboard with filtering, alerts, and real-time visualization.

## Project Structure

```
.
├── mysite/                     # Django web application
│   ├── manage.py               # Django management script
│   ├── db.sqlite3              # SQLite database (excluded from git)
│   ├── mysite/                 # Project configuration
│   │   ├── settings.py         # Django settings
│   │   ├── urls.py             # Root URL routing
│   │   └── wsgi.py             # WSGI entry point
│   ├── smart_campus/           # Core app: sensor data management
│   │   ├── models.py           # SensorData model
│   │   ├── views.py            # Data display with filtering & alerts
│   │   ├── mqtt_handler.py     # MQTT subscriber for sensor data
│   │   └── templates/          # HTML templates
│   ├── dashboard/              # Dashboard v1 (summary view)
│   ├── dashboardtwo/           # Dashboard v2 (interactive charts)
│   ├── iot/                    # IoT event data display
│   ├── blog/                   # Blog entries app
│   ├── inventory/              # Inventory management
│   └── timeevent/              # Time-based event tracking
├── firmware/                   # Arduino sensor firmware
│   ├── ESP8266/                # ESP8266 sensor node
│   │   ├── ESP8266.ino         # Main firmware
│   │   ├── LedMatrix.h         # LED matrix header
│   │   └── LedMatrix.cpp       # LED matrix implementation
│   └── M5StickC/               # M5StickC sensor node
│       └── M5StickC_Final.ino  # Main firmware
├── .gitignore
└── README.md
```

## Key Features

- **MQTT Integration**: Receives real-time sensor data via MQTT from IoT devices
- **Data Filtering**: Filter sensor readings by location, node ID, and date range
- **Alert System**: Automatic alerts for high/low temperature, high sound levels, and nighttime noise
- **Interactive Dashboard**: Chart.js-based visualization with parameter and location filtering
- **Data Export**: Flexmonster pivot tables for data analysis

## Setup

```bash
# Install dependencies
pip install django paho-mqtt

# Run migrations
cd mysite
python manage.py migrate

# Start the development server
python manage.py runserver

# Start MQTT data collection (in a separate terminal)
python manage.py shell -c "from smart_campus import mqtt_handler"
```

## Django Apps

| App | URL | Description |
|-----|-----|-------------|
| smart_campus | `/smart_campus/` | Main sensor data view with filtering and alerts |
| dashboard | `/dashboard/` | Dashboard v1 with summary statistics |
| dashboardtwo | `/dashboardtwo/` | Dashboard v2 with interactive charts |
| iot | `/iot/` | IoT event data listing |
| blog | `/blog/` | Blog entries |
| inventory | `/inventory/` | Inventory tracking |
| timeevent | `/timeevent/` | Time-based events |

## Hardware

Sensor nodes use ESP8266 and M5StickC microcontrollers. Firmware source code is in the `firmware/` directory. The devices connect to the MQTT broker at `ia.ic.polyu.edu.hk` and publish to topic `iot/sensor-A`.   
