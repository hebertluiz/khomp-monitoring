# khomp-monitoring
Tools to monitor khomp devices


Tool created to help monitoring applications like nagios connect and retrieve data from khomp kQuery server.

Usage: `$ ./khomp-device-check.py --check-type <E1|GSM|DEVICE> --serial <DEVICE_SERIAL> --link <LINK_NUMBER>`

#### DONE
- [x] E1 state.
#### TODO

- [ ] GSM state
    - [ ] Return GSM Signal Level
    - [ ] Return GSM Carrier name
    - [ ] Reset GSM modem
- [ ] Device state
    - [ ] Return device address 
    - [ ] Return device type
    - [ ] Return device channel count.
