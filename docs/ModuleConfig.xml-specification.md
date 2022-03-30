![logo2](https://user-images.githubusercontent.com/76909130/153789287-58f516ff-ed97-45cc-8d8c-426956d27f84.png)

# AnyLink IoT Agent ModuleConfig.xml Specification

Version 3.0.1  
March 14th, 2022

# 1. Terminology  
**Driver:** Driver is a dynamically loaded component (.so file in Linux) of AnyLink IoT agent, which is responsible for communicating with field devices. There&#39;re two types of drivers in AnyLink IoT agent, one is task driver and the other is normal driver. The difference is that one instance of normal driver can only process data for one device, while one instance of task driver can process data for multiple devices.

**Driver version:** Starting from agent version 3.7.21, we introduced a new feature which agent automatically downloads a specific version of driver from the AnyLink cloud if the driver is not present in the AnyLinkIoT box. This feature requires configuration of attribute `version` in the `driver` element. If attribute `version` is not configured, agent will NOT automatically download driver from AnyLink Cloud even if the driver is not present in the box.

**ra-model** and **ra-device**: This device is configured by AnyLink as a default, which is used to report system information (i.e. uptime, WiFi related information, etc). This is a device represent the IoT box itself and it should be not removed. The task drivers configured in the <task> element by default are the essential drivers for IoT agent to work and they should not be removed.

**Device id**: `id` attribute in `<device>` element (we call it 'agent_device_id') is the unique identification for each device within the IoT agent. AnyLink Cloud will use this value to create `deviceId` in the AnyLink Cloud. Here's the algorithm to generate `deviceId`:  
```
IoTBox-SerialNumber * 1024 + agent_device_id
```

# 2. ModuleConfig.xml (Factory Default Configuration)
The values inside "{{ }}" will vary between different boxes and releases.

```xml
<agent flag="SET-TASKS" id="{{IoTBox-SerialNumber}}" n="Agent-{{IoTBox-SerialNumber}}" port="-1" script="{{script_version}}" sdmwebs="{{webUI_version}}" timezone="UTC">
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
          <dataItem addr="" config="" freq="120000" id="18" n="MEMORY" report="1" rw="0" type="s" vtype=""/>  
          <dataItem addr="" config="" freq="120000" id="19" n="STORAGE" report="1" rw="0" type="s" vtype=""/>  
          <dataItem addr="" config="" freq="120000" id="22" n="WIFI-TYPE" report="1" rw="0" type="s" vtype=""/>  
          <dataItem addr="" config="" freq="120000" id="23" n="WIFI-HIDDEN" report="1" rw="0" type="s" vtype=""/>
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
    <TaskDriver>
      <driver config="1" n="T.IDrv.Task:libtremoteplc"/>
    </TaskDriver>  
  </task>  
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
|                                                  | type          | No           | type of device |
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
|                                                  | type          | Yes          | Data item type:<br>&#39;a&#39; is numerical value (i.e. BYTE, WORD, DWORD, FLOAT, uint8, int8, uint16, int16, uint32, int32, etc); <br>&#39;b&#39; is Boolean; <br>&#39;s&#39; is string |
|                                                  | vtype         | Yes          | Reserved                                                     |


# 3. Sample template ModuleConfig.xml to add a new device
Bellow is a sample configuration file to add a new device with libTModbus driver. Please replace parameters in "{{ }}" with real value.

```xml
<agent flag="SET-TASKS" id="{{IoTBox-SerialNumber}}" n="{{Agent-Name}}" port="-1" script="1.1.0" sdmwebs="1.1.0" timezone="UTC">
  <model n="{{Model-Name}}">
    <device n="{{DeviceName}}" id="3" ip="192.168.1.1" type="test">
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
    <TaskDriver>
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
          <dataItem addr="" config="" freq="120000" id="18" n="MEMORY" report="1" rw="0" type="s" vtype=""/>  
          <dataItem addr="" config="" freq="120000" id="19" n="STORAGE" report="1" rw="0" type="s" vtype=""/>  
          <dataItem addr="" config="" freq="120000" id="22" n="WIFI-TYPE" report="1" rw="0" type="s" vtype=""/>  
          <dataItem addr="" config="" freq="120000" id="23" n="WIFI-HIDDEN" report="1" rw="0" type="s" vtype=""/>
        </commDataItems>
      </driver>
    </device>
  </model>
</agent>
```


# 4. MQTT configuration


```xml
<TaskDriver>
	<driver n="T.IDrv.Task:libkmqtt" config="192.168.100.102;8883;192.168.100.102;8883;60;2;0;0;admin;public;;1;" />
</TaskDriver>
```

 The items in config are as follows：
 **note** if the value is not required, fill in empty string in the place. username and password are configured based on MQTT server configuration.  

phost;pport;shost;sport;keepalive;qos;retain;bencode;user;password;bindaddr;btls;

|           | **Comments**                                        |**Required**| **Recommended value**      |
| --------- | --------------------------------------------------- |------------| -------------------------- |
| phost     | MQTT server address                                 |Yes|                            |
| pport     | MQTT server port                                    |Yes| TLS：8883<br>Non TLS：1883 |
| shost     | MQTT server address                                 |Yes|                            |
| sport     | MQTT server port                                    |Yes| TLS：8883<br>Non TLS：1883 |
| keepalive | time（use default value）                           |Yes| 60                         |
| qos       | Message quality (use default value)                 |Yes| 2                          |
| retain    | Retain value of MQTT message                        |Yes| 0                          |
| bencode   | User name and password encryption，0-None，1-base64 |Yes| 0                          |
| user      | SSL username                                       |No|                            |
| password  | SSL password                                        |No|                            |
| bindaddr  | empty string                                          |No| empty string                 |
| btls      | Whether open TLS                                    |Yes| 1 -- TLS<br>0 -- Non TLS   |

# 5. Update ModuleConfig.xml
## 5.1 using AnyLink Cloud API

Use AnyLink Cloud API /remoteAgent/sendAnylinkXML (please refer to AnyLink Cloud REST API doc for detail) to update the ModuleConfig.xml in the IoT box.  
Once IoT agent receives the updated the configuration file, it will automatically restart IoT agent (not rebooting the whole system) and load the new configuration file.

## 5.2 Update ModuleConfig.xml manually using SSH

It's always recommended to use AnyLink Cloud API to update configuration file whenever is possible.  
1. SSH into IoT box
2. edit file /opt/agent/ModuleConfig.xml  
3. save file after done with editing
4. make a copy of the configuration file to /opt/sdmwebs/web/conf/config.xml using the following command:  
```    
cp /opt/agent/ModuleConfig.xml /opt/sdmwebs/web/conf/config.xml  
```  
5. reboot IoT box
