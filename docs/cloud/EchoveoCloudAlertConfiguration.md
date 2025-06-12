# 1. Set up alarm rules in CloudWeb

  **Settings -> Gateway Management -> Remote Manage**

  - Click **Upload Gateway Configuration** – this forces the gateway to upload its current config file.

  - Next, navigate to **Open Saved Configuration**

   ![1749554342664](https://github.com/user-attachments/assets/3fd6541b-a297-4646-9da5-51ec29b68417)

![1749553854410](https://github.com/user-attachments/assets/2d07167d-e062-4c22-b77f-638a948783b1)



![1749554221735](https://github.com/user-attachments/assets/1d138624-6dde-4b87-a87c-7759d8d2b1e0)



In the **Alarms** tab, you can modify existing alarm rules or create new ones.

After modifying or adding an alarm rule, click the **Save** button in the upper-right corner of the page. Note that this only saves the configuration on the server side. You must then click **Deploy** to push the configuration to the edge device.




  # 2. View alarms in CloudWeb

  ## Alarm rules

  ![image-20250430103727595](https://github.com/user-attachments/assets/345cea9d-f473-4fa9-961c-e58267b6abcf)


  ![image-20250430103928448](https://github.com/user-attachments/assets/70110a37-17ae-4a40-b2d6-35c03bb789ee)


  ## Current Alarms

  ![image-20250430104131997](https://github.com/user-attachments/assets/a1c93161-b6bc-4300-99bf-825ad1f2ffcb)


  ## Historical alarms

  ![image-20250430104233774](https://github.com/user-attachments/assets/6b7e0a11-aada-4834-88c2-0f3185b053ec)



  ## Configure email notification for alarms

  1. Set user's email address

     ![image-20250430104716281](https://github.com/user-attachments/assets/113fcb0f-0ca1-437f-a040-adecc0fd5e1f)


  2. Bind devices to users, so they only receive alarm notifications from their bound devices.

     **Access Control -> Device Access Control**

     ![image-20250430104827304](https://github.com/user-attachments/assets/4f21708c-5d92-4aea-a065-58c19bb94a91)

      ![image-20250430104940441](https://github.com/user-attachments/assets/6c020a43-1656-4a2b-be06-915c7dc09b64)

 - Select the target user from the left panel

 - Check the corresponding device checkbox

 - Click the icon on the right side



# 3. Configure alarm rules in ModuleConfig.xml

## XML configuration file description

In addition to configuring alarm rules on the web page, you can also manually modify the XML configuration file. But this requires combining RestAPI to deploy the XML configuration file into the box.

Here we first introduce the formats related to alarm rules in XML.

```xml
<model n="CO2" id="2" d="IDrv.Custom:libDModbus" config="rtu;/dev/ttyUSB0;9600;None;8;1;STANDARD;2000;100;20" devicedriver="Modbus-RTU">
    <device n="CO2" id="2" ip="192.168.1.1" type="test">
        <driver n="IDrv.Custom:libDModbus" config="rtu;/dev/ttyUSB0;9600;None;8;1;STANDARD;2000;100;20" id="1">
            <commDataItems>
                <dataItem id="1" n="CO2PPM" alias="CO2PPM" config="" type="a" rw="0" freq="10000" report="1"/>
                <dataItem id="2" n="humidity" alias="humidity" config="" type="a" rw="0" freq="10000" report="1"/>
                <dataItem id="3" n="temperature" alias="temperature" config="" type="a" rw="0" freq="10000" report="1"/>
            </commDataItems>
        </driver>
        <Rules>
            <rule id="1" name="CO2">
                <Triggers>
                    <trigger name="demo" type="1" relation="1&amp;(2|3)" >
                        <di id="1" name="${dataItem.name}" opr="" opd="" dep="" />
                        <di id="2" name="humidity" opr="" opd="" dep="" />
                        <di id="3" name="temperature" opr="" opd="" dep="" />
                    </trigger>
                </Triggers>
                <Actions>
                    <action alarm="CO2PPM" ctrl_item="" ctrl_switch="0" ctrl_value="" descr="CO2PPM,$0" name="CO2PPM" severity="8" type="1"/>
                </Actions>
            </rule>
        </Rules>
    </device>
</model>
```

- Add `Rules/rule/Triggers` and `Rules/rule/Actions` in the `model/device` module.

- tags: 

  - `rule.id` must be unique within the `device` scope.

  - `rule.name` Alarm rule name

  - `trigger`

    - `trigger.relation` relations between `<di>` tags, has `&, |, (, )`  
      1,2,3... -> `di.id`  
      The `&` character should be represented as `&` in XML generation.  

    - Set `trigger.type` to a fixed value of 1, indicating a date item trigger.

  - `di` 

    - `dep` depend relation, used to group items,  group item rules may be need a key item.

    - `id` index

    - `name` corresponds to the data item name `dataitem.name`, such as `CO2PPM`

    - `opd` alarm threshold value. When the corresponding `dataItem` reaches this threshold, an alarm is triggered. For boolean types, valid values are `0 or 1`

    - `opr` numeric operator codes with corresponding relationships as follows:

      |      |             |
      | ---- | ----------- |
      | 1    | include     |
      | 2    | ==          |
      | 3    | !=          |
      | 4    | ==          |
      | 5    | !=          |
      | 6    | >=          |
      | 7    | >           |
      | 8    | <=          |
      | 9    | <           |
      | 10   | >           |
      | 11   | <           |
      | 12   | not include |

  - `action`

    - `name` action name
    - `type` action type, 1->send alarm
    - `alarm` alarm name
    - `severity` alarm severity, currently supports `8, 9, 10, 11, 12`, which correspond to `Level 1, Level 2, Level 3, Level 4, Notification` on the page respectively.
    - `descr` alarm description. The suffix `$0` indicates that the alarm timestamp and current data value will be automatically appended when uploading the alarm description

## Deploy configuration files to the box through RestfulAPI
Reference Python script file: https://github.com/echoveo/NeuroQ/blob/main/docs/cloud/deployConfig-RestfulAPI.py
Sample XML configuration file: https://github.com/echoveo/NeuroQ/blob/main/docs/cloud/1801702.xml

