
import React, { useState, useEffect } from "react";
import axios from "axios";

interface Device {
  deviceId: string;
  devEui: string;
}

const DeviceListPage: React.FC = () => {
  const [devices, setDevices] = useState<Device[]>([]);

  useEffect(() => {
    const fetchDevices = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:5000/devices");
        const fetchedDevices = response.data.end_devices.map((device: any) => ({
          deviceId: device.ids.device_id,
          devEui: device.ids.dev_eui,
        }));
        setDevices(fetchedDevices);
      } catch (error) {
        console.error("Error fetching devices", error);
      }
    };
    fetchDevices();
  }, []);

  return (
    <div className="device-list">
      <h1>Device List</h1>
      {devices.length === 0 ? (
        <p>No devices found.</p>
      ) : (
        <ul>
          {devices.map((device) => (
            <li key={device.deviceId}>
              <p><strong>Device ID:</strong> {device.deviceId}</p>
              <p><strong>Device EUI:</strong> {device.devEui}</p>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default DeviceListPage;

