# SEN0592 Distance Sensor

This repository contains the ESPHome configuration and ROS 2 driver for the [SEN0592 distance sensor](https://www.dfrobot.com/product-2729.html), 5m range, RS485, IP67.

## Directory Structure

- `firmware/`: Contains the ESPHome configuration (`atomlite-distance.yaml`) and related files for the [Atom Lite board](https://shop.m5stack.com/products/atom-lite-esp32-development-kit) with [RS485 interface](https://shop.m5stack.com/products/atomic-rs485-base) to the SEN0592 sensor.
- `ros_node/`: Contains the `sen0592_driver` ROS 2 package to interface with the sensor over HTTP.

## Sensor Wiring

| Color  | Label | Description                       |
| ------ | ----- | --------------------------------- |
| Red    | VCC   | power supply input positive pole  |
| Black  | GND   | power ground wire                 |
| Yellow | B     | RS485 B line                      |
| White  | A     | RS485 A line                      |

## Build and Flash Instructions

```bash
pixi run compile
pixi run upload
```

## Network Configuration

The sensor is configured to use a static IP address (`192.168.105.70`) on a
private network, which credentials must be set in `firmware/secrets.yaml`.
To switch to a different network, update the `secrets.yaml` and provide Wi-Fi
credentials or use the ESPHome captive portal that will be available when the
device cannot connect to the configured network.

Format of `secrets.yaml`:
```yaml
wifi_ssid: "YourWiFiSSID"
wifi_password: "YourWiFiPassword"
```

## ROS 2 Node

The corresponding ROS 2 node for this sensor is `sen0592_node`. It polls the
ESPHome web server to retrieve distance measurements and publishes them as a
`sensor_msgs/Range` message.

- **Default IP:** `192.168.105.70`
- **ESPHome Endpoint:** `/sensor/distance`
- **Output Topic:** `/sen0592/distance` (Range in meters)
- **Frame ID:** `sen0592_link`

### Usage

Run the node using:
```bash
source <ROS Workspace>/install/setup.bash
ros2 run sen0592_driver sen0592_node --ros-args -p sensor_ip:=192.168.105.70
```
