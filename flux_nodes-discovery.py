# python 3.6

import sys 
import uuid
import json
import time
import sys
import requests
from datetime import timedelta, datetime
from os import environ
 
from requests import get
from paho.mqtt import client as mqtt_client

############### MODIFY VARIABLE BELOW #############
broker = '192.168.xxx.xxx'
port = 1883
# Generate a Client ID with the publish prefix.
client_id = 'flux'
username = 'mqtt'
password = 'xxx'
############### MODIFY VARIABLE END################

wallet = sys.argv[1]

g_deviceModel = "Flux-node"                        
g_swVersion = "0.9"                               
g_manufacturer = "Byackee"                              
g_deviceName = "Flux-node"

liste = {
    "status": ["benchmark", "status.status", "online", "offline"],
    "ip": ["flux", "ip", "\u200B", "\u200B"],
    "type": ["node", "status.tier", "\u200B", "\u200B"],
    "benchmark_info_version": ["benchmark", "info.version", "\u200B", "\u200B"],
    "flux_info_version": ["flux", "version", "\u200B", "\u200B"],
    "flux_staticIp": ["flux", "staticIP", "\u200B", "\u200B"],
    "flux_bench_realCores": ["benchmark", "bench.real_cores", "\u200B", "\u200B"],
    "flux_bench_realCores": ["benchmark", "bench.real_cores", "\u200B", "\u200B"],
    "flux_bench_cores": ["benchmark", "bench.cores", "\u200B", "\u200B"],
    "flux_bench_ram": ["benchmark", "bench.ram", "\u200B", "\u200B"],
    "flux_bench_ssd": ["benchmark", "bench.ssd", "\u200B", "\u200B"],
    "flux_bench_hdd": ["benchmark", "bench.hdd", "\u200B", "\u200B"],
    "flux_bench_ddwrite": ["benchmark", "bench.ddwrite", "\u200B", "\u200B"],
    "flux_bench_totalstorage": ["benchmark", "bench.totalstorage", "\u200B", "\u200B"],


 }
 
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("ee")#Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    if password:
        client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

liste_adresses_ip = ""
payload = ""
    
def parse(client): 

    url = f"http://api.runonflux.io/explorer/fluxtxs?filter={wallet}"

    print(f"Requesting {url=}")
    res = get(url=url)
    data = res.json()
    liste_adresses_ip = set(entry["ip"] for entry in data["data"] if entry["ip"])
    
    if res.status_code != 200:
        print(f"Error")
     
    else:
        for ip in liste_adresses_ip:
            # Récupérer le JSON pour chaque adresse IP
            json_data = recuperer_json(ip)
            ip = ip.replace(":", "_")
            ip = ip.replace(".", "_")
            if json_data:
                data = json_data.pop("data", {})
                # Utiliser le JSON (remplacer cela par le traitement spécifique dont vous avez besoin)
                if data:
                    for index, (x, valeurs) in enumerate(liste.items()):
                        print(index)
                        if x in ["status", "blocked"]: #binary_sensor   
                            discoveryTopic = f"homeassistant/binary_sensor/fluxnode/node_{ip}_{x}/config";
                            payload = '{"unique_id": "' + f"node_{ip}_" + x + '" , ' + '"name": "' + f"node_{ip}" + '.' + x + '", "stat_t": "' + f"flux_nodes/{ip}/{valeurs[0]}" +'", "value_template": "{{ value_json.' + valeurs[1] +' }}", ' + '"device_class": "connectivity' + '", "payload_on": "' + valeurs[2] +'", "payload_off": "' + valeurs[3] +'", "device": {"identifiers": ["'+ f"{g_deviceModel}_{ip}"'"], "name": "' + f"node_{ip}" + '", "model": "' + f"{g_deviceModel}" + '", "manufacturer": "' + f"{g_manufacturer}" + '", "sw_version": "' + f"{g_swVersion}" '+" }}'

                        else:
                            discoveryTopic = f"homeassistant/sensor/fluxnode/node_{ip}_{x}/config";
                            payload = '{"unique_id": "' + f"node_{ip}_" + x + '" , ' + '"name": "' + f"node_{ip}" + '.' + x + '", "stat_t": "' + f"flux_nodes/{ip}/{valeurs[0]}" +'", "value_template": "{{ value_json.' + valeurs[1] +' }}", ' + ' "device": {"identifiers": ["'+ f"{g_deviceModel}_{ip}"'"], "name": "' + f"node_{ip}" + '", "model": "' + f"{g_deviceModel}" + '", "manufacturer": "' + f"{g_manufacturer}" + '", "sw_version": "' + f"{g_swVersion}" '+" }}'
                        
                        client.publish(discoveryTopic,payload,0,retain=True)

     
    # Fonction pour récupérer le JSON à partir de l'URL https://IP/flux/info
def recuperer_json(ip):
    url = f"http://{ip}/flux/info"
    print(f"Retrieve json data for {url=}")
    try:
        reponse = requests.get(url, timeout=4)
        if reponse.status_code == 200:
            # Retourner le contenu JSON
            return reponse.json()
        else:
            print(f"Échec de la requête pour {ip} avec le code de statut {reponse.status_code}")
    except requests.RequestException as e:
        print(f"Erreur de requête pour {ip} : {e}")
    return None

    # Boucle sur chaque adresse IP dans la liste

def run():
    client = connect_mqtt()
    parse(client)

   
if __name__ == '__main__':
    run()
 
