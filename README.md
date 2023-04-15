# SMART FARMING
A smart farming system with the integration of IOT.

## Requirements
* PYTHON
* PIP
* VIRTUALENV

## Installations
1. Get Firebase credential json file for Admin SDK in Firebase console setting.

2. Clone the repo
``` git
git clone https://github.com/tonible14012002/SmartFarm
```
3. Install requirements

* ` cd ./server`
* `virtualenv env`
* `python -m pip install -r requirements.txt`

4. Configuration
* Create **settings.py** file inside /utils.
* add these line of code.
``` python 
AIO_USERNAME = '__yourAdafruitUsername__'
AIO_KEY = '__yourAdafruitKey__'
AIO_FEED_IDs = ['light', 'temperature', 'humidity']

# Firebase settings.
DATABASE_URL = 'https://smart-farm-f00f3-default-rtdb.asia-southeast1.firebasedatabase.app/'
DATABASE_SERVICE_UID = 'my-service-worker'
DATABASE_CERTIFICATE_PATH = '__directoryPathToYourCertificationFile__'

```