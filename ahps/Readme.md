# AtHomeServer API Module
For complete documentation of the AtHomeServer interface, see 
[here](https://github.com/dhocker/athomepowerlineserver/blob/master/README.md).

## Module: athomeapi 
### Class: ServerRequest

**class ServerRequest(host="localhost", port=9999, verbose=True)**
```python
from athomeapi import ServerRequest
request = ServerRequest()
```

#### Instance Methods

**status_request()**
```python
result = request.status_request()
```
result
```json
{
  "request": "StatusRequest",
  "date-time": "2019-06-25 16:30:18.080467",
  "server": "PerryM2/AtHomePowerlineServer",
  "server-version": "2019.0.0.1",
  "result-code": 0,
  "day-of-week": "1",
  "firmware-revision": "0.0.0.0",
  "message": "Success",
  "call-sequence": 5
}
```

**device_on(device_id, dim_amount)**
```python
result = request.device_on(1, 0)
```
result
```json
{
    "request": "On",
    "date-time": "2019-06-22 14:12:14.983421",
    "server": "PerryM2/AtHomePowerlineServer",
    "server-version": "2019.0.0.1",
    "result-code": 0,
    "message": "Success",
    "call-sequence": 1
}
```

**device_off(device_id, dim_amount)**
```python
result = request.device_off(1, 0)
```
result
```json
{
    "request": "Off",
    "date-time": "2019-06-22 14:17:46.370052",
    "server": "PerryM2/AtHomePowerlineServer",
    "server-version": "2019.0.0.1",
    "result-code": 0,
    "message": "Success",
    "call-sequence": 2
}
```

**device_bright(device_id, bright_amount)**
```python
result = request.device_bright(1, 100)
```

**device_dim(device_id, dim_amount)**
```python
result = request.device_dim(1, 50)
```

**define_device(device)**
```python
device = {
    "device-name": "Device under test",
    "device-location": "Unknown test location",
    "device-type": "tplink",
    "device-address": "192.168.1.234",
    "device-selected": 0
}
request.define_device(device)
```
result
```json
{
    "request": "DefineDevice",
    "date-time": "2019-06-22 14:28:53.208809",
    "server": "PerryM2/AtHomePowerlineServer",
    "server-version": "2019.0.0.1",
    "result-code": 0,
    "device-id": 26,
    "message": "Success",
    "call-sequence": 3
}
```

**update_device(device)**
```python
device = {
    "device-id": 25,
    "device-name": "Device under test update 1",
    "device-location": "Unknown test location",
    "device-type": "tplink",
    "device-address": "192.168.1.234",
    "device-selected": 0
}
result = request.update_device(device)
```
result
```json
{
    "request": "UpdateDevice",
    "date-time": "2019-06-22 14:39:32.071068",
    "server": "PerryM2/AtHomePowerlineServer",
    "server-version": "2019.0.0.1",
    "result-code": 0,
    "device-id": 25,
    "message": "Success",
    "call-sequence": 4
}
```

**delete_device(device_id)**
```python
result = request.delete_device(25)
```
result
```json
{
    "request": "DeleteDevice",
    "date-time": "2019-06-23 13:18:24.745503",
    "server": "PerryM2/AtHomePowerlineServer",
    "server-version": "2019.0.0.1",
    "result-code": 0,
    "device-id": "25",
    "message": "Success",
    "call-sequence": 6
}
```

**open_request(request_json)**

Use to send a customized raw JSON request. Refer to 
[AtHomeServer documentation](https://github.com/dhocker/athomepowerlineserver/blob/master/README.md).
for complete documentation of all requests.

```python
result = request.device_dim(1, 50)
```
