# SMART FARM - SERVER SIDE CONTROLLER

## Installation
#### Prerequisites
* Docker
* Firebase realtime database
* Clone this repo

#### Firebase setup
1. On root database url, insert dump data as below to create database schema
```javascript
{
    threshold: {
        humidity: <integer>,
        temperature: <integer>,
        light: <integer>,
    },
    log: {
        __randomkey__: {
            "event": "overbound",
            "feed": "<feed_id>"
            "value": "<integer>",
            "time": "YYYY-MM-DD hh:mm:ss",  // UTC time string
        }
        // ...
    }
}
```
2. Insert rules
```javascript
{
  "rules": {
    "log": {
      ".read": true,
      ".write": "auth.uid === 'my-service-worker'",
      "$log_id": {
        ".indexOn": ["time"],
          
			}
    },
    "threshold": {
      ".read": true,
      ".write": "auth.uid !== 'my-service-worker'"
		}
  }
}
```

3. Download certificate file for Admin SDK from firebase Project Setting page.
4. Go to root directory, config the settings.py
``` python
    DATABASE_URL = 'https://__databaseURL__.firebasedatabase.app/'
    DATABASE_CERTIFICATE_PATH = '__path_to_certification_file__'
```

#### Run
> Go to root directory ./server

    docker build -t smartfarm/server:v1 .
    docker compose up

## GUIDE
This is a server-side scripts for automatically update log data into cloud database as well as take controll over devices **Fan, Water Pump, Light Bulb** whenever auto-mode is turned ON.

### Update Data Log
Automatically append new log data onto cloud database whenever received overbound data. Log data will be in `log/`

* Event - `overbound` or `button`
* Feed - sensor feed_id
* value - Sensor value
* Time - UTC time string

The log data is as below
```javascript
{
    __randomkey__: {
        "event": "overbound",
        "feed": "<feed_id>"
        "value": "<integer>",
        "time": "YYYY-MM-DD hh:mm:ss", 
    }
}
```

### Control devices status
Autimatically publish `ON:1`  `OFF:0` to devices' feed id **`Only if auto-mode feed is set to 1`**.

* Publish `1  (ON)` to corresponding device's feed when received overbound data.
* Setimer to wait for at least 5 minutes to checking feed data again.
* Publish `0 (OFF)` ro corresponding device's feed if data not overbound and Timeout
