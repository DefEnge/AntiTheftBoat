import React, { useState, useEffect } from "react";
import axios from "axios";

interface Device {
  deviceId: string;
}

const DeviceListPage: React.FC = () => {
  const [devices, setDevices] = useState<Device[]>([]);

  useEffect(() => {
    const fetchDevices = async () => {
      try {
        const response = await axios.get("http://localhost:5000/devices");
        setDevices(response.data);
      } catch (error) {
        console.error("Error fetching devices", error);
      }
    };
    fetchDevices();
  }, []);

  return (
    <div className="device-list">
      <h1>Device List</h1>
      <ul>
        {devices.map((device) => (
          <li key={device.deviceId}>
            <span>{device.deviceId}</span>
            <button>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default DeviceListPage;

