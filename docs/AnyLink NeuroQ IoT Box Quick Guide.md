![logo2](https://user-images.githubusercontent.com/76909130/153789287-58f516ff-ed97-45cc-8d8c-426956d27f84.png)

**AnyLink NeuroQ IoT Box Quick Guide**



# 1. Connect to IoT box via LAN port

**Step 1** : Connect your PC to LAN port on IoT box using ethernet cable  
<img src="https://www.anylinkiot.com/doc/NeuroQ-F.JPEG" width = "80" height = "343" alt="" align=center />  

**Step 2:** Plug power supply to IoT box to power on

**Step 3** : Open **http://192.168.101.204** in your browser and enter username and password (default is **admin/admin** )

**Step 4** : Click **Advanced-\&gt;Agent Config** to configure AnyLink Cloud address in **MQTT Publish** and **MQTT Subscription section** and click **Save** button at the bottom once finished.  
<img src="https://www.anylinkiot.com/doc/neuroq-ui1.png" width = "440" height = "250" alt="" align=center />

**Step 5** : Click **Advanced-\&gt;Network Config** to configure your network connection to AnyLink Cloud. Select **Ethernet** if you use **WAN** port on IoT box to connect to AnyLink Cloud, or select **WiFi** if you use WiFi to connect to AnyLink Cloud. If network connection is correct, the upper right corner **Cloud Connection** status will be displayed as **Connected**.  
<img src="https://www.anylinkiot.com/doc/neuroq-ui2.png" width = "440" height = "250" alt="" align=center />

**Step 6:** Login to AnyLink Cloud to make sure your IoT box is registered in the Cloud. You can find serial number of the IoT box on the back side of the box.  
<img src="https://www.anylinkiot.com/doc/NeuroQ-B.JPEG" width = "80" height = "343" alt="" align=center />  
# 2. Configure IoT box to communicate with instrument

Once you connect your IoT box to the AnyLink Cloud, you can deploy configuration file from AnyLink Cloud to IoT box via rest API.

## 2.1 Sequence diagram

<img src="https://www.anylinkiot.com/doc/neuroq-seq.png" width = "400" height = "175" alt="" align=center />

## 2.2 Process description

1. Use the API /remoteAgent/sendAnylinkXML (**please refer   [AnyLink Cloud REST API](https://anylinkiot.com/doc/AnylinkCloud%20RestAPI.md) for details**) to send the xml configuration file to anylink
2. After anylink receives the xml configuration file, it needs to restart to load the new configuration
3. After anylink restarts, it will reregister to Anylink cloud
4. Call the interface /agent/register (**please refer   [AnyLink Cloud REST API](https://anylinkiot.com/doc/AnylinkCloud%20RestAPI.md) for details**) for details) to query the registration result of anylink. If anylink is reregistered successfully, it means the xml file be sent successfully and the whole process will end.

## 2.3 Sample code (JAVA)

```java
private final String BASE_URL = "http://staging.anylink.io:8600";

@Test
public void sendModuleConfigTest()
{
    String url = BASE_URL + "/remoteAgent/sendAnylinkXML";
    JSONObject param = new JSONObject();
    param.put("token", "0293bd56-af76-449c-8f5d-1dcfe4772dc0");
    param.put("filetype", "config_xml");
    param.put("serialnumber", 1401868);
    param.put("content", "<agent n=\"Agent-1401868\" id=\"1401868\" flag=\"SET-TASKS\" port=\"-1\" timezone=\"UTC\" version=\"3.6.6\">\n" +
            "  <model n=\"ra-model\">\n" +
            "    <device n=\"ra-device\" id=\"1023\" ip=\"127.0.0.1\">\n" +
            "      <driver n=\"T.IDrv.Task:libtremoteplc\" config=\"1\">\n" +
            "        <commDataItems>\n" +
            "          <dataItem freq=\"120000\" id=\"1\" n=\"CSQ\" rw=\"0\" report=\"1\" type=\"a\" vtype=\"\" addr=\"\" config=\"\"/>\n" +
            "        </commDataItems>\n" +
            "      </driver>\n" +
            "    </device>\n" +
            "  </model>\n" +
            "  <task>\n" +
            "    <TaskDriver>\n" +
            "      <driver n=\"T.IDrv.Task:libcontrol\" config=\"10001\"/>\n" +
            "    </TaskDriver>\n" +
            "    <TaskDriver>\n" +
            "      <driver n=\"T.IDrv.Task:libtremoteplc\" config=\"1\"/>\n" +
            "    </TaskDriver>\n" +
            "    <TaskDriver>\n" +
            "      <driver n=\"T.IDrv.Task:libzigbee\" config=\"NULL;115200;8;N;1;0;1;0;0;localhost;10001;6;60;1;10000;3\"/>\n" +
            "    </TaskDriver>\n" +
            "    <TaskDriver>\n" +
            "      <driver n=\"T.IDrv.Task:libkmqtt\" config=\"40.121.212.65;1883;40.121.212.65;1883;60;2;1;0;;;;0;\"/>\n" +
            "    </TaskDriver>\n" +
            "  </task>\n" +
            "  <model n=\"test\" id=\"1\" d=\"IDrv.Custom:libDModbus\" config=\"tcp;192.168.100.38;520;200;100;20\" devicedriver=\"Modbus-TCP\">\n" +
            "    <device n=\"device\" id=\"1\" ip=\"192.168.1.1\" type=\"test\">\n" +
            "      <driver n=\"IDrv.Custom:libDModbus\" config=\"tcp;192.168.100.38;520;200;100;20\" id=\"1\">\n" +
            "        <commDataItems>\n" +
            "          <dataItem id=\"2\" n=\"a\" alias=\"a\" config=\"1;1;100;1;BOOLEAN;0;0;1\" type=\"b\" rw=\"1\" freq=\"60000\" report=\"1\"/>\n" +
            "          <dataItem id=\"3\" n=\"b\" alias=\"b\" config=\"1;1;100;1;BOOLEAN;0;0;1\" type=\"b\" rw=\"1\" freq=\"60000\" report=\"1\"/>\n" +
            "        </commDataItems>\n" +
            "      </driver>\n" +
            "    </device>\n" +
            "  </model>\n" +
            "</agent>");
    String postResult = post(url, param.toJSONString());
    JSONObject postResultJSON = JSONObject.parseObject(postResult);
    if(postResultJSON != null && postResultJSON.getInteger("status") == 100){
        System.out.println("SUCCESS");
    }else{
        System.out.println("FAILED");
    }
}

public String post(String urlStr, String messageOut) {
    HttpURLConnection httpConn = null;
    URL url = null;
    String messageIn="";
    try {
        url = new URL(urlStr);
        httpConn = (HttpURLConnection) url.openConnection();
        httpConn.setRequestMethod("POST");
        httpConn.setDoInput(true);
        httpConn.setDoOutput(true);
        httpConn.setRequestProperty("Accept-Charset", "UTF-8");
        httpConn.setRequestProperty("Content-Type", "application/json");
        @Cleanup PrintWriter out = new PrintWriter(httpConn.getOutputStream());
        out.println(messageOut);
        out.flush();

        @Cleanup InputStreamReader isReader = new InputStreamReader(httpConn.getInputStream(),"utf-8");
        @Cleanup BufferedReader bin = new BufferedReader(isReader);

        StringBuffer buff = new StringBuffer();
        String line;
        while ((line = bin.readLine()) != null) {
            buff.append(line);
        }
        messageIn = buff.toString();

    } catch (ConnectException ce) {
        ce.printStackTrace();
    }  catch (Exception e) {
        e.printStackTrace();
    }finally {
        if(httpConn!=null) {
            httpConn.disconnect();
            httpConn = null;
        }
    }
    return messageIn;
}
```
