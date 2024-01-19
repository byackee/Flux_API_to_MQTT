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
 
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

liste_adresses_ip = ""

def parse(client): 

    url = f"http://api.runonflux.io/explorer/fluxtxs?filter={wallet}"

    print(f"Requesting {url=}")
    res = get(url=url)
    data = res.json()
    liste_adresses_ip = set(entry["ip"] for entry in data["data"] if entry["ip"])
    
    if res.status_code != 200:
        print(f"Error {data}")
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
                    for key, value in data.items():
                        topic = f"flux_nodes/{ip}/{key}"
                        payload = json.dumps(value)
                        client.publish(topic, payload)
                        #print(f"Published on {topic}: {payload}")
 
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
 