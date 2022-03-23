![logo2](https://user-images.githubusercontent.com/76909130/153789287-58f516ff-ed97-45cc-8d8c-426956d27f84.png)

AnylinkCloud RestAPI

The token authentication of the following APIs adds support for `Authorization: Bearer [token]` in http/https request header. At the same time, it also continues to support the way of carrying tokens in the request body. If both the request body and the header contain a token, the one in the header shall prevail.

**The old way of carrying tokens in the request body will be deprecated in the future releases, please switch to the new way of using bearer header token in your new releases.**

The following image shows how to add a `Authorization: Bearer [token]` in the header when using postman to call the interface: 
![image-20220212121738282](https://user-images.githubusercontent.com/76909130/153696301-1f0d776d-0e6e-4742-8711-c63c7596f6ff.png)




## 1. Get token for AnylinkCloud UI

This token is for the following APIs only, for all other APIs, please use **[2. Get token for AnylinkCloud API](https://github.com/tetrascience/ts-anylink-shared/blob/master/Documents/API%20Instructions/AnylinkCloud%20RestAPI.md#2-get-token-for-anylinkcloud-api)** instead :  
- [1.  Modifying AnyLink Cloud user password](https://github.com/tetrascience/ts-anylink-shared/blob/master/Documents/API%20Instructions/AnylinkCloud%20RestAPI.md#3-change-anylinkcloud-api-password)
- [21. Get device list of a user](https://github.com/tetrascience/ts-anylink-shared/blob/master/Documents/API%20Instructions/AnylinkCloud%20RestAPI.md#21-get-device-list-of-a-user)  
- [22. Associate devices to a user](https://github.com/tetrascience/ts-anylink-shared/blob/master/Documents/API%20Instructions/AnylinkCloud%20RestAPI.md#22-associate-devices-to-a-user)  
- [23. Remove device from user](https://github.com/tetrascience/ts-anylink-shared/blob/master/Documents/API%20Instructions/AnylinkCloud%20RestAPI.md#23-remove-device-from-user)    

In AnyLink Cloud, there're two type of users, one is tenant user, which is used to login into the AnyLink cloud system via web UI, the other is API user, which is used to make API calls into AnyLink Cloud. And the user name here is tenant user name not AnyLink Cloud API user name.

The token is valid for 10 hours. After the timeout, you need to obtain a new token.

Request type:    POST

url:         /user/getToken

Parameters:  JSON

| Parameters  | Type   | Required | Comment            |
| ----------- | ------ | -------- | ------------------ |
| tenantEname | String | Yes      | Tenant name        |
| name        | String | Yes      | Tenant user name   |
| password    | String | Yes      | Password           |
| hash        | String | Yes      | Use ‘tetrascience’ |

Return value:  JSON    

| Parameters | Type   | Comment                       |
| ---------- | ------ | ----------------------------- |
| status     | String | return code: <br>**100**: successful   <br/>**103**: invalid parameter   <br/>**107**: tenant name not exist   <br/>unknown username<br>**115**: this user is locked<br>**116**: error password<br>**111**:other errors |
| msg        | String | Detail error message          |
| data       | String | Token value                   |

Sample request:

```json
{
    "tenantEname": "tetrascience",
    "name": "admin",
    "password": "123456",
    "hash": "tetrascience"
}
```

Sample response:

```json
{
    "status":"100",
    "data":"dc91c34b-6a11-437a-ab8e-fa6fdc3e547b"
}
```

## 2. Get token for AnylinkCloud API

Function: This token is used to call Anylink Cloud APIs.
The token is valid for 10 hours. After the timeout, you need to obtain a new token.

Request type: POST

url: /user/login

Parameters:

| Parameters | Type   | Required | Comment                       |
| ---------- | ------ | -------- | ----------------------------- |
| name       | String | yes      | AnyLink cloud API User name   |
| hash       | String | yes      | hash code. Use ‘tetrascience’ |
| password   | String | yes      | AnyLink cloud API password    |

```
{
    "name": "apiuser",
    "password": "123456",
    "hash": "tetrascience"
}
```

Return value: JSON

| Parameters | Type   | Comment                                                      |
| ---------- | ------ | ------------------------------------------------------------ |
| status     | String | return code: <br>**100**: successful<br>**103**: parameter error <br>**107**: There will be the following two situations: <br/>       username or password is error <br>       username does not exist<br>**111**: For some other errors, refer to the "msg" value. |
| msg        | String | error message                                                |
| data       | String | token                                                        |

```
{
    "status": "100",
    "data":"dc91c34b-6a11-437a-ab8e-fa6fdc3e547b"
}
```

## 3. Change AnylinkCloud API password

Function: Change the password for AnylinkCloud API user（The token can be obtained through the interface **'/user/login'** of AnylinkCloudAPI）.

Request type: PUT

url: /user/password

Parameters:

| Parameters | Type   | Required | Comment                                                    |
| ---------- | ------ | -------- | ---------------------------------------------------------- |
| token      | String | yes      | User token, this token is obtained through **/user/login** |
| hash       | String | yes      | hash code                                                  |
| password   | String | yes      | new password                                               |

Sample request： /user/password?token=dc91c34b-6a11-437a-ab8e-fa6fdc3e547b&hash=test&password=1234567

Return value: JSON

| Parameters | Type   | Comment                                                      |
| ---------- | ------ | ------------------------------------------------------------ |
| status     | String | return code: <br>**100**: successful <br>**101**: Please use system administrator account<br>**103**: parameter error <br>**104**: invalid token <br>**111**: For some other errors, refer to the "msg" value. |
| msg        | String | error message                                                |



```
{
    "status":"100"
}
```

## 4. Get AnylinkCloud deviceId by serialnumber and device name

Function: Get AnylinkCloud deviceId by serialnumber and device name

Request type: GET

url: /devicelist/getDeviceID

Parameters:

| Parameters | Type    | Required | Comment                   |
| ---------- | ------- | -------- | ------------------------- |
| token      | String  | yes      | User token                |
| hash       | String  | yes      | hash (use ‘tetrascience’) |
| deviceName | String  | yes      | device name               |
| agentID    | Integer | yes      | serialnumber              |

Return value: JSON

| Parameters | Type    | Comment                                                      |
| ---------- | ------- | ------------------------------------------------------------ |
| status     | String  | return code: <br>**100**: successful <br>**103**: parameter error <br>**104**: invalid token <br>**111**: For some other errors, refer to the "msg" value. |
| msg        | String  | error message                                                |
| data       | Integer | Anylink device id                                            |

Sample request:

/devicelist/getDeviceID?token=08a67a16-9e96-4bfd-8492-3f415585639c&hash=tetrascience&deviceName=test&agentID=1700631

Sample response:

```
{
    "status": "100",
    "data": 1228801025,
}
```

## 5. Send ASCII command to RS232

Function: Send ASCII command to RS232 on a specified device

Request type: POST

url: /control/device

Parameters: JSON

| Parameters   | Sub Parameters | Type    | Required | Comment                                                      |
| ------------ | -------------- | ------- | -------- | ------------------------------------------------------------ |
| token        |                | String  | yes      | User token. Both types of tokens are available               |
| hash         |                | String  | yes      | hash is not used for now（use ‘tetrascience’ as example and null is OK too） |
| serialNumber |                | Integer | yes      | AnyLink box serial number                                    |
| deviceId     |                | Integer | yes      | Anylink cloud device id. This value must be configured with libTetraSerialCmd driver. |
| driverName   |                | String  | yes      | Driver name, the value is libTetraSerialCmd, cannot be other values. |
| cmds         |                |         |          | JSONArray array of commands, multiple commands are allowed   |
|              | index          | Integer | yes      | A unique index of commands, used to distinguish different commands |
|              | serial         | String  | yes      | Semicolon separated Serial port communication parameters: "portNo;baudRate;parity;dataBit;stopBit;timeout". For example: "485_1;9600;N;8;1;5000" timeout is in milliseconds |
|              | type           | String  | yes      | Data type, default to ascii                                  |
|              | cmd            | String  | yes      | Content of command, base64 encoded utf-8 characters.         |
|              | res_len        | Integer | yes      | Expected max return length. **res_len** is a required parameter, if **res_len** is not specified, the driver does not respond until timeout. <br>If **res_len** <= 0 , the driver will not accept the data value returned by any device, and directly return success after writing the command, and return the empty value( "res_data": "", "res_len": 0,) <br>If **res_len** > 0, the driver will enter listening state according to the timeout parameter after writing the command and wait for the response of the device. If the device data received within the timeout is longer than **res_len**, exit listening in advance. After exiting listening, the driver will return the device data to the API. <br>If **res_len** is too large, the driver will wait until it receives enough data or time out. <br>If **res_len** is too small, the driver will cut the data returned by device. |


Return value: JSON

| Parameters | Sub Parameters | Type      | Comment                                                      |
| ---------- | -------------- | --------- | ------------------------------------------------------------ |
| status     |                | String    | return code: <br>**100**: successful <br>**102**: REST API call timeout <br>**103**: parameter error, such as "cmd cannot be empty", "invalid base64 encoding" <br />**104**: invalid token <br />**111**: For some other errors, refer to the "msg" value. <br />**125**: Anylink box is offline |
| msg        |                | String    |                                                              |
| resps      |                | JSONArray | Responses from commands                                      |
|            | index          | Integer   | command index                                                |
|            | res_data       | String    | Content of command response, base64 encoded utf-8 characters. |
|            | res_error      | String    | Error message from the agent, i.e. "Can't Open Serial Port!" when USB cable is unplugged from the IoT box |
|            | res_len        | Integer   | Length of command response                                   |
|            | rs             | Integer   | Command result: 0: success -1: failure 7: Driver not found   |
|            | userid         | String    | Identification code used to obtain control results via API /control/result. |


Sample request:

```
{
    "token":"f53073f3-ef67-4bb5-a152-eab3f3139331",
    "hash":"1234",
    "serialNumber":1700631,
    "deviceId":1741446148,
    "driverName":"libTetraSerialCmd",
    "cmds":[
        {
            "index":1,
            "serial":"/dev/ttyUSB0;9600;None;8;1;5000",
            "type":"ascii",
            "cmd":"VGhpcyBpcyBhIHJlcXVlc3QgdGVzdA==",
            "res_len":10
        }
    ]
}
```

`"serial":"/dev/ttyUSB0;9600;None;8;1;5000"` The last value is the timeout (time in `ms`)

Sample response:

```
{
    "resps": [
        {
            "index": 1,
            "res_data": "dGhpcyBpcyBhIHJlc3BvbnNlIHRlc3Qh",
            "res_len": 24,
            "rs": 0,
            "userid": "1609836987877325"
        }
    ],
    "status": "100"
}
{
    "msg": "Anylink box is offline",
    "status": "125"
}
{
    "msg": "cmd cannot be empty",
    "status": "103"
}
{
    "msg": "Get command response timeout.",
    "status": "102"
}
```

## 6. How to configure Device for RS232

Here’s the sample configuration for device in the AnyLink box:

```
<model n="Http2Serial" id="1">
    <device n="Http2Serial1" id="1" ip="192.168.1.1" type="test">
        <driver n="IDrv.Custom:libTetraSerialCmd" config="">
            <commDataItems/>
        </driver>
    </device>
</model>
```

If the driver to be upgraded is task driver, you should add the driver both in task driver and model/device/driver. Dont forget the **version** attribute. The configuration is as follows:

```
<task>
    <TaskDriver>
      <driver config="test" id="1" n="T.IDrv.Task:libTUsbtenki" version="1.0.2"/>
    </TaskDriver>
</task>
<model config="test" d="T.IDrv.Task:libTUsbtenki" id="1" n="task">
    <device id="1" ip="192.168.1.1" n="DIP-production-tetrascience-1701354-1" type="test">
      <driver config="" id="1" n="T.IDrv.Task:libTUsbtenki" version="1.0.2">
        <commDataItems>
          <dataItem alias="temperature" config="0" freq="60000" id="1" n="temp" report="1" rw="1" type="a"/>
        </commDataItems>
      </driver>
    </device>
</model>
```

## 7. Get AnyLink IoT agent firmware version

Function: Get firmware versions for agent, web, script from AnyLink IoT box

Request type: GET

url: /anylinkAttribute

Parameters:

| Parameters   | Type    | Required | Comment                                        |
| ------------ | ------- | -------- | ---------------------------------------------- |
| token        | String  | yes      | User token. Both types of tokens are available |
| serialNumber | Integer | yes      | AnyLink box serial number                      |

Response: JSON

| Parameters    | Type       | Comment                                                      |
| ------------- | ---------- | ------------------------------------------------------------ |
| status        | String     | return code: <br />**100**: successful <br />**103**: parameter error <br />**104**: invalid token <br />**111**: For some other errors, refer to the "msg" value. |
| msg           | String     | error message                                                |
| data          | JSONObject |                                                              |
| agentVersion  | String     | agent version                                                |
| scriptVersion | String     | script version                                               |
| webVersion    | String     | web for Anylink configuration                                |
| serialNumber  | Integer    | AnyLink box serial number                                    |

Sample request:

```
{
    "token":"96acfbae-e27b-48ee-b3be-f6c3363feee1",
    "serialNumber": 1700630,
}
```

Sample response:

```
{
    "status":"100",
    "data":{
        "agentVersion":"3.7.16",
        "scriptVersion":"2.6.6",
        "serialNumber":1700630,
        "webVersion":"3.5.4"
    }
}
```

## 8. Gets the historical data of a dataitem

Function: Get the historical data of a dataitem

Request type: GET

url: /historydata

Parameters:

| Parameters | Type    | Required | Comment                                                      |
| ---------- | ------- | -------- | ------------------------------------------------------------ |
| token      | String  | yes      | User token.                                                  |
| hash       | String  | yes      | hash（use ‘tetrascience’）                                   |
| deviceid   | Integer | yes      | AnylinkCloud device id                                       |
| dataitemid | String  | yes      | AnylinkCloud dataitem id                                     |
| stime      | Long    | no       | Start time, UTC timestamp in `milliseconds`. If this value is empty, the default value is 12 hours before the current time. |
| etime      | Long    | no       | End time, UTC timestamp in `milliseconds`. If this value is empty, the default value is current time. |

Return value: JSON

| Parameters | Type    | Comment                                                      |
| ---------- | ------- | ------------------------------------------------------------ |
| status     | String  | return code: <br />**100**: successful <br />**103**: parameter error <br />**104**: invalid token <br />**111**: For some other errors, refer to the "msg" value. |
| msg        | String  | error message                                                |
| data       | array   |                                                              |
| devid      | String  | AnylinkCloud device id                                       |
| itemid     | String  | Dataitem id                                                  |
| itemname   | String  | Dataitem name                                                |
| alias      | String  | Dataitem alias                                               |
| val        | String  | History value                                                |
| htime      | String  | UTC timestamp string                                         |
| datatype   | String  | data type, e.g 'a', 'b', 's'                                 |
| readOnly   | Boolean | true: read-only, false: writable                             |

Sample request: /historydata?token=fd361aec-6173-4518-8b89-09c21565af52&deviceid=1435394049&dataitemid=1&hash=test&stime=1536570000000&etime=1536573600000

Sample Response:

```
{
    "status":"100",
    "data":[
        {
            "alias":"channel0",
            "datatype":"a",
            "datatypeName":"decimal",
            "devName":"SHT31",
            "devid":"1435394049",
            "htime":"2018-09-10 05:42:33.0",
            "itemid":"1",
            "itemname":"channel0",
            "readOnly":true,
            "val":"3465.041748046875"
        },
        {
            "alias":"channel0",
            "datatype":"a",
            "datatypeName":"decimal",
            "devName":"SHT31",
            "devid":"1435394049",
            "htime":"2018-09-10 05:42:23.0",
            "itemid":"1",
            "itemname":"channel0",
            "readOnly":true,
            "val":"99518.921875"
        }
    ]
} 
```

# The following APIs(9-13) are the remote configuration of WiFi

## 9. Issue command to the agent, and the agent uploads the configuration file

Function: Issue the control command to the agent, and the agent uploads the configuration file

Request type: PUT

url： /remoteAgent/uploadCmd

Parameters:

| Parameters   | Type    | Required | Comment                                                      |
| ------------ | ------- | -------- | ------------------------------------------------------------ |
| token        | String  | yes      | User token. Both types of tokens are available               |
| hash         | String  | yes      | hash（use ‘tetrascience’）                                   |
| filetype     | String  | yes      | Type of file to upload: anylink_xml(for WIFI config), idinfo_xml alldevicedriver_xml, config_xml |
| serialnumber | Integer | yes      | AnyLink box serial number                                    |

Return value: JSON

| Parameters | Type   | Comment                                                      |
| ---------- | ------ | ------------------------------------------------------------ |
| status     | String | return code: <br />**100**: successful <br />**103**: parameter error, such as "File type must be one of the following: anylink_xml, idinfo_xml, alldevicedriver_xml, config_xml" <br />**104**: invalid token<br />**99**: failed to send command to agent. Failure reason: refer to "msg" value<br />**111**: For some other errors, refer to the "msg" value. |
| msg        | String | error message                                                |
| data       | String | Identification code used to obtain control results           |

```
{
    "status": "100",
    "data": 1415844000000
}
```

## 10. Get the result for a command

Function: Get the result for the command (you need to loop until you get the result). Now the **timeout** is 90s, if there's no response when timeout is triggered, API will consider it as timeout. The result from /control/result will be

```
{
    "status":100,
    "data":"3"
}
```

3 means timeout.

Request type: GET

url： /control/result

Parameters:

| Parameters | Type   | Require | Comment                                                      |
| ---------- | ------ | ------- | ------------------------------------------------------------ |
| token      | String | yes     | User token. Both types of tokens are available               |
| hash       | String | yes     | hash（use ‘tetrascience’）                                   |
| sign       | String | yes     | Get the result for the command，this is the data value from API "/remoteAgent/uploadCmd" |

Return value: JSON

| Parameter | Type   | Comments                                                     |
| --------- | ------ | ------------------------------------------------------------ |
| status    | String | return code: <br />**100**: successful <br />**103**: parameter error <br />**104**: invalid token<br />**111**: For some other errors, refer to the "msg" value. |
| msg       | String | error message                                                |
| data      | String | Result（0：success，3：overtime，others：failed）            |

```
{
    "status":"100",
    "data":"0"
}
```

## 11. Get the Agent Configuration XML file for a specific IoT box

Function： Get the XML file that Anylink uploaded. Before calling this API, you must first issue a command to the agent through the interface ```/remoteagent/uploadcmd``` to let the agent upload the configuration file to the server.

Request type: GET

url： /device/readAnylinkXml

Parameters: JSON

| Parameters   | Value   | Required | Comments                                                 |
| ------------ | ------- | -------- | -------------------------------------------------------- |
| token        | String  | yes      | User token. Both types of tokens are available           |
| hash         | String  | yes      | hash（use ‘tetrascience’）                               |
| xmlType      | String  | yes      | XML file type： anylink_xml(for WIFI config), config_xml |
| serialNumber | Integer | yes      | AnyLink box serial number                                |

Return value: JSON

| Parameters | Value  | Comments                                                     |
| ---------- | ------ | ------------------------------------------------------------ |
| status     | String | return code: <br />**100**: successful <br />**103**: parameter error<br />**104**: invalid token <br />**111**: For some other errors, refer to the "msg" value. |
| data       | String | Result                                                       |
| msg        | String | Error message                                                |

Response example:

```
{
    "status":"100",
    "data":"<AnyLink><BasicInfo><HardwareModel>AnyLink 200</HardwareModel><AgentVersion>V3.6.6</AgentVersion><SoftVersion>DA-3.3.77</SoftVersion><SerialNumber>1400032</SerialNumber></BasicInfo>.......<NetworkInfo muti="YES" hostname="id0032"><Mode>gateway</Mode><Model>simcom</Model><WAN dhcp="NO" mask="255.255.255.0" gateway="192.168.100.1" dns="114.114.114.114" ip="192.168.100.215"/><LAN dhcp="NO" mask="255.255.255.0" gateway="192.168.101.1" dns="114.114.114.114" ip="192.168.101.204"/></NetworkInfo><VPN display="YES"/><Wifi><W_Modestatus>start</W_Modestatus><W_SSID>redbudtek-Guest</W_SSID><W_Password/><W_Status>COMPLETED</W_Status><W_IP>192.168.1.113</W_IP><W_DHCP>YES</W_DHCP><W_GATEWAY>0.0.0.0</W_GATEWAY><W_STRONG>-79</W_STRONG><W_NETMASK>255.255.255.0</W_NETMASK></Wifi>......</AnyLink>"
}
```

## 12. Send Agent configuration file (Anylink.xml or ModuleConfig.xml) to agent

Function: Send configuration file to agent

Request type: POST

url： /remoteAgent/sendAnylinkXML

Parameters:

| Parameters   | Value   | Required | Comments                                                     |
| ------------ | ------- | -------- | ------------------------------------------------------------ |
| token        | String  | yes      | User token. Both types of tokens are available               |
| hash         | String  | yes      | hash（use ‘tetrascience’）                                   |
| filetype     | String  | yes      | XML file type： anylink_xml(for WIFI config), config_xml (ModuleConfig.xml for agent)    |
| serialnumber | Integer | yes      | AnyLink box serial number                                    |
| anylinkType  | String  | no       | For **WIFI** configuration，filetype=”anylink_xml”, anylinkType="WIFI", otherwise leave this empty |
| content      | String  | yes      | Send content                                                 |

Example for WIFI configuration：

```
{
     "token":"8fa07284-661c-4aec-99ad-38e894c8ebe0",
     "filetype":"anylink_xml",
     "serialnumber":1401868,
     "anylinkType": "WIFI",
     "content": "<AnyLink>......</AnyLink>"
}
```

Example for config_xml：

```
{
     "filetype":"config_xml",
     "serialnumber":1401868,
     "token":"8fa07284-661c-4aec-99ad-38e894c8ebe0",
     "content":"<agent ......</agent>"
}
```

Reponse value:

| Parameters | Type   | Comments                                                     |
| ---------- | ------ | ------------------------------------------------------------ |
| status     | String | return code: <br />**100**: successful <br />**103**: parameter error, such as "For file type anylink_xml, anylinkType is required, and the value can be one of the following: SYNC, LANIP, WIFI", "Invalid XML content."<br />**104**: invalid token <br />**99**: Configuration file can only be uploaded when Anylink box is online. <br />**111**: For some other errors, refer to the "msg" value. |
| data       | Long   | The register ID of this distribution operation is used when calling the interface to get the registration result (/agent/register) |
| msg        | String | Error message                                                |

```
{
    "status":"100",
    "data":"1534311799247"
}
{
    "status": "99",
    "msg": "Configuration file can only be uploaded when Anylink box is online."
}
```
Anylink.xml structure:
```xml
<AnyLink> 
  <BasicInfo> 
    <HardwareModel>AnyLink 100</HardwareModel>  
    <AgentVersion>V3.6.7</AgentVersion>  
    <SoftVersion>DA-3.4.7</SoftVersion>  
    <SerialNumber>1401561</SerialNumber> 
  </BasicInfo>  
  <ZigbeeInfo> 
    <Type>0</Type>  
    <NetNumber>50</NetNumber>  
    <NetAddress>0</NetAddress>  
    <Physchannel>19</Physchannel> 
  </ZigbeeInfo>  
  <LoraInfo> 
    <g_baudrate>9600</g_baudrate>  
    <g_parity>NONE</g_parity>  
    <g_RF_freq>443</g_RF_freq>  
    <g_RF_factor>10</g_RF_factor>  
    <g_RF_mode>normal</g_RF_mode>  
    <g_RF_BW>125K</g_RF_BW>  
    <g_ID_H>0</g_ID_H>  
    <g_ID_L>0</g_ID_L>  
    <g_net_ID>0</g_net_ID>  
    <g_power>20db</g_power> 
  </LoraInfo>  
  <NetworkInfo muti="YES" hostname="id1561"> 
    <Mode>gateway</Mode>  
    <Model>simcom</Model>  
    <WAN mac="C4:F3:12:F2:F2:B3" dns="114.114.114.114" ip="192.168.100.220" dhcp="NO" mask="255.255.255.0" gateway="192.168.100.1"/>  
    <LAN mac="C4:F3:12:F2:F2:B5" dns="114.114.114.114" ip="192.168.101.204" dhcp="NO" mask="255.255.255.0" gateway="192.168.101.1"/> 
  </NetworkInfo>  
  <VPN display="YES"/>  
  <Wifi> 
    <W_Modestatus>start</W_Modestatus>  
    <W_SSID>redbudtek-Guest</W_SSID>  
    <W_Password>82602929</W_Password>  
    <W_Status>COMPLETED</W_Status>  
    <W_IP>192.168.1.113</W_IP>  
    <W_DHCP>YES</W_DHCP>  
    <W_GATEWAY>0.0.0.0</W_GATEWAY>  
    <W_MAC>EC:3D:FD:30:91:50</W_MAC>  
    <W_STRONG>-83</W_STRONG>  
    <W_NETMASK>255.255.255.0</W_NETMASK>  
    <!-- Fill in here when sending multiple WiFi messages remotely -->  
    <W_Remote> 
      <W_List> 
        <W_Info> 
          <W_SSID>ssid1</W_SSID>  
          <W_Password>password1</W_Password> 
        </W_Info>  
        <W_Info> 
          <W_SSID>ssid1</W_SSID>  
          <W_Password>password1</W_Password> 
        </W_Info> 
      </W_List> 
    </W_Remote> 
  </Wifi>  
  <CloudInfo> 
    <Address>s1.anylinkcloud.com:8686</Address> 
  </CloudInfo>  
  <ApnInfo> 
    <IsAuto>0</IsAuto>  
    <Apn/>  
    <Proxy/>  
    <Port/>  
    <Username/>  
    <Password/> 
  </ApnInfo>  
  <TimeZoneInfo> 
    <TimeZone>UTC</TimeZone> 
  </TimeZoneInfo>  
  <AgentConfig> 
    <AgentMode>0</AgentMode>  
    <UploadType>1</UploadType>  
    <RegRetryCount>100</RegRetryCount>  
    <QueueSize>1</QueueSize>  
    <Protocol>mqtt</Protocol>  
    <LogPath/>  
    <AlarmMode>0</AlarmMode>  
    <DBEnable>1</DBEnable>  
    <DBSize>10000</DBSize>  
    <DBScanTime>3</DBScanTime>  
    <BadDataMode>0</BadDataMode> 
  </AgentConfig> 
</AnyLink>
```
| **Element**   | **Comments**                          | **Value**                                                    |
| ------------- | ------------------------------------- | ------------------------------------------------------------ |
| W\_Modestatus | Wifi mode                             | start，stop                                                  |
| W\_SSID       | Wifi name                             |                                                              |
| W\_Password   | Wifi password                         |                                                              |
| ~~W\_Status~~ | Deprecated                            | Deprecated                                                   |
| W\_IP         | Wifi ip address                       | Automatic acquisition                                        |
| W\_MAC        | MAC address of WiFi module            | Automatic acquisition                                        |
| W\_DHCP       | Whether WiFi automatically obtains IP | At present, it can only be set to YES. Only automatic acquisition is supported, and manual modification is not supported. |
| W\_GATEWAY    | Wifi gateway                          | Automatic acquisition                                        |
| W\_STRONG     | Wifi signal strength                  | Automatic acquisition                                        |
| W\_NETMASK    | WiFi subnet mask                      | Automatic acquisition                                        |
| W\_Remote     | Hidden WiFi list                      | Fill in here when sending multiple WiFi messages remotely    |

**Multi-WiFi settings**: 

  （1）The WiFi module will select the available WiFi with the best signal in the W_List to connect

 （2）When the WiFi list sent to Anylink, it will be completely overwritten, that is, all the old WiFi lists will be deleted. If you want to retain the old wifi, you also need to keep them in the new configuration

**ModuleConfig.xml structure:**
```xml
<agent flag="SET-TASKS" id="{{IoTBox-SerialNumber}}" n="{{Agent-Name}}" port="-1" script="1.1.0" sdmwebs="1.1.0" timezone="UTC"> 
  <model n="{{Model-Name}}"> 
    <device n="DeviceName" id="3" ip="192.168.1.1" type="test"> 
      <driver config="1;0" id="3" n="T.IDrv.Task:libTModbus" version="1.4.3"> 
        <commDataItems> 
          <dataItem n="A1" alias="A1_alias" config="" freq="60000" id="34" report="1" rw="0" type="a"/>  
          <dataItem n="A2" alias="A2_alias" config="" freq="60000" id="35" report="1" rw="0" type="b"/> 
        </commDataItems> 
      </driver> 
    </device> 
  </model>  
  <task> 
    <TaskDriver> 
      <driver config="10001" n="T.IDrv.Task:libcontrol"/> 
    </TaskDriver>  
    <TaskDriver> 
      <driver config="NULL;115200;8;N;1;0;1;0;0;localhost;10001;6;60;1;10000;3" n="T.IDrv.Task:libzigbee"/> 
    </TaskDriver>  
    <TaskDriver> 
      <driver config="us-s1.anylink.io;8883;us-s1.anylink.io;8883;60;2;0;0;;;;1;-1" n="T.IDrv.Task:libkmqtt"/> 
    </TaskDriver>  
    <TaskDriver>AnyLink LLC Page 3 | 3 
      <driver config="1" n="T.IDrv.Task:libtremoteplc"/> 
    </TaskDriver>  
    <TaskDriver> 
      <driver config="rtu;/dev/ttymxc2;9600;Even;7;1;STANDARD;200;100;20" id="3" n="T.IDrv.Task:libTModbus" version="1.4.3"/> 
    </TaskDriver> 
  </task>  
  <model n="ra-model"> 
    <device id="1023" ip="127.0.0.1" n="ra-device"> 
      <driver config="1;wlan0;" n="T.IDrv.Task:libtremoteplc"> 
        <commDataItems> 
          <dataItem addr="" config="" freq="120000" id="1" n="CSQ" report="1" rw="0" type="a" vtype=""/>  
          <dataItem addr="" config="" freq="120000" id="2" n="NET-TYPE" report="1" rw="0" type="s" vtype=""/>  
          <dataItem addr="" config="" freq="120000" id="3" n="WAN-IP" report="1" rw="0" type="s" vtype=""/>  
          <dataItem addr="" config="" freq="120000" id="4" n="WAN-MAC" report="1" rw="0" type="s" vtype=""/>  
          <dataItem addr="" config="" freq="120000" id="5" n="WIFI-LIST" report="1" rw="0" type="s" vtype=""/>  
          <dataItem addr="" config="" freq="120000" id="6" n="WIFI-IP" report="1" rw="0" type="s" vtype=""/>  
          <dataItem addr="" config="" freq="120000" id="7" n="WIFI-MAC" report="1" rw="0" type="s" vtype=""/>  
          <dataItem addr="" config="" freq="120000" id="8" n="WIFI-SSID" report="1" rw="0" type="s" vtype=""/>  
          <dataItem addr="" config="" freq="120000" id="9" n="WIFI-STRONG" report="1" rw="0" type="s" vtype=""/>  
          <dataItem addr="" config="" freq="120000" id="10" n="WIFI-DHCP" report="1" rw="0" type="s" vtype=""/>  
          <dataItem addr="" config="" freq="120000" id="11" n="UPTIME" report="1" rw="0" type="s" vtype=""/>  
          <dataItem addr="" config="" freq="120000" id="12" n="WIFI-BSSID" report="1" rw="0" type="s" vtype=""/>  
          <dataItem addr="" config="" freq="120000" id="13" n="USB-DEVS" report="1" rw="0" type="s" vtype=""/>  
          <dataItem addr="" config="" freq="120000" id="14" n="GPS-MCC" report="1" rw="0" type="s" vtype=""/>  
          <dataItem addr="" config="" freq="120000" id="15" n="GPS-MNC" report="1" rw="0" type="s" vtype=""/>  
          <dataItem addr="" config="" freq="120000" id="16" n="GPS-LAC" report="1" rw="0" type="a" vtype=""/>  
          <dataItem addr="" config="" freq="120000" id="17" n="GPS-CID" report="1" rw="0" type="a" vtype=""/>  
          <dataItem addr="" config="" freq="120000" id="18" n="MEMORY" report="1" rw="0" type="s" vtype=""/>  
          <dataItem addr="" config="" freq="120000" id="19" n="STORAGE" report="1" rw="0" type="s" vtype=""/>  
          <dataItem addr="" config="" freq="120000" id="20" n="GPS-LONGITUDE" report="1" rw="0" type="s" vtype=""/>  
          <dataItem addr="" config="" freq="120000" id="21" n="GPS-LATITUDE" report="1" rw="0" type="s" vtype=""/>  
          <dataItem addr="" config="" freq="120000" id="22" n="WIFI-TYPE" report="1" rw="0" type="s" vtype=""/>  
          <dataItem addr="" config="" freq="120000" id="23" n="WIFI-HIDDEN" report="1" rw="0" type="s" vtype=""/> 
        </commDataItems> 
      </driver> 
    </device> 
  </model> 
</agent>
```
| **Element**                                      | **Attribute** | **Required** | **Description**                                              |
| ------------------------------------------------ | ------------- | ------------ | ------------------------------------------------------------ |
| agent                                            | id            | Yes          | Agent Serial Number                                          |
|                                                  | n             | Yes          | Agent name: letters, numbers and &#39;-&#39;, &#39;+&#39; are allowed |
|                                                  | port          | Yes          | Reserved, default is -1                                      |
|                                                  | script        | Yes          | Script version                                               |
|                                                  | sdmwebs       | Yes          | Local web UI version                                         |
|                                                  | timezone      | Yes          | Agent timezone                                               |
|                                                  | Flag          | Yes          | Reserved, default is SET-TASKS                               |
| agent/task/TaskDriver/driver                     | n             | Yes          | Task driver name: file name of driver without file extention |
|                                                  | config        | Yes          | Task driver config string                                    |
|                                                  | id            | No           | Task driver id, if task driver is used in the device element, the driver id&#39;s in the\&lt;TaskDriver\&gt; and \&lt;device\&gt; must match. |
|                                                  | version       | No           | Task driver version                                          |
| agent/model                                      | n             | Yes          | Device model name                                            |
| agent/model/device                               | id            | Yes          | Device ID，ra-device must have id as 1023                    |
|                                                  | n             | Yes          | Device name: letters, numbers and &#39;-&#39;, &#39;+&#39; are allowed |
|                                                  | ip            | Yes          | Reserved attribute, default to 192.168.1.1                   |
| agent/model/device/driver                        | n             | Yes          | Driver name                                                  |
|                                                  | config        | Yes          | Driver config string: usually defines how driver communicates with data source. Thisis driver specific, please refer each driver document for detail. |
|                                                  | version       | No           | Driver version.                                              |
|                                                  | id            | No           | Task driver id, if task driver is used in the device element, the driver id&#39;s in the\&lt;TaskDriver\&gt; and \&lt;device\&gt; must match. |
| agent/model/device/driver/commDataItems/dataItem | id            | Yes          | Data item id                                                 |
|                                                  | n             | Yes          | Data item name                                               |
|                                                  | alias         | No           | Data item name alias                                         |
|                                                  | config        | Yes          | Reserved.                                                    |
|                                                  | freq          | Yes          | Data item upload frequency                                   |
|                                                  | report        | Yes          | Whether to upload this data item, 1: upload, 0: not upload   |
|                                                  | rw            | Yes          | Whether this data item value is writable from cloud，1: writable |
|                                                  | type          | Yes          | Data item type，&#39;a&#39; is numerical value, &#39;b&#39; is Boolean, &#39;s&#39; is string |
|                                                  | vtype         | Yes          | Reserved                                                     |

**dataitem.type**

| **Value** | **Comments**    | **Corresponding data type**                                  |
| --------- | --------------- | ------------------------------------------------------------ |
| a         | numerical value | BYTE, WORD, DWORD, FLOAT, uint8, int8, uint16, int16, uint32, int32 |
| b         | boolean         | BOOLEAN                                                      |
| s         | String          | STRING                                                       |

**dataitem.config**

| **Index** | **libDModbus**                             |
| --------- | ------------------------------------------ |
| 1         | Slave address                              |
| 2         | Function code                              |
| 3         | Data address                               |
| 4         | Operation mode                             |
| 5         | Data type                                  |
| 6         | Now this is invalid                        |
| 7         | 1—Small end alignment，0—Big end alignment |
| 8         | Lora network ID，-1 means invalid          |


**MQTT configuration**

```xml
<TaskDriver>
	<driver n="T.IDrv.Task:libkmqtt" config="192.168.100.102;8883;192.168.100.102;8883;60;2;0;0;admin;public;;1;" />
</TaskDriver>
```

 The items in config are as follows：

phost;pport;shost;sport;keepalive;qos;retain;bencode;user;password;bindaddr;btls;

|           | **Comments**                                        | **Recommended value**      |
| --------- | --------------------------------------------------- | -------------------------- |
| phost     | MQTT server address                                 |                            |
| pport     | MQTT server port                                    | SSL：8883<br>Non SSL：1883 |
| shost     | MQTT server address                                 |                            |
| sport     | MQTT server port                                    | SSL：8883<br>Non SSL：1883 |
| keepalive | time（use default value）                           | 60                         |
| qos       | Message quality (use default value)                 | 2                          |
| retain    | Retain value of MQTT message                        | 0                          |
| bencode   | User name and password encryption，0-None，1-base64 | 0                          |
| user      | SSL username                                        |                            |
| password  | SSL password                                        |                            |
| bindaddr  | Null value                                          | Null value                 |
| btls      | Whether open TLS                                    | 1 -- SSL<br>0 -- tcp       |


## 13. Query the result of sending XML file

Function: After send the configuration file to Anylink box, the agent will register to again. This interface is used to obtain the registration result.

Request type GET

url： /agent/register

Prameters: JSON

| Parameters   | Type    | Required | Comment                                                |
| ------------ | ------- | -------- | ------------------------------------------------------ |
| token        | String  | yes      | User token. Both types of tokens are available         |
| serialNumber | Integer | yes      | AnyLink box serial number                              |
| registerID   | Long    | yes      | The value is the data from /remoteAgent/sendAnylinkXML |

Response: JSON

| Parameters | Type   | Comments                                                     |
| ---------- | ------ | ------------------------------------------------------------ |
| status     | String | return code: <br />**100**: successful, <br />**102**: Timeout<br />**103**: parameter error, <br />**104**: invalid token <br />**122**: AnyLink box is waiting to register.<br />**123**: Registration failed<br />**125**: Get status failed because AnyLink box is offline.<br />**126**: Registering<br />**111**: For some other errors, refer to the "msg" value. |
| msg        | String | Error message                                                |

## 14. Upload OTA upgrade file

Function: Uplaod OTA upgrade file to AnylinkCloud. oldVersion + newVersion is the unique index, if this record exist, it will be covered by new file, otherwise new file will be added.

Request type: POST

url： /ota/addOTAVersion

Prameters: form-data

| Parameters | Type   | Required | Comment                                                      |
| ---------- | ------ | -------- | ------------------------------------------------------------ |
| token      | String | yes      | User token. Both types of tokens are available               |
| oldVersion | String | yes      | The agent version for which the upgrade package is applicable. Multiple version numbers are separated by commas, e.g. "3.7.0,3.7.1". |
| newVersion | String | yes      | Upgraded version                                             |
| fileName   | String | yes      | File name of upgrade file                                    |
| fileStream | File   | yes      | File stream of upgrade file                                  |

Response: JSON

| Parameters | Type   | Comments                                                     |
| ---------- | ------ | ------------------------------------------------------------ |
| status     | String | return code: <br />**100**: successful<br />**103**: parameter error  <br />**104**: invalid token <br />**111**: For some other errors, refer to the "msg" value.<br />**133**: otaUpgradeFilePath is null |
| msg        | String | Error message                                                |

# 15. Add Driver Version

Function: Upload driver upgrade file to AnylinkCloud.

Request type: POST

url： /addDriverVersion

Prameters: form-data

| Parameters    | Type   | Required | Comment                                                      |
| ------------- | ------ | -------- | ------------------------------------------------------------ |
| token         | String | Yes      | User token. Both types of tokens are available               |
| agentVersion  | String | Yes      | The agent version for which the upgrade package is applicable. Multiple version numbers are separated by commas, e.g. "3.7.0,3.7.1". You can also fill in the version range, separated by "-", e.g. "3.0.1-3.2.0". |
| driverName    | String | Yes      | Driver name                                                  |
| driverVersion | String | Yes      | Driver version                                               |
| fileName      | String | Yes      | File name of upgrade file, and correct suffix is required.   |
| fileStream    | File   | Yes      | File stream of upgrade file                                  |
| anylinkModel  | String | Yes      | Anylink model, such as DA, IE, IE Pro, WINDOWS               |
| description   | String | No       | You can add some useful description information for the driver. |
| remark        | String | No       |                                                              |

Response: JSON

| Parameters | Type   | Comments                                                     |
| ---------- | ------ | ------------------------------------------------------------ |
| status     | String | return code: <br />**100**: successful <br />**103**: parameter error<br />**104**: invalid token <br />**111**: For some other errors, refer to the "msg" value.<br />**133**: rddUpgradeFilePath is null |
| msg        | String | Error message                                                |

# 16. Get driver list

Function: Get the driver list uploaded to AnylinkCloud.

Request type: GET

url： /rdd/rddVersionList

Prameters:

| Parameters    | Type    | Required | Comment                                                      |
| ------------- | ------- | -------- | ------------------------------------------------------------ |
| token         | String  | Yes      | User token. Both types of tokens are available               |
| page          | Integer | No       | Page number, starting from 1. Default value is "1"           |
| perPage       | Integer | No       | Number of data per page. Default value is "10"               |
| driverVersion | String  | No       | Driver version                                               |
| driverName    | String  | No       | Driver name                                                  |
| agentVersion  | String  | No       | The agent version for which the upgrade package is applicable. |
| anylinkModel  | String  | No       | Anylink model, such as DA, IE, IE Pro, WINDOWS               |

Response: JSON

```
{
    "status": "100",
    "data": [
        {
            "id": 1,
            "anylinkModel": "IE",
            "anylinkVersion": "3.7.21",
            "driverName": "libddemo1",
            "driverVersion": "1.1.1",
            "fileName": "libddemo1_IE_1.1.1_3.7.21.zip",
            "filePath": "/usr/apps/sdmconfig-new/rdd/IE/libddemo1_IE_1.1.1_3.7.21.zip",
            "description": "test",
            "remark": "test",
            "createTime": 1622693107060,
            "updateTime": 1622693107060
        }
    ]
}
```

# 17. Delete driver file

Function: Delete one driver file uploaded to AnylinkCloud

Request type: DELETE

url： /rdd/deleteRddVersion

Prameters:

| Parameters | Type   | Required | Comment                                        |
| ---------- | ------ | -------- | ---------------------------------------------- |
| token      | String | Yes      | User token. Both types of tokens are available |
| id         | String | Yes      |                                                |

Response JSON:

| Parameters | Type   | Comments                                                     |
| ---------- | ------ | ------------------------------------------------------------ |
| status     | String | return code: <br />**100**: successful, <br />**103**: parameter error<br />**104**: invalid token <br />**111**: For some other errors, refer to the "msg" value. |
| msg        | String | Error message                                                |

```
{    "status": "100"}
```

# 18. API to get AnyLink IoT box online/offline status

Function: Get current online/offline status of IoT boxes

Request type: POST

url: /agentList/condition

Prameters:

| Parameters | Type      | Required | Comment                                        |
| ---------- | --------- | -------- | ---------------------------------------------- |
| token      | String    | Yes      | User token. Both types of tokens are available |
| agentIds   | JSONArray | Yes      | An Array of IoT boxes' Serial Numbers          |

Sample request:

```
{
    "token": "805b2b68-0f3b-47c2-a57a-0401d2f2b95c",
    "agentIds":[
        1701354,
        1701178
    ]
}
```

Response JSON:

| Parameters | Type      | Comments                                                     |
| ---------- | --------- | ------------------------------------------------------------ |
| status     | String    | return code: <br />**100**: successful <br />**103**: parameter error<br />**104**: invalid token<br />**111**: For some other errors, refer to the "msg" value. |
| msg        | String    | Error message                                                |
| data       | JSONArray | agentid: serialnumber, condition: 0--offline, 1--online      |

```
{
    "status": "100",
    "data": [
        {
            "agentid": 1701178,
            "condition": 0
        },
        {
            "agentid": 1701354,
            "condition": 1
        }
    ]
}
```

# 19. Get list of agents (IoT boxes' serial numbers) and devices for a specific user

Function: Get agent and device list

Request type: GET

url: /agentList

Prameters:

| Parameters | Type   | Required | Comment                                        |
| ---------- | ------ | -------- | ---------------------------------------------- |
| token      | String | Yes      | User token. Both types of tokens are available |

Response JSON:

| Parameters | Type      | Comments                                                     |
| ---------- | --------- | ------------------------------------------------------------ |
| status     | String    | return code: <br />**100**: successful, <br />**103**: parameter error <br />**104**: invalid token<br />**111**: For some other errors, refer to the "msg" value. |
| msg        | String    | Error message                                                |
| data       | JSONArray | **agentCondition**: online/offline status, <br />     0--offline <br />     1--online <br />**deviceList**: devices that belong to the gateway <br />**serialNumber**: agent serial number |

```
{
    "status":"100",
    "data":[
        {
            "agentCondition":0,
            "deviceList":[
                {
                    "condition":0,
                    "deviceId":1437705215,
                    "deviceName":"ra-device",
                    "serialNumber":"1404008"
                }
            ],
            "protocol":"mqtt",
            "serialNumber":1404008
        }
    ]
}
```

# 20. Get agent configuration

Function: Get the configuration information of gateway registration

Request type: GET

url: /agent

Prameters:

| Parameters   | Type    | Required | Comment                                        |
| ------------ | ------- | -------- | ---------------------------------------------- |
| token        | String  | Yes      | User token. Both types of tokens are available |
| serialNumber | Integer | Yes      |                                                |

Response JSON:

| Parameters | Type      | Comments                                                     |
| ---------- | --------- | ------------------------------------------------------------ |
| status     | String    | return code: <br />**100**: successful, <br />**103**: parameter error <br />**104**: invalid token <br />**111**: For some other errors, refer to the "msg" value. |
| msg        | String    | Error message                                                |
| data       | JSONArray | **agent_name**: agent name <br />**agentxml**: ModuleConfig.xml content agent uploads when it register to AnylinkCLoud. Detailed introduction of ModuleConfig.xml configuration [click here](https://github.com/tetrascience/ts-anylink-shared/blob/master/Documents/Configuration/ModuleConfig.xml-description.pdf) <br />**condition**: online/offline status, 0--offline, 1--online <br />**createtime**: The first time(ms) agent registered to AnylinkCloud <br />**id**: serial number <br />**protocol**: Data transmission protocol, e.g "http", "mqtt" <br />**updatetime**：The last time(ms) agent registered to AnylinkCloud <br />**version_detail**: agent version |

```
{
    "status":"100",
    "data":{
        "agent_name":"Agent-1701178",
        "agentxml":"<agent>......</agent>",
        "anylink_model":"DA",
        "condition":0,
        "createtime":1609294261277,
        "id":1701178,
        "protocol":"mqtt",
        "updatetime":1627177971998,
        "version_detail":"3.7.17"
    }
}
```

# The following are `device-user` related API (21, 22, 23)

You should use [1. Get token for AnylinkCloud UI](https://github.com/tetrascience/ts-anylink-shared/edit/master/Documents/API%20Instructions/AnylinkCloud%20RestAPI.md#1-get-token-for-anylinkcloud-ui) to get the token when call the following APIs:

- [21. Get device list of a user](https://github.com/tetrascience/ts-anylink-shared/edit/master/Documents/API%20Instructions/AnylinkCloud%20RestAPI.md#21-get-device-list-of-a-user)
- [22. Associate devices to a user](https://github.com/tetrascience/ts-anylink-shared/edit/master/Documents/API%20Instructions/AnylinkCloud%20RestAPI.md#22-associate-devices-to-a-user)
- [23. Remove device from user](https://github.com/tetrascience/ts-anylink-shared/edit/master/Documents/API%20Instructions/AnylinkCloud%20RestAPI.md#23-remove-device-from-user)

## 21. Get device list of a user

 Function: Get device list bound to a user

 Request type: GET

 url: `/userDevice/listByPagination`

 Prameters:

| Parameters   | Type    | Required | Comment                                                      |
| ------------ | ------- | -------- | ------------------------------------------------------------ |
| token        | String  | Yes      | User token (AnylinkCloud UI token)                           |
| userId       | Integer | No       | The `userId` to get the device list. If `userId` is null, it will be the id of the user corresponding to the `token`. |
| serialNumber | Integer | No       | Anylink serial number                                        |
| deviceName   | String  | No       | device name                                                  |
| page         | Integer | Yes      | Page number, starting from 1                                 |
| perPage      | Integer | Yes      | Number of data per page                                      |

 Response JSON:

| Parameters | Type       | Comments                                                     |
| ---------- | ---------- | ------------------------------------------------------------ |
| status     | String     | return code: <br />**100**: successful, <br />**103**: parameter error <br />**104**: invalid token <br />**111**: For some other errors, refer to the "msg" value. |
| msg        | String     | Error message                                                |
| result     | JSONObject | `pageInfo`  <br />     `page` Page number, starting from 1   <br />     `perPage` Number of data per page   <br />     `total` Total number of data pieces <br />`data` JSONArray   <br />     `id`    <br />     `device_id` AnylinkCloud device id   <br />     `name` Device name   <br />     `serialnumber` Anylink serial number |

```
{
    "status": "100",
    "result": {
        "pageInfo": {
            "page": 1,
            "perPage": 10,
            "total": 3
        },
        "data": [
            {
                "id": 3,
                "device_id": 1535998977,
                "name": "Monitor_Test",
                "serialnumber": "1499999"
            }
        ]
    }
}
```

## 22. Associate devices to a user

 Function: Associate devices to a user

 Request type: POST

 url: `/userDevice/add`

 Prameters:

| Parameters | Type    | Required | Comment                                                      |
| ---------- | ------- | -------- | ------------------------------------------------------------ |
| token      | String  | Yes      | User token (AnylinkCloud UI token)                           |
| userId     | Integer | Yes      | The `userId` to bind the device list.                        |
| deviceIds  | String  | Yes      | AnylinkCloud device id. Multiple values are separated by commas. |

 Response JSON:

| Parameters | Type    | Comments                                                     |
| ---------- | ------- | ------------------------------------------------------------ |
| status     | String  | return code: <br />**100**: successful<br />**103**: parameter error <br />**104**: invalid token <br />**111**: For some other errors, refer to the "msg" value. |
| msg        | String  | Result message                                               |
| data       | Integer | When the number of bound devices is greater than 10, it indicates the number of successfully bound devices. |

```
{
    "status": "100",
    "data": "15"
}
```

## 23. Remove device from user

Function: Remove device from a user

 Request type: GET

 url: `/userDevice/deleteByUserIdAndDeviceId`

 Prameters:

| Parameters | Type    | Required | Comment                               |
| ---------- | ------- | -------- | ------------------------------------- |
| token      | String  | Yes      | User token (AnylinkCloud UI token)    |
| userId     | Integer | Yes      | The `userId` to bind the device list. |
| deviceId   | Integer | Yes      | AnylinkCloud device id.               |

 Response JSON:

| Parameters | Type    | Comments                                                     |
| ---------- | ------- | ------------------------------------------------------------ |
| status     | String  | return code: <br />**100**: successful <br />**103**: parameter error <br />**104**: invalid token <br />**111**: For some other errors, refer to the "msg" value. |
| msg        | String  | Error message                                                |
| data       | Integer | Number of devices successfully unbound                       |

```
{
    "status": "100",
    "data": "1"
}
```

## 24. Get device list

Function: Get device list

 Request type: GET

 url: `/devicelist`

 Prameters:

| Parameters   | Type    | Required | Comment                                                      |
| ------------ | ------- | -------- | ------------------------------------------------------------ |
| token        | String  | Yes      | User token. Both types of tokens are available               |
| hash         | String  | No       | 'tetrascience'                                               |
| serialNumber | Integer | No       | AnyLink box serial number. If it is null, API will return all the devices in permission of this token. |

 Response JSON:

| Parameters | Type      | Comments                                                     |
| ---------- | --------- | ------------------------------------------------------------ |
| status     | String    | return code: <br />**100**: successful <br />**103**: parameter error <br />**104**: invalid token <br />**111**: For some other errors, refer to the "msg" value. |
| data       | JSONArray | `id`:  device ID<br/>`name`: device name<br/>`serialNumber`: device serial number<br/>`deviceAttributes` device attributes<br>`lastContact`: last contact time,  time string(GMT-4)<br/>`lastRegister`: agent last registration time, time string(GMT-4)<br/>`pingRate` not in use<br>`deviceCondition`: device condition，1--device is uploading data，0/null--device is not uploading data within "5*data frequency"<br/>`description` some description infomation<br>`channel` device channel for Anylink SE <br>`channelName` device channel name for Anylink SE<br>`isActive` not in use<br>`protocol` not in use<br>`userGroupName` not in use<br>`userGroupId` not in use<br>`version`: agent version<br/>`vpnVersion`: vpn version supported in the agent<br/>`deviceModel`: <br/>      `id: `device model ID<br/>      `name`: device model name<br>      `alias`:  device model alias<br>      `manufacturer`: not in use<br>      `description`: some description infomation |



```
{
    status: "100",
    data: [
       {
            "id": 1441802239,
            "name": "Kallyope-014-system",
            "serialNumber": "1408009",
            "deviceAttributes": null,
            "lastContact": "2020-09-25 17:50:00.0",
            "lastRegister": "2020-09-25 17:26:59.632027",
            "pingRate": 0,
            "deviceCondition": 0,
            "description": null,
            "channel": null,
            "channelName": null,
            "isActive": 1,
            "protocol": null,
            "userGroupName": null,
            "userGroupId": null,
            "version": "3.7.5",
            "deviceModel": {
                "id": 2,
                "name": "ra-model",
                "alias": null,
                "manufacturer": null,
                "description": null
            }
        },
        …
      ]
   }
```



## 25. Get user ID by user name

Function: Get user ID

 Request type: GET

 url: `/user/findByUsername`

 Prameters:

| Parameters  | Type   | Required | Comment                                                      |
| ----------- | ------ | -------- | ------------------------------------------------------------ |
| token       | String | Yes      | User token, got from API `/user/getToken` (AnylinkCloud UI token) |
| tenantEname | String | Yes      | tenant name                                                  |
| loginName   | String | Yes      | user name                                                    |

 Response JSON:

| Parameters | Type       | Comments                                                     |
| ---------- | ---------- | ------------------------------------------------------------ |
| status     | String     | return code: <br />**100**: successful <br />**103**: parameter error <br />**104**: invalid token <br />**109**: username does not exist<br />**111**: For some other errors, refer to the "msg" value. |
| data       | JSONObject | `cellphone`:  celphone number <br/>`created_by`: creator ID <br/>`created_on`: created time: Unix time in ms <br/>`email`: email <br/>`id`: userId <br/>`isadmin`: 1: administrator，2: maintenance user，0: regulator user<br/>`last_login_time`: last login time in Unix time in ms<br/>`real_name`: full name<br/>`status`: status，1 is active，0 is disabled<br/>`tenant_name`: tenant name<br/>`type`: 0 is user，1 is department<br/>`updated_by`: updator ID<br/>`updated_on`: updated time in Unix time in ms<br/>`user_name`: user name |



```
   {
       "status": "100",
       "data": {
           
       }
   }
   {
       "status": "100",
       "data": {
           "cellphone": "1234",
           "created_by": 1,
           "created_on": 1597680000000,
           "email": "test",
           "id": 2,
           "isadmin": 1,
           "last_login_time": 1633536000000,
           "real_name": "test",
           "status": 1,
           "tenant_name": "AnyLink",
           "type": 0,
           "updated_by": 1,
           "updated_on": 1597680000000,
           "user_name": "test"
       }
   }
```

## 26. Get OTA file list

Function: Get OTA file list uploaded to AnylinkCloud

 Request type: GET

 url: `/ota/OTAVersionList`

 Prameters:

| Parameters | Type   | Required | Comment                                        |
| ---------- | ------ | -------- | ---------------------------------------------- |
| token      | String | Yes      | User token. Both types of tokens are available |

 Response JSON:

| Parameters | Type      | Comments                                                     |
| ---------- | --------- | ------------------------------------------------------------ |
| status     | String    | return code: <br />**100**: successful <br />**103**: parameter error <br />**104**: invalid token <br />**111**: For some other errors, refer to the "msg" value. |
| msg        | String    | Error message                                                |
| data       | JSONArray | `currentVersion` The version of agent **before** OTA upgrade<br />`newVersion` Version number of agent **after** OTA upgrade <br />`fileName` File name of OTA upgrade package <br />`fsign` MD5 hash value of file of OTA upgrade package <br />`createTime` Creation time (UNIX time in ms) of this data <br />`updateTime` Last update time (UNIX time in ms) |

```
{
    "status": "100", 
    "data": [
        {
            "createTime": 1556446121094,
            "currentVersion": "3.7.4",
            "fileName": "agent-hf-3.7.4.zip",
            "fsign": "ZRhLoZDbflPiRyYelX0f4w==",
            "id": 1,
            "newVersion": "3.7.4",
            "updateTime": 1556446121094
        }
    ]
}
```

## 27. OTA Pre-Check

Function: Before initiating OTA, check whether the gateway supports OTA

Request type: POST

url: `/ota/preCheck`

Parameters:

| Parameters    | Type      | Required | Comment                                        |
| ------------- | --------- | -------- | ---------------------------------------------- |
| token         | String    | Yes      | User token. Both types of tokens are available |
| serialNumbers | JSONArray | Yes      | Anylink serial numbers                         |

Request parameter example:

```
{
	"token": "",
	"serialNumbers":[1200001,1200002]
}
```

Response JSON:

| Parameters | Type       | Comments                                                     |
| ---------- | ---------- | ------------------------------------------------------------ |
| status     | String     | return code: <br />**100**: successful <br />**103**: parameter error <br />**104**: invalid token <br />**111**: For some other errors, refer to the "msg" value. |
| msg        | String     | Error message                                                |
| data       | JSONObject | `NO` Not meeting OTA upgrade conditions <br />`reason` The reason why OTA cannot be performed. It will be null if the Anylink can perform OTA <br />`condition` 0--AnylinkBox online, 1--AnylinkBox offline <br />`serialNumber` Anylink serial number <br />`anylinkModel` Anylink model, such as `DA` `SE` `IE` `IE Pro` <br />`currentVersion` Current version of agent <br />`OK` List that have passed the pre-check |

```
{
    "status":100,
    "data":{
        "OK":[
            {
                "serialNumber":1200001,
                "currentVersion":"3.1.6",
                "anylinkModel":"DA",
                "condition":1
            }
        ],
        "NO":[
            {
                "serialNumber":1200003,
                "currentVersion":"3.1.6",
                "anylinkModel":"DA",
                "condition":0,
                "reason":"OTA is supported since Agent 3.7.4"
            }
        ]
    }
}
```

## 28. Get the list of upgradeable versions

Function: Get the list of upgradeable versions

Request type: GET

url: `/ota/optionalVersions`

Parameters:

| Parameters   | Type    | Required | Comment                                                      |
| ------------ | ------- | -------- | ------------------------------------------------------------ |
| token        | String  | Yes      | User token. Both types of tokens are available               |
| serialNumber | Integer | No       | Anylink serial number. If it is null, API will return all optional versions that have uploaded to server. |

Request parameter example:

```
{
	"token": "",
	"serialNumber": 1200001
}
```

Response JSON:

| Parameters | Type      | Comments                                                     |
| ---------- | --------- | ------------------------------------------------------------ |
| status     | String    | return code: <br />**100**: successful<br />**103**: parameter error <br />**104**: invalid token <br />**111**: For some other errors, refer to the "msg" value. |
| msg        | String    | Error message                                                |
| data       | JSONArray | `currentVersion` The version of agent **before** OTA upgrade <br />`newVersion` Version number of agent **after** OTA upgrade |

```
{
    "status":"100",
    "data":[
        {
            "currentVersion":"3.7.4",
            "newVersion":"3.7.5"
        },
        {
            "currentVersion":"3.7.4",
            "newVersion":"3.7.6"
        },
        {
            "newVersion":"latest"
        }
    ]
}
```

## 29. Start OTA for an AnylinkBox

Function: Start OTA for an AnylinkBox

Request type: POST

url: `/ota/startOTA`

Parameters:

| Parameters    | Type    | Required | Comment                                        |
| ------------- | ------- | -------- | ---------------------------------------------- |
| token         | String  | Yes      | User token. Both types of tokens are available |
| serialNumber  | Integer | Yes      | Anylink serial number                          |
| targetVersion | String  | Yes      | Target version number to upgrade to via OTA    |

Request parameter example:

```
{
    "token":"b06b512b-c377-48a4-b3fd-d59bb033bb9d",
    "serialNumbers":[
        {
            "serialNumber": 1500001,
            "targetVersion": "3.7.20"
        }
    ]
}
```

Response JSON:

| Parameters | Type       | Comments                                                     |
| ---------- | ---------- | ------------------------------------------------------------ |
| status     | String     | return code: <br />**100**: successful <br />**103**: parameter error <br />**104**: invalid token <br />**111**: For some other errors, refer to the "msg" value. |
| msg        | String     | Error message                                                |
| data       | JSONObject | `NO` Not meeting OTA upgrade conditions <br />`OK` Ota is successfully initiated and the value is `sessionid` |

```
{
    "status": "100",
    "data": {
        "NO": {
            "1400219": false
        },
        "OK": {
            "1400218": "1636342247983"
        }
    }
}
```

## 30. Get OTA status

Function: Get OTA status

Request type: GET

url: `/ota/downloadStatus`

Parameters:

| Parameters   | Type    | Required | Comment                                        |
| ------------ | ------- | -------- | ---------------------------------------------- |
| token        | String  | Yes      | User token. Both types of tokens are available |
| serialNumber | Integer | Yes      | Anylink serial number                          |
| sessionid    | String  | Yes      | `sessionid` returned by `/ota/startOTA` API    |

Response JSON:

| Parameters | Type       | Comments                                                     |
| ---------- | ---------- | ------------------------------------------------------------ |
| status     | String     | return code: <br />**99**: This OTA instance is not exist.<br />**100**: successful <br />**103**: parameter error <br />**104**: invalid token <br />**111**: For some other errors, refer to the "msg" value. |
| msg        | String     | Error message                                                |
| data       | JSONObject | `serialNumber` Anylink serial number <br />`oldVersion` The version of agent **before** OTA upgrade <br />`sessionid` returned by `/ota/startOTA` API <br />`startTime` OTA start time <br />`cmd` The command sent to agent <br />`newVersion` Version number of agent **after** OTA upgrade <br />`status` Current OTA status <br />`statusCode` Current OTA status code |

```
{
    "status": "100",
    "data": {
        "serialNumber": 1400219,
        "oldVersion": "3.7.20",
        "sessionid": "1636351404453",
        "startTime": 1636351406348,
        "cmd": "{\"fsign\":\"7acxVMKd2cK7NwvamX5Edw==\",\"file\":\"OTA-DA-Agent-3.7.21.zip\",\"nblock\":149,\"fsize\":2432576,\"csign\":\"L73XQWVbI2+TdPcoc91td7gRj9mAG2zTFbLUGSuoSeCDqG0Yly29AcT2V/KLsc/t4pOMWiXRq93pu9dPZDiGQVW5N1YpgPaerrt12tLQvPQetDNwF2Zy0FwUIUgkrolrqOTJ2vbgjbPtHwmcgN2OnDudCoos5oAwa5PIURja0uw=\",\"sessionid\":\"1636351404453\",\"type\":0}",
        "newVersion": "3.7.21",
        "status": "OTA_DOWNLOAD_CMD_PUBLISHED",
        "statusCode": 1
    }
}
```

OTA status code:

| code | status                                    |                                                              |
| ---- | ----------------------------------------- | ------------------------------------------------------------ |
| 0    | AGENT_OTA_STATUS_WAITING                  | The OTA command is waiting to sent                           |
| 1    | OTA_DOWNLOAD_CMD_PUBLISHED                | The OTA command has been sent to agent                       |
| 2    | AGENT_OTA_UPDATE                          | The agent has returned the status of whether it can be updated |
| 3    | AGENT_OTA_DOWNLOADING_FILE                | OTA file blocks are being sent                               |
| 4    | AGENT_OTA_DOWNLOAD_FINISHED_WAITING_CHECK | OTA file distribution is completed, waiting for agent verification |
| 5    | AGENT_OTA_DOWNLOAD_FINISHED               | OTA file verification is completed, and agent is performing upgrade |
| 6    | AGENT_OTA_FINISHED                        | OTA process completed                                        |

## 31. Add user

Function: Add a user

Request type: POST

url: `/user/addUser`

Parameters: JSON

This API will parse the payload and only pickup the fields listed below and discard the others which are not mentioned in the following list. 

| Parameters  | Type       | Required | Comment                                          |
| ----------- | ---------- | -------- | ------------------------------------------------ |
| token       | String     | Yes      | User token. Both types of tokens are available   |
| param       | JSONObject | Yes      |                                                  |
| user_name   | String     | Yes      | User name, used to login                         |
| password    | String     | Yes      | Password should be between 5-16 characters       |
| re_password | String     | Yes      | Enter the password again                         |
| real_name   | String     | Yes      | Real name                                        |
| parent_id   | Integer    | No       | User's department id                             |
| cellphone   | String     | Yes      |                                                  |
| email       | String     | No       |                                                  |
| telephone   | String     | No       |                                                  |
| isadmin     | Integer    | No       | 0 -- ordinary admin, 1-- administrator           |
| type        | Integer    | Yes      | User type, 0 -- add a user, 1-- add a department |

Request parameter example:

```
{
    "token": "5e2719d6-6556-4fa4-a536-8106a392354e",
    "param": {
        "user_name": "s2",
        "password": "12345678",
        "re_password": "12345678",
        "real_name": "s1",
        "parent_id": "1",
        "cellphone": "123456",
        "email": "gfdgvdf@dfgdfg.dfg",
        "telephone": 43566212344,
        "undefined": "435662123dfg",
        "isadmin": "0",
        "type": 1
    }
}
```

Response JSON:

| Parameters | Type    | Comments                                                     |
| ---------- | ------- | ------------------------------------------------------------ |
| status     | String  | return code: <br />**100**: successful <br />**103**: parameter error <br />**104**: invalid token <br />**111**: For some other errors, refer to the "msg" value.<br>**116**: password mismatch<br>**110**: duplicate user |
| msg        | String  | Error message                                                |
| data       | Integer | Newly added user id                                          |


## 32. List all the departments

Function: List all the departments

Request type: GET

url: `/user/getTenantUserTree`

Parameters: 

| Parameters | Type       | Required | Comment                                                      |
| ---------- | ---------- | -------- | ------------------------------------------------------------ |
| token      | String     | Yes      | User token, got from API `/user/getToken` (AnylinkCloud UI token) |
| userType   | Integer | Yes      | The value is **1**. It means list the department.            |

Response JSON:

| Parameters | Type      | Comments                                                     |
| ---------- | --------- | ------------------------------------------------------------ |
| status     | String    | return code: <br />**100**: successful <br />**103**: parameter error <br />**104**: invalid token <br />**111**: For some other errors, refer to the "msg" value. |
| msg        | String    | Error message                                                |
| data       | JSONArray | `created_by` The user id who created this department<br>`created_on` Create time, UNIX time in ms<br>`id` The department id<br>`isadmin`  If this is a user but not department, 0 means ordinary user, 1 means administrator<br>`real_name` Department name<br>`remark` remark<br>`status` 0--disable, 1--enable<br>`type` 0-- user, 1--department<br>`updated_by` User id who last updated this department<br>`updated_on` Last updated time, UNIX time in ms |

Response example: 

```json
{
    "status": "100",
    "data": [
        {
            "created_by": 1,
            "created_on": 1642651200000,
            "id": 3,
            "isadmin": 0,
            "real_name": "It Department",
            "remark": "",
            "status": 1,
            "type": 1,
            "updated_by": 1,
            "updated_on": 1642651200000
        }
    ]
}
```
