import os
from flask import Flask
import requests
import binascii
import time


def send_data():
    url = "https://eu1.cloud.thethings.network/api/v3/as/applications/anti-theft-boat0/webhooks/test-webhook/devices/guardplace-device/down/push"

    headers = {
        "Authorization": "Bearer NNSXS.",
        "Content-Type": "application/json",
        "User-Agent": "my-integration/my-integration-version",
    }

    data = {"downlinks": [{"frm_payload": "test", "f_port": 15, "priority": "NORMAL"}]}

    response = requests.post(url, headers=headers, json=data)

    return "all good"


def send_register(device: str):
    deveui_b = os.urandom(8)
    deveui_x = binascii.hexlify(deveui_b).decode("utf-8").upper()

    appkey_b = os.urandom(16)
    appkey_x = binascii.hexlify(appkey_b).decode("utf-8").upper()

    # deveui_x = "70B3D57ED006E210"
    # appkey_x = "7052DAE80D8406DB38D2532B10D92348"

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

    headers = {
        "Authorization": "Bearer NNSXS",
        "Content-Type": "application/json",
    }

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
            return "registered the new device"
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

    headers = {
        "Authorization": "Bearer NNSXS",
        "Content-Type": "application/json",
        "User-Agent": "my-integration/my-integration-version",
    }

    response = requests.delete(url, headers=headers)

    if response.status_code == 200:
        return "delete succesfully"
    else:
        print(response.status_code)
        print(response.text)
        return "erro"


def get_devices():
    url = "https://eu1.cloud.thethings.network/api/v3/applications/anti-theft-boat0/devices"

    headers = {
        "Authorization": "Bearer NNSXS",
        "Content-Type": "application/json",
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("okay")
        return response.text
    else:
        print(response.status_code)
        print(response.text)
        return "err"


# Initialize the Flask application
app = Flask(__name__)


# Define a route for the home page
@app.route("/downlink")
def downlink():
    return send_data()


@app.route("/register")
def register():
    return send_register("funziona")


@app.route("/delete")
def delete():
    return delete_device("funziona")


@app.route("/devices")
def list_devices():
    return get_devices()


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
