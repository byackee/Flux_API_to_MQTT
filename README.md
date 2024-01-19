# Flux_API_to_MQTT
Scan and add nodes with your wallet address to MQTT (with Home Assistant discovery)

## Requirements:
  * Python3 & pip3
  * module paho-mqtt (pip3 install paho-mqtt)

## Utilisation:
  1) In both file presearch-discovery.py & presearch.py, modify mqtt variable for connect your broker (ip, port, user, port)
  2) Launch 1 time script "python3 flux_nodes-discovery.py your_api_token"
  3) Create cron (every 5 minute) to run scrupt "python3 flux_nodes.py your_api_token

## How its work:
With your cron the script give the main data from flux API and send all to your MQTT broker.

## Credits


## Todo
- [x] Functional code
- [ ] Cleanup and add more docs on complete installation
- [ ] Improve/Optimize code
- [ ] Add more features & personalization
- [ ] Easy install by HACS

## Donation
  [Support via PayPal](https://www.paypal.me/byackee/)
  
  Eth: 0x7F57f6ad25c501deb2fcaCA863264F593efe31d8
  
  Flux: t1U3ubvVNhCHFkzGYZV52huyE4a1MGh3ymE
