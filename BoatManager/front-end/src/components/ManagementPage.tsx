import React, { useState } from "react";
import axios from "axios";

const ManagementPage: React.FC = () => {
  const [deviceId, setDeviceId] = useState<string>("");
  const [devEui, setDevEui] = useState<string>("");
  const [appKey, setAppKey] = useState<string>("");
  const [message, setMessage] = useState<string>(null);

  const handleAddDevice = async () => {
    try {
      setDeviceId("");
      setDevEui("");
      setAppKey("");
      const response = await axios.get("http://127.0.0.1:5000/register/" + deviceId);
      console.log(response.data)
      setDeviceId(response.data.DeviceId);
      setDevEui(response.data.DevEui);
      setAppKey(response.data.AppKey);
      setMessage("Device added successfully!");
    } catch (error) {
      console.error("Error adding device", error);
      setMessage("Error adding device.");
    }
  };

  const handleDeleteDevice = async () => {
    try {
      await axios.get("http://127.0.0.1:5000/delete/" + deviceId);
      setDeviceId("");
      setDevEui("");
      setAppKey("");
      setMessage("Device deleted successfully!");
    } catch (error) {
      console.error("Error deleting device", error);
      setMessage("Error deleting device.");
    }
  };

  return (
    <div className="device-management">
      <h1>Device Management</h1>
      <div>
        <input
          type="text"
          placeholder="Device ID"
          value={deviceId}
          onChange={(e) => setDeviceId(e.target.value)}
        />
        <button onClick={handleAddDevice}>Register Device</button>
        <button onClick={handleDeleteDevice}>Delete Device</button>
      </div>

      {message && <div className="alert">{message}</div>}
      {deviceId && <div className="alert">{"DeviceId: " + deviceId}</div>}
      {devEui && <div className="alert">{"DevEui: " + devEui}</div>}
      {appKey && <div className="alert">{"Appkey: " + appKey}</div>}
    </div>
  );
};

export default ManagementPage;

