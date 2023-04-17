# SMART FARMING
A smart farming system with the integration of IOT.

## Requirements
* PYTHON
* PIP
* VIRTUALENV

## Installations
### Firebase setup
1. Go to your firebase console, create new Project.
2. Create realtime database instance.
3. Insert data as below
``` javascript 
yourDatabaseURL: {
    himidity: {
        current: {
            created_at: "YYYY-MM-DD hh:mm:ss", // replace the date time you want
            value: "50"
        },
        pass: {} // data will be inserted later
    },
    light: {}, //Similar to himidity.
    temperature: {}, // Similar to humidity

    users: {    // storing user's tokens for cloud message
        // username: "token" 
    }
    log: { // Storing log data
        // eventName: { // ex: bound
        //     subEventName: "humidity"
        //     detail: "___"
        // } 
    }
}
```
4. Go to Edit Rules tab, insert lines
``` javascript
{
  "rules": {
    ".read": true,
		"$sensor_data": {
      ".read": true,
      ".write": "auth.uid === 'my-service-worker'",
        "pass": {
            ".indexOn": ["created_at"]
        }
    }
  }
}

```
5. Go to Project Settings, in the Service account tab, hit on Button **Generate new private key** to download certificate file.


### Setup directory

``` git
git clone https://github.com/tonible14012002/SmartFarm
```
1. Install requirements

* ` cd ./server`
* `virtualenv env`
* `.\env\scripts\activate`
* `python -m pip install -r requirements.txt`

2. Configuration
* Create **settings.py** file inside /utils.
* add these lines of code.
``` python 
AIO_USERNAME = '__yourAdafruitUsername__'
AIO_KEY = '__yourAdafruitKey__'
AIO_FEED_IDs = ['light', 'temperature', 'humidity']

# Firebase settings.
DATABASE_URL = 'https://smart-farm-f00f3-default-rtdb.asia-southeast1.firebasedatabase.app/'
DATABASE_SERVICE_UID = 'my-service-worker'
DATABASE_CERTIFICATE_PATH = '__directoryPathToYourCertificationFile__'

```