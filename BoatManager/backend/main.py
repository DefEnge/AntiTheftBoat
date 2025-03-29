import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import requests
import threading
import paho.mqtt.client as mqtt
import binascii
import time
from dotenv import load_dotenv

load_dotenv()

APIKEY = os.getenv("APIKEY")
headers = {
    "Authorization": "Bearer " + str(APIKEY),
    "Content-Type": "application/json",
}

# MQTT cred
MQTT_APIKEY = os.getenv("MQTT_APIKEY")
MQTT_TENANT = os.getenv("MQTT_TENANT")
MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT = os.getenv("MQTT_PORT")
APPLICATION_ID = os.getenv("APPLICATION_ID")


def on_connect(client, userdata, flags, rc, prop):
    print("connected with result code " + str(rc))
    client.subscribe("#")


def on_message(client, userdata, msg):
    topic = str(msg.topic)
    message = str(msg.payload.decode("utf-8"))
    print(topic + " " + message)


client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id="pyintegration",
    userdata=None,
    protocol=4,
)
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(APPLICATION_ID, MQTT_APIKEY)
client.connect(MQTT_BROKER, 1883, 60)


def send_register(device: str, username: str, plate: str):
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
            response = {
                "DeviceId": device,
                "DevEui": str(deveui_x),
                "AppKey": str(appkey_x),
                "message": "Device added successfully",
                "device": {
                    "deviceId": device,
                    "username": username,
                    "targa": plate,
                },
                "status": 200,
            }
            return response
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
            return "err"
    else:
        print(response.status_code)
        print(response.text)
        return "err"


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
        return jsonify(response.json())
    else:
        print(response.status_code)
        print(response.text)
        return "err"


app = Flask(__name__)

CORS(app)


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"sqlite:///{os.path.join(BASE_DIR, 'devices.db')}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


class Device(db.Model):
    id = db.Column(
        db.Integer, primary_key=True, autoincrement=True
    )  # Primary key with auto-increment
    device_id = db.Column(db.String(100), nullable=False, unique=True)
    targa = db.Column(db.String(20), nullable=False)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    cognome = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False)


with app.app_context():
    db.create_all()


@app.route("/register", methods=["POST"])
def register():
    input_json = request.get_json(force=True)
    if not input_json:
        return jsonify({"error": "No json received"}), 400

    device_id = input_json.get("deviceId")
    username = input_json.get("username")
    plate = input_json.get("targa")

    if not all([device_id, username, plate]):
        return jsonify({"error": "Missing required fields"}), 400

    respons = send_register(device_id, username, plate)
    if respons != "err":
        new_device = Device(
            device_id=input_json["deviceId"],
            targa=input_json["targa"],
        )

        db.session.add(new_device)
        db.session.commit()
    return jsonify({"respons": respons}), 201


@app.route("/delete/<deviceid>")
def delete(deviceid):
    try:
        respons = delete_device(deviceid)
        device = Device.query.filter_by(device_id=deviceid).first()

        if not device or respons == "err":
            return jsonify({"error": f"Device with ID {deviceid} not found"}), 404

        # Delete the device
        db.session.delete(device)
        db.session.commit()

        return jsonify({"message": f"Device {deviceid} deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route("/devices")
def list_devices():
    devices = Device.query.all()
    return jsonify(
        [
            {
                "deviceId": d.device_id,
                "nome": d.nome,
                "cognome": d.cognome,
                "targa": d.targa,
            }
            for d in devices
        ]
    )
    # usare per prendere da ttn;
    # return get_devices()


@app.route("/pair", methods=["POST"])
def pair_devices():
    data = request.get_json()
    username = data.get("username")
    device = data.get("device")

    user = User.query.filter_by(username=username).first()
    deviceid = Device.query.filter_by(device_id=device).first()

    if not user or not deviceid:
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify({"paired_device": device, "user": username})


@app.route("/signin", methods=["POST"])
def signin():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")
    name = data.get("nome")
    surname = data.get("cognome")
    role = data.get("role", "user")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "User already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    new_user = User(
        username=username,
        email=email,
        nome=name,
        cognome=surname,
        password_hash=hashed_password,
        role=role,
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()

    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid credentials"}), 401

    token = "test log succes"
    return jsonify({"access_token": token, "role": user.role})


# Run the Flask app
def mqtt_client():
    client.loop_forever()


if __name__ == "__main__":
    mqtt_t = threading.Thread(target=mqtt_client)
    mqtt_t.start()
    app.run(debug=True)
