# Home Assistant Raspberry Pi Fan GPIO PWM custom integration

## About

This project is a fork of the original [RedMeKool](https://github.com/RedMeKool/HA-Raspberry-pi-GPIO-PWM) project which I modified in order to detect the entity as a fan rather than as a light.

**This is a spin-off from the original Home Assistant integration which was marked as deprecated and will be removed in Home Assistant Core 2022.4.**

The rpi_fan_gpio_pwm platform allows to control multiple fans using pulse-width modulation. It supports FANs driven by GPIOs of a Raspberry Pi (same host or remote)
For controlling the GPIOs, the platform connects to the pigpio-daemon (http://abyz.me.uk/rpi/pigpio/pigpiod.html), which must be running. On Raspbian Jessie 2016-05-10 or newer the pigpio library is already included. On other operating systems it needs to be installed first (see installation instructions: https://github.com/soldag/python-pwmled#installation).

For Home Assistant this daemon can be installed as an add-on (https://github.com/Poeschl/Hassio-Addons/tree/master/pigpio).

## Installation

### HACS

The recommend way to install `ha-rpi_fan_gpio_pwm` is through [HACS](https://hacs.xyz/).

### Manual installation

Copy the `ha-rpi_fan_gpio_pwm` folder and all of its contents into your Home Assistant's `custom_components` folder. This folder is usually inside your `/config` folder. If you are running Hass.io, use SAMBA to copy the folder over. You may need to create the `custom_components` folder and then copy the `ha-rpi_fan_gpio_pwm` folder and all of its contents into it.

## Configuration
To enable this platform, add the following lines to your configuration.yaml:

```yaml
# Example configuration.yaml entry
fan:
  - platform: rpi_fan_gpio_pwm
    fans:
      - name: RPI Cooling Fan
        pin: 17
```

## CONFIGURATION VARIABLES
- **fans** list *(REQUIRED)*: Can contain multiple FANs.

- **name** string *(REQUIRED)*: The name of the FAN.

- **pin** integer *(REQUIRED)*: The pin connected to the FAN as a list.

- **host** string *(optional, default: localhost)*: The remote host address for the GPIO driver.

- **port** integer *(optional, default: 8888)*: The port on which the GPIO driver is listening.

## Authors & contributors

This project is a fork of the original [RedMeKool](https://github.com/RedMeKool/HA-Raspberry-pi-GPIO-PWM) project.

## License

MIT License

Copyright (c) 2023 [Frosh](https://github.com/erdnaxela02)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
>
> **_BECAUSE IT IS A FORK, Parts of the project are originally Copyright (c) 2022, [RedMeKool](https://github.com/RedMeKool/HA-Raspberry-pi-GPIO-PWM)_**
>
