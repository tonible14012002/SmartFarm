# SMART FARM SERVER

## Installation
#### Prerequisites
* Docker
* Clone this repo

#### Run server 
> Go to server root

    docker build -t smartfarm/server:v1 .
    docker compose up

## Rest API
The apis are described as below

### Update threshold of sensor
Allow user to public new threshold value to corresponding feed. Only allow sensor data feed. The server will then append new log data on firebase at reference `<base_url>/<feed_id>/threshold`
#### Request
`POST /threshold/<feed_id>`

    Content-Type: application/json
    body: {
        "value": <integer>
    }
#### Response
##### Success
    Content-Type: application/json
    status: 200
    body: {
        "status": "ok"
        "value": <integer>
    }
##### Error
    Content-Type: application/json
    status: 400
    body: {
        "status": "error"
        "msg": <error_string>
    }

### Control device status
This api is for update the device's status `1:ON` `0:OFF`, the server then append new log data to database at the reference `<base_url>/log`
#### Log data schema

    log : {
        ...
        <log_id>: {
            event: "___",
            feed: "<feed_id>",
            time: "<utc_datetime>",
            value: "<feed_value>"
        }
    }


#### Request
`POST /button/<feed_id>`

    Content-Type: application/json
    body: {
        "value": <integer-0/1>
    }
#### Response
##### Success
    Content-Type: application/json
    status: 200
    body: {
        "status": "ok"
        "value": <integer>
    }
##### Error
    Content-Type: application/json
    status: 400
    body: {
        "status": "error"
        "msg": <error_string>
    }
