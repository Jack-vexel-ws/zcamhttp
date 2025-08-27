
# ZCAM camera HTTP command table

The command table is based on [ZCAM official HTTP API Doc](https://github.com/imaginevision/Z-Camera-Doc/blob/master/E2/protocol/http/http.md) and Javascript [reference code](https://github.com/imaginevision/Z-Camera-Doc/blob/master/E2/protocol/http/api.js).  

## Camera 

### Utility

command | http url | response
:-----|:-----  | :----
get camera info | /info | see below json text
get camera sn | /ctrl/get?k=sn |
get commit info | /commit_info | { "mode_name": "eclipse", "git_commit": "63b23314f6", "build_time": "2503281106" }
get nick name | /ctrl/nick_name | {"name":"E2"}
camera status | /camera_status | { "isp": "OK", "sync_link": "OK", "stream0_lost_frame": 0, "https_on": false, "code": 0 }
-----------|----------  | ------
check session status | /ctrl/session
occupy the session | /ctrl/session?action=occupy
quit the session | /ctrl/session?action=quit
----------|----------  | ------
clear setting | /ctrl/set?action=clear
temperature | /ctrl/temperature |
battery_voltage | /ctrl/get?k=battery_voltage
battery | /ctrl/get?k=battery
raw over hdmi | /ctrl/get?k=raw_over_hdmi
led on/off | /ctrl/get?k=led |
desqueeze | /ctrl/get?k=desqueeze |
export profile | /prf/export

``` json
// /info response json data
{
  "cameraName": "E2_0B0333",
  "model": "eclipse",
  "number": "1",
  "sw": "1.0.10",
  "hw": "5.0",
  "mac": "9e:51:0e:b5:8f:ba",
  "sn": "615A00B0333",
  "nickName": "E2",
  "eth_ip": "192.168.1.120",
  "ip": "192.168.1.120",
  "pixelLinkMode": "Subordinate",
  "feature": {
    "product_catalog": "camera",
    "rebootAfterClearSettings": "0",
    "rebootAfterVideoSystem": "0",
    "upgradeWOCard": "1",
    "fwName": "*.zip",
    "fwCheck": "1",
    "md5Check": "1",
    "setCfgToAll": "0",
    "syncOnlyMaster": "1",
    "stopPreviewInSnap": "0",
    "stopPreviewInTimelapse": "0",
    "mfOnly": true,
    "photoSupport": "1",
    "wsSupport": "1",
    "release": true,
    "snapSupportExposureMode": "1",
    "preRoll": true,
    "pixelLink": true,
    "ezLink": true,
    "expIsoControl": true,
    "fastReadout": true,
    "audioCodecXLR": true,
    "advanceColor": true,
    "assitool": true,
    "wfm": true,
    "wifiSupport": true,
    "snapSupportFmt": {
      "isAllFmt": "1",
      "fmt": [
        "4KP23.98 (Low Noise)",
        "4KP29.97 (Low Noise)",
        "C4KP23.98 (Low Noise)",
        "C4KP29.97 (Low Noise)",
        "4KP23.98",
        "4KP29.97",
        "4KP59.94",
        ...
        ...
      ]
    },
    "timelapseSupportFmt": {
      "isAllFmt": "1",
      "fmt": [
        "4KP23.98 (Low Noise)",
        "4KP29.97 (Low Noise)",
        "C4KP23.98 (Low Noise)",
        "C4KP29.97 (Low Noise)",
        "4KP23.98",
        "4KP29.97",
        "4KP59.94",
        ...
        ...
      ]
    }
  }
}

```

### Work mode

command | http url | response
:-----|:-----  | :----
query working mode | /ctrl/mode?action=query or /ctrl/mode
switch to video record mode | /ctrl/mode?action=to_rec
switch to video playback mode | /ctrl/mode?action=to_pb
switch to standby | /ctrl/mode?action=to_standby
exit standby | /ctrl/mode?action=exit_standby

### Record

command | http url | response
:-----|:-----  | :----
batch get record settings | <font color="#ffc000">/ctrl/getbatch?catalog=record</font>
record mode | /ctrl/get?k=record_mode | `Normal` `Timelapse` |
start record | /ctrl/rec?action=start
stop record | /ctrl/rec?action=stop
get record status | /ctrl/rec?action=query
query remain recording time (minutes) | /ctrl/rec?action=remain
get repair status | /ctrl/rec?action=query_repairing
set record meta | /ctrl/set?record_meta=$value | `Enable` `Disable`
get record meta option | /ctrl/get?k=record_meta |
get camera id | /ctrl/get?k=camera_id |
set camera id | /ctrl/set?camera_id=$value |
get reel name | /ctrl/get?k=reelname |
set reel name | /ctrl/set?reelname=$value |
record format | /ctrl/get?k=record_file_format | `MP4` `MOV`
record file rotation | /ctrl/get?k=rotation|
record split duration | /ctrl/get?k=split_duration|
record frame indicator | /ctrl/get?k=rec_frame_indicator|
preroll enable | /ctrl/get?k=preroll|
preroll duration | /ctrl/get?k=preroll_duration|

### Camera Shot

command | http url | response
:-----|:-----  | :----
mov format | ctrl/get?k=movfmt
resolution | /ctrl/get?k=resolution
project fps | /ctrl/get?k=project_fps
vfr control | /ctrl/get?k=vfr_ctrl
mov vfr | /ctrl/get?k=movvfr
record fps | /ctrl/get?k=rec_fps

### Photo

command | http url | response
:-----|:-----  | :----
photo quality | /ctrl/get?k=photo_q | `JPEG` `RAW` `HEIF`
photo capture | /ctrl/still?action=cap

### Multi cam

command | http url | response
:-----|:-----  | :----
multiple cam mode | /ctrl/get?k=multiple_mode | 
union auto exposure | /ctrl/get?k=union_ae | `Enable` `Disable`
union auto white blance | /ctrl/get?k=union_awb| `Enable` `Disable`
ezlink mode | /ctrl/get?ezlink_mode | `Single` `Main` `Subordinate`
ezlink trigger | /ctrl/get?ezlink_trigger | `Auto` `Manual`
query pixel link role | /info | get `pixelLinkMode` value from response json data, 'Single' `Main` `Subordinate`

### Power

command | http url | response
:-----|:-----  | :----
shutdown | /shutdown, {timeout: 1000} |
reboot | /reboot, {timeout: 1000} |
auto off | /ctrl/get?k=auto_off |
set auto off | /ctrl/set?auto_off=$value | "Off","30s","1 min","2 min","4 min","8 min","15 min" 
auto standby | /ctrl/get?k=auto_standby |
set auto standby | /ctrl/set?auto_standby=$value | "Off","1 min","5 min","15 min"

### Time code

command | http url | response
:-----|:-----  | :----
query | /ctrl/tc?action=query |
reset tc | /ctrl/tc?action=reset |
set current | /ctrl/tc?action=current_time |
set manual | /ctrl/tc?action=set&tc=$time_code |
tc source | /ctrl/get?k=tc_source
tc count up | /ctrl/get?k=tc_count_up
tc hdmi display | /ctrl/get?k=tc_hdmi_display
tc drop frame option | /ctrl/get?k=tc_drop_frame

### Genlock

command | http url | response
:-----|:-----  | :----
genlock status | /ctrl/get?k=genlock |
genlock coarse | /ctrl/get?k=genlock_coarse |
genlock fine | /ctrl/get?k=genlock_fine |

### Clock

command | http url | response
:-----|:-----  | :----
sync camera time | /datetime?date=YYYY-MM-DD&time=hh:mm:ss
set timezone | /datetime?timezone=$timezone
get date time | /datetime/get
ntp time start | /ctrl/sntp?action=start&ip_addr=192.aa.bb.cc&port=123&interval=24
ntp time stop | /ctrl/sntp?action=stop
get ntp status | /ctrl/sntp?action=get
set ntp interval | /ctrl/sntp?action=set_interval&interval=$interval

### Upgrade

command | http url | response
:-----|:-----  | :----
upload new firmware to camera  | /uploadfirmware | 
refresh firmware to new one | /ctrl/upgrade?action=run |
check firmware | /ctrl/upgrade?action=fw_check |
ui check firmware | /ctrl/upgrade?action=ui_check

### Batch catalog settings query

use `/ctrl/getbatch?catalog=$catalog_name` to get a catalog settings from camera

command | http url | response
:-----|:-----  | :----
record | /ctrl/getbatch?catalog=record
video | /ctrl/getbatch?catalog=video
audio | /ctrl/getbatch?catalog=audio
image | /ctrl/getbatch?catalog=image
exposure | /ctrl/getbatch?catalog=exposure
white balance | /ctrl/getbatch?catalog=wb
lens | /ctrl/getbatch?catalog=lens
assist tools | /ctrl/getbatch?catalog=assitool
time code | /ctrl/getbatch?catalog=timecode
multi camera | /ctrl/getbatch?catalog=multicam
network | /ctrl/getbatch?catalog=network
security | /ctrl/getbatch?catalog=security
system | /ctrl/getbatch?catalog=system
maintanence | ctrl/getbatch?catalog=maintanence

## Settings

You can control most of the settings in the camera, just like what you see in the camera's GUI.
There are three data types of the camera settings.

|Type|Description|
|:--|:--|
|choice|Use the item from the option list|
|range|Numberic value, from mininum value to maxinum value with step|
|string|Text value|

You should get the data type and status(readonly or not) of the setting before you change it.
Each of the setting is bind to a key.

Use the following interface to get/set setting.
``` 
/ctrl/get?k=key
/ctrl/set?key=value
```

### Video settings

to batch get video settings with command

```
/ctrl/getbatch?catalog=video
```

command description | key | values
-------------------|----------  | ------
encoder | video_encoder | `H.264` `H.265` `ZRAW`
mov format |  | `ProRes 422 Proxy` `ProRes 422 LT` `ProRes 422` `ProRes 422 HQ`
bitrate level | bitrate_level | `Low` `Medium` `High`
compose mode (WDR) | compose_mode |`Off` `On`
eis on off | eis_on_off | `Off` `On`
video rotation | vid_rot | `Normal` `Upside Down`
video timelapse interval | video_tl_interval | 
low jello （低果冻） | low_jello | `Off` `On`

### Audio settings

command description | key | values
-------------------|----------  | ------
encoder | primary_audio | `None` `AAC` `PCM`
audio source | audio_channel | Off,Microphone,XLR,Mic Left + XLR Right,Mic Right + XLR Left
Phantom Power | audio_phantom_power | `Enable` `Disable` 
level display | audio_level_display | `Enable` `Disable`
gain type | ain_gain_type | `Auto` `Manual`
input level | audio_input_level |
input gain | audio_input_gain |
input left gain | audio_in_l_gain|
input right gain | audio_in_r_gain|
output gain | audio_output_gain| 0 ~ 13
noise reduction | audio_noise_reduction|`Off` `On`

### White balance settings

command description | key | response
-------------------|----------  | ------
white balance mode | wb | "Auto","Manual",..."Cloudy","Expert"
manual kelvin | mwb |
manual Tint | tint |
manual R | mwb_r |
manual G | mwb_g |
manual B | mwb_b |
auto white balance priority | wb_priority |
lock awb in recording | lock_awb_in_rec |

### Exposure settings

to batch get exposure settings with command

```
/ctrl/getbatch?catalog=exposure
```

command description | key | response
-------------------|----------  | ------
get/set ev | ev | ??? unknown
flicker | flicker | `60Hz` `50Hz`
meter mode | meter_mode | `Center` `Average` `Spot`
iris (aperture 光圈) | iris | `22` `20` ... `2` `2.2`...
iso options | iso | `Auto` `500` `640` ...
min iso | min_iso | `Auto` `500` `640` ...
max iso | max_iso | `1000` `1250` ... `102400`
iso control | iso_ctrl | `Fine` `Native ISO`
shutter angle | shutter_angle_ctrl | `Coarse` `Fine`
shutter operation | sht_operation | `Speed` `Angle`
max exposure shutter time | max_exp_shutter_time | `Auto` `1/50` `1/55`
Elec ND | eND | 
auto exposure speed | ae_speed |
black light comp | bl_comp |
live ae shutter | live_ae_shutter |
live ae iso | live_ae_iso |
ev choice  | ev_choice |
shutter time options | shutter_time |
lock ae in record | lock_ae_in_rec |

### Image basic settings

command | key | response
-------------------|----------  | ------
image profile | lut |
noise reduction | noise_reduction |
luma level | luma_level | it be used in video settings of web page 
sharpness | sharpness |
brightness | brightness
contrast | contrast |
saturation | saturation |
hue | hue |
dro | dro |
vignette | vignette |

##### Image Matrix
command | url | response
-------------------|----------  | ------
query | /ctrl/matrix
enable | /ctrl/matrix?enable=$value | 1 - enable, 0 -disable
set matrix value | /ctrl/matrix?index=$index&value=$value | [0, 5], value [-100, 100]

##### Image color correction
command | url | response
-------------------|----------  | ------
query cc option | /ctrl/cc
enable cc | /ctrl/cc?enable=${value} | 1 - enable, 0 -disable
set hue | /ctrl/cc?action=set_hue&index=${index}&value=${value} | [0, 12], value [-100, 100]
set saturation | /ctrl/cc?action=set_sat&index=${index}&value=${value} | [0, 12], value [-100, 100]

##### Image  gamma setting
command | url | response
-------------------|----------  | ------
get gamma options | /ctrl/gamma?action=get&option=gamma |
set gamma power | /ctrl/gamma?action=set&option=gamma&base=${base}&power=${power} |
query black level  | /ctrl/gamma?action=get&option=black_level |
config black level | /ctrl/gamma?action=set&option=black_level&enable=1&level=10 | 1 - enable, 0 - disable, level [-1000, 1000]
query black gamma | /ctrl/gamma?action=get&option=black_gamma |
config black gamma | /ctrl/gamma?action=set&option=black_gamma&enable=1&range=Narrow&level=0 |
query knee | /ctrl/gamma?action=get&option=knee |
config knee | /ctrl/gamma?action=set&option=knee&enable=1&point=50&slope=0 |

### Network settings

command | key | response
-------------------|----------  | ------
get ip mode | /ctrl/network?action=query
ethnet mode | /ctrl/get?k=eth_mode
get ip configuration | /ctrl/network?action=info
DHCP router, get ip from local router | /ctrl/network?action=set&mode=Router
Direct IP (10.98.32.1) | /ctrl/network?action=set&mode=Direct
Static IP | /ctrl/network?action=set&mode=Static&...
query wifi status | /ctrl/wifi_ctrl?action=query
get wifi options | /ctrl/get?k=wifi
set wifi options | /ctrl/set?wifi=$value | `Off` `On`

set static IP command
```
/ctrl/network?action=set&mode=Static&ipaddr=192.168.1.100&netmask=255.255.255.0&gateway=192.168.1.1&dns=8.8.8.8
```

### Connection settings

command | key | response
-------------------|----------  | ------
get usb role | /ctrl/get?k=usb_device_role |
set usb role | /ctrl/set?usb_device_role=$value | "Host","Mass Storage","Network","Serial","PTP","USB Camera"
query usb info | /ctrl/usb?action=query |
------ | ------ | ------
get sdi eanble/disable | /ctrl/get?k=sdi |
set sdi enable/disable | /ctrl/set?sdi=$value |
get sdi 3g mode | /ctrl/get?k=3g_sdi_mode |
set sdi 3g mode | /ctrl/set?3g_sdi_mode=$value |
------ | ------ | ------
get hdmi format | /ctrl/get?k=hdmi_format |
set hdmi format | /ctrl/set?hdmi_format=$value |
get hdmi osd option| /ctrl/get?k=hdmi_osd |
set hdmi osd option | /ctrl/set?hdmi_osd=$value | `Off` `On`
get hdmi osd layout | /ctrl/get?k=osd_layout |
set hdmi osd layout | /ctrl/set?osd_layout=$value | `Type 1` `Type 2`
------ | ------ | ------
query free-D | /ctrl/freed |
set free-D camera id | /ctrl/freed?camera_id=$value |
config free-D | /ctrl/freed?ip=$ip_address&port=$portValue |
enable free-D | /ctrl/freed?enable=$value |
------ | ------ | ------
set visca id | /ctrl/set?visca_id=$id_value |
set visca baudrate | /ctrl/set?visca_baudrate=$value |
enable visca | /ctrl/set?visca_enable=$value |

## Streaming

### libssp

command | key 
-------------------|---------- 
alt stream source to stream0 | /ctrl/set?send_stream=Stream0
alt stream source to stream1 | /ctrl/set?send_stream=Stream1
query | /ctrl/stream_setting?index=stream1&action=query
change streaming bitrate on the fly | /ctrl/stream_setting?index=stream1&bitrate=2000000

change stream settings

```
/ctrl/stream_setting?param1=value1&param2=value2&param3=value3...
```
for example
``` 
/ctrl/stream_setting?index=stream1&width=1920&height=1080
/ctrl/stream_setting?index=stream1&venc=h265
/ctrl/stream_setting?index=stream1&bitwidth=8
```
|param|description|
|:--|:--|
|index|stream0/stream1|
|width|video width|
|height|video height|
|bitrate|encode bitrate (bps)|
|split|in seconds (less than 5 minutes)|
|fps|fps of the stream data|
|venc|video encoder|
|bitwidth|bit width of the H.265|

> [!NOTE] Title
> before stream0/1, please make sure it is idle with command `/ctrl/stream_setting?index=stream1&action=query`

### General
In high version firmware (1.0.10 or later) , support these genera streaming settings for rtmp/rtsp/srt

command | key | description 
-------------------|---------- | ---- 
get/set stream resolution | stream_resolution | 
get/set stream frame rate | stream_fps |
get/set stream video encoder | stream_video_encoder | `H.264` or `H.265`
get/set stream param save | stream_param_save |

command example :
```
/ctrl/get?k=stream_video_encoder
/ctrl/get?k=stream_fps

/ctrl/set?stream_video_encoder=H.265
```

### Rtmp
command | key | description 
-------------------|---------- | ---- 
query| /ctrl/rtmp?action=query

### Rtsp
command | key | description 
-------------------|---------- | ---- 
query| /ctrl/rtsp?action=query

### Ndi
command | key | description 
-------------------|---------- | ---- 
query | /ctrl/ndi?action=query

### Srt
command | key | description 
-------------------|---------- | ---- 
query | /ctrl/srt?action=query


## Lens control

### lens control utils

command | key | description 
-------------------|----------  | ------
restore lens pos | /ctrl/set?restore_lens_pos=Disable/Enable |
get lens information | /ctrl/lens?action=query | {<br>  "name": "LAOWA C&D-Dreamer MFT 10mm F2.0", <br>  "focus_distance": 327675,<br>  "focal_length": 10,<br>  "iris_fno": "F22"<br>}
get lens focal length | /ctrl/get?k=lens_focal_length

### Focus

command | key | description
-------------------|----------  | ------
near | /ctrl/lens?action=focusnear&fspeed=$speed
far | /ctrl/lens?action=focusfar&fspeed=$speed
stop | /ctrl/lens?action=focusstop
status | /ctrl/lens?action=f_status

### AF (*Auto Focus*)

command | key | description
-------------------|----------  | ------
triger auto focus | /ctrl/af
af speed | /ctrl/get?k=af_speed
focus method | /ctrl/get?k=focus |`MF` or `AF`
continuous af | /ctrl/get?k=caf |`On` or `Off`
flexiable size | /ctrl/get?k=af_area
continuous af sensitivity | /ctrl/get?k=caf_sens
live continuous af | /ctrl/get?k=live_caf
af adjust with PTZ | /ctrl/get?k=af_adjust_with_ptz | 
MF assist preview | /ctrl/get?k=mf_mag | `On` or `Off`
MF assist recording | /ctrl/get?k=mf_recording | `On` or `Off`
-------------------|----------  | ------
trace with face id | /ctrl/af_face/trace_target?id=$id_value
-------------------|----------  | ------
ROI type | /ctrl/get?k=af_mode | `Flexible Zone` or `Human Track`
update the ROI of AF | /ctrl/af?action=update_roi&x=0&y=0&w=100&h=100 | [x,y,w,h] is normalized value scaled on 1000
update the ROI to center | /ctrl/af?action=update_roi_center&x=500&y=500
get the ROI | /ctrl/af?action=query
-------------------|----------  | ------
control the focus far/near | /ctrl/set?mf_drive=1、2、3、-3、-2、-1
set the focus plane to a specific value | /ctrl/set?lens_focus_pos=$value

### Zoom

command | key | description
-------------------|----------  | ------
zoom mode | /ctrl/get?k=zoom_mode | not supported in some model ???
zoom position | /ctrl/get?k=lens_zoom_pos
zoom status | /ctrl/lens?action=z_status
zoom in with speed | /ctrl/set?lens_zoom=in&fspeed=$value
zoom out | /ctrl/set?lens_zoom=out&fspeed=$value
stop zoom | /ctrl/set?lens_zoom=stop
zoom to a position | /ctrl/set?lens_zoom_pos=value

> [!NOTE] 
> **To control the focus manually with HTTP, the lens must be in the AF mode with command '/ctrl/set?focus=AF' **

### Pan Tilt control

```
/ctrl/pt?action=direction&speed=N
```

direction could be following values : `left、right、up、down、leftup、leftdown、rightup、rightdown、stop`
the range of speed is `0-0x3f`, larger value means faster speed

### PTZ

command | key | description
-------------------|----------  | ------
query | /ctrl/pt?action=query
query details | /ctrl/pt?action=query&detail=y
stop | /ctrl/pt?action=stop |
stop all | /ctrl/pt?action=stop_all |
direction move | /ctrl/pt?action=$direction&fspeed=$speed |
pan and tilt speed | /ctrl/pt?action=pt&pan_speed=$pan&tilt_speed=$tilt
home |/ctrl/pt?action=home
reset |/ctrl/pt?action=reset
limit update | /ctrl/pt?action=limit&direct=$direct&pan_pos=$pan_pos&tilt_pos=$tilt_pos
limit | /ctrl/get?k=ptz_limit | `Enable` `Disable`
speed mode | /ctrl/get?k=pt_speedmode |
speed with zoom position | /ctrl/get?k=pt_speed_with_zoom_pos |
flip | /ctrl/get?k=ptz_flip |
privacy mode | /ctrl/get?k=pt_priv_mode |
power on position | /ctrl/get?k=pt_pwr_pos |
-------------------|----------  | ------
preset recall | /ctrl/preset?action=recall&index=$value |
preset save  | /ctrl/preset?action=save&index=$value
preset delete  | /ctrl/preset?action=del&index=$value
preset info | /ctrl/preset?action=get_info&index=$index_value
preset name | /ctrl/preset?action=set_name&index=$value&new_name=$name_vaule
preset speed unit | /ctrl/preset?action=preset_speed&index=$index&preset_speed_unit=$unit
preset speed by duration | /ctrl/preset?action=preset_speed&index=$index&preset_time=$time
preset speed by index | /ctrl/preset?action=preset_speed&index=$index&preset_speed=$speed
common speed | /ctrl/get?k=ptz_common_speed |
common time | /ctrl/get?k=ptz_common_time |
preset recall mode | /ctrl/get?k=ptz_preset_mode |
recall speed mode | /ctrl/get?k=ptz_speed_mode |
freeze duration recall | /ctrl/get?k=freeze_during_preset |
common speed unit | /ctrl/get?k=ptz_common_speed_unit |
-------------------|----------  | ------
delete ptz trace | /ctrl/ptrace?action=del&index=${index}
rename ptz trace | /ctrl/ptrace?action=set_name&index=${index}&new_name=$value}
record trace start | /ctrl/ptrace?action=rec_start&index=${index} |
record trace stop | /ctrl/ptrace?action=rec_stop}
prepare play trace | /ctrl/ptrace?action=play_prepare&index=${index}
play trace start | /ctrl/ptrace?action=play_start
play trace stop | /ctrl/ptrace?action=play_stop
query | /ctrl/ptrace?action=query
get trace info | /ctrl/ptrace?action=get_info&index=${index}

## Storage

command | key | description
-------------------|----------  | ------
check the card is present | /ctrl/card?action=present
query format | /ctrl/card?action=query_format
format the storage card | /ctrl/card?action=format
format the card to fat32 | /ctrl/card?action=fat32
format the card to exfat | /ctrl/card?action=exfat
query the card free space | /ctrl/card?action=query_free
query the card total space | /ctrl/card?action=query_total
-------------------|----------  | ------
list out the folders in card | /DCIM/ | {  "code": 0,   "desc": "",  "files": [   "100ZCAME",   "101ZCAME" ]}
list the files under the folder | /DCIM/$folderName | $folderName is get from `/DCIM`
download the file | /DCIM/$folderName/$fileName | $fileName is get from `/DCIM/$folderName`
delete the file | /DCIM/$folderName/$fileName?act=rm
get the thumbnail | /DCIM/$folderName/$fileName?act=thm | JPEG data
get screen nail | /DCIM/$folderName/$fileName?act=scr | larger JPEG data then the thumbnail
get create time of the file | /DCIM/$folderName/$fileName?act=ct
get the file info | /DCIM/$folderName/$fileName?act=info
