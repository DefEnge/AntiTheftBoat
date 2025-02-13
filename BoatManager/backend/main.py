import os
from flask import Flask
import requests
import binascii
import time
from dotenv import load_dotenv

load_dotenv()

APIKEY = os.getenv("APIKEY")

headers = {
    "Authorization": "Bearer " + str(APIKEY),
    "Content-Type": "application/json",
}


def send_register(device: str):
    deveui_b = os.urandom(8)
    deveui_x = binascii.hexlify(deveui_b).decode("utf-8").upper()

    appkey_b = os.urandom(16)
    appkey_x = binascii.hexlify(appkey_b).decode("utf-8").upper()

    url = "https://eu1.cloud.thethings.network/api/v3/applications/anti-theft-boat0/devices"
    nsurl = (
        "https://eu1.cloud.thethings.network/api/v3/ns/applications/anti-theft-boat0/devices/"
        + device
    )
    asurl = (
        "https://eu1.cloud.thethings.network/api/v3/as/applications/anti-theft-boat0/devices/"
        + device
    )
    jsurl = (
        "https://eu1.cloud.thethings.network/api/v3/js/applications/anti-theft-boat0/devices/"
        + device
    )
    data = {
        "end_device": {
            "ids": {
                "join_eui": "0000000000000000",
                "dev_eui": str(deveui_x),
                "device_id": device,
                "application_ids": {"application_id": "anti-theft-boat0"},
            },
            "network_server_address": "eu1.cloud.thethings.network",
            "application_server_address": "eu1.cloud.thethings.network",
            "join_server_address": "eu1.cloud.thethings.network",
        },
        "field_mask": {
            "paths": [
                "network_server_address",
                "application_server_address",
                "join_server_address",
            ]
        },
    }

    data_ns = {
        "end_device": {
            "frequency_plan_id": "EU_863_870_TTN",
            "lorawan_version": "MAC_V1_0_3",
            "lorawan_phy_version": "PHY_V1_0_3_REV_A",
            "supports_join": True,
            "multicast": False,
            "supports_class_b": False,
            "supports_class_c": False,
            "mac_settings": {"rx2_data_rate_index": 0, "rx2_frequency": "869525000"},
            "ids": {
                "join_eui": "0000000000000000",
                "dev_eui": str(deveui_x),
                "device_id": device,
                "application_ids": {"application_id": "anti-theft-boat0"},
            },
        },
        "field_mask": {
            "paths": [
                "frequency_plan_id",
                "lorawan_version",
                "lorawan_phy_version",
                "supports_join",
                "multicast",
                "supports_class_b",
                "supports_class_c",
                "mac_settings.rx2_data_rate_index",
                "mac_settings.rx2_frequency",
                "ids.join_eui",
                "ids.dev_eui",
                "ids.device_id",
                "ids.application_ids.application_id",
            ]
        },
    }

    data_as = {
        "end_device": {
            "ids": {
                "join_eui": "0000000000000000",
                "dev_eui": str(deveui_x),
                "device_id": device,
                "application_ids": {"application_id": "anti-theft-boat0"},
            }
        },
        "field_mask": {
            "paths": [
                "ids.join_eui",
                "ids.dev_eui",
                "ids.device_id",
                "ids.application_ids.application_id",
            ]
        },
    }

    data_js = {
        "end_device": {
            "ids": {
                "join_eui": "0000000000000000",
                "dev_eui": str(deveui_x),
                "device_id": device,
                "application_ids": {"application_id": "anti-theft-boat0"},
            },
            "root_keys": {"app_key": {"key": str(appkey_x)}},
        },
        "field_mask": {
            "paths": [
                "ids.join_eui",
                "ids.dev_eui",
                "ids.device_id",
                "ids.application_ids.application_id",
                "root_keys.app_key.key",
            ]
        },
    }

    response = requests.post(url, headers=headers, json=data)

    time.sleep(5)
    if response.status_code == 200:
        print(response.text)
        print("-----------------------")
        print(nsurl)
        print(asurl)
        print(jsurl)
        print("-----------------------")

        response_ns = requests.put(nsurl, headers=headers, json=data_ns)
        time.sleep(2)
        response_as = requests.put(asurl, headers=headers, json=data_as)
        time.sleep(5)
        response_js = requests.put(jsurl, headers=headers, json=data_js)
        if (
            response_ns.status_code == 200
            and response_as.status_code == 200
            and response_js.status_code == 200
        ):
            return (
                "registered the new device "
                + device
                + "with DevEui:"
                + str(deveui_x)
                + "AppKey:"
                + str(appkey_x)
            )
        else:
            print(response_ns.status_code)
            print(response_ns.text)
            print("-----------------------")
            print(response_as.status_code)
            print(response_as.text)
            print("-----------------------")
            print(response_js.status_code)
            print(response_js.text)
            print("-----------------------")
            return "ERROR"
    else:
        print(response.status_code)
        print(response.text)
        return "erro"


def delete_device(device: str):
    url = (
        "https://eu1.cloud.thethings.network/api/v3/applications/anti-theft-boat0/devices/"
        + device
    )
    nsurl = (
        "https://eu1.cloud.thethings.network/api/v3/ns/applications/anti-theft-boat0/devices/"
        + device
    )
    asurl = (
        "https://eu1.cloud.thethings.network/api/v3/as/applications/anti-theft-boat0/devices/"
        + device
    )
    jsurl = (
        "https://eu1.cloud.thethings.network/api/v3/js/applications/anti-theft-boat0/devices/"
        + device
    )

    response = requests.delete(url, headers=headers)

    responsens = requests.delete(nsurl, headers=headers)
    responseas = requests.delete(asurl, headers=headers)
    responsejs = requests.delete(jsurl, headers=headers)

    if (
        response.status_code == 200
        and responsens.status_code == 200
        and responseas.status_code == 200
        and responsejs.status_code == 200
    ):
        return "delete succesfully" + device
    else:
        print(response.status_code)
        print(response.text)
        return "err"


def get_devices():
    url = "https://eu1.cloud.thethings.network/api/v3/applications/anti-theft-boat0/devices"

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("okay")
        return response.text
    else:
        print(response.status_code)
        print(response.text)
        return "err"


app = Flask(__name__)


@app.route("/register/<deviceid>")
def register(deviceid):
    return send_register(deviceid)


@app.route("/delete/<deviceid>")
def delete(deviceid):
    return delete_device(deviceid)


@app.route("/devices")
def list_devices():
    return get_devices()


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
