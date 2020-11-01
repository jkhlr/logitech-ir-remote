# Logitech IR remote

Turn your Logitech Z-5500 Digital speakers on and off using a Raspberry Pi 3 Model B

## Setup IR Emitter

Connect IR emitter to Raspberry Pi GPIO
- `GND -> Pin 20`
- `VCC -> Pin 2`
- `SIG -> Pin 18 (GPIO 24)`

## Activate Kernel Module

```shell script
echo 'dtoverlay=gpio-ir-tx,gpio_pin=24' >> /boot/config.txt
```
... and reboot your Raspberry Pi
 
## Run the Server

```shell script
docker build -t local/logitech-ir-remote .
docker run --rm -p 8000:80 --device /dev/lirc0 local/logitech-ir-remote
```

## Turn Power On and Off

Turn on:
```shell script
curl localhost:8000/on
```

Turn off
```shell script
curl localhost:8000/off
```

Get status:
```shell script
curl localhost:8000/off
```