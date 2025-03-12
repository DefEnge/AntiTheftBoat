import React, { useState } from "react";
import { Box, Button, TextField, Alert } from '@mui/material';
import axios from "axios";
import { NavBar } from "../../components";
import { ContentWrapper, FormWrapper } from "../../components/Wrapper/style";

const ManagementPage: React.FC = () => {
  const [deviceId, setDeviceId] = useState<string>("");
  const [cognome, setCognome] = useState<string>("");
  const [nome, setNome] = useState<string>("");
  const [targa, setTarga] = useState<string>("");
  const [devEui, setDevEui] = useState<string>("");
  const [appKey, setAppKey] = useState<string>("");
  const [message, setMessage] = useState<string>("");

  const handleAddDevice = async () => {
    try {
      setDeviceId("");
      setDevEui("");
      setCognome("");
      setNome("");
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
    <>
      <NavBar />
      <ContentWrapper>
        <FormWrapper>
          <Box component="form" sx={{ display: "flex", flexWrap: "wrap", flexDirection: "column" }}>

            <TextField
              label="Device ID"
              placeholder="test-1234"
              value={deviceId}
              onChange={(e) => setDeviceId(e.target.value)}
              sx={{ paddingBottom: "10%" }}
            />

            <TextField
              label="Nome"
              placeholder="Mario"
              value={nome}
              onChange={(e) => setNome(e.target.value)}
              sx={{ paddingBottom: "10%" }}
            />

            <TextField
              label="Cognome"
              placeholder="Rossi"
              value={cognome}
              onChange={(e) => setCognome(e.target.value)}
              sx={{ paddingBottom: "10%" }}
            />

            <TextField
              label="Targa"
              placeholder="LV00000"
              value={targa}
              onChange={(e) => setTarga(e.target.value)}
              sx={{ paddingBottom: "10%" }}
            />



            <Box component="div" sx={{ display: " flex", flexWrap: "wrap", flexDirection: "row", justifyContent: "space-between", }}>
              <Button variant="contained" sx={{ margin: "1rem" }} onClick={handleAddDevice} >Add device</Button>
              <Button variant="contained" sx={{ margin: "1rem" }} onClick={handleDeleteDevice}>Delete device</Button>
            </Box>
          </Box>
        </FormWrapper>
        <Box component="div" sx={{ background: "", display: " flex", flexWrap: "wrap", flexDirection: "inherit", justifyContent: "space-between", minHeight: "14rem", paddingTop: "20%" }}>
          {message && <Alert>{message}</Alert>}
          {devEui && <Alert>{"DevEui: " + devEui}</Alert>}
          {appKey && <Alert>{"Appkey: " + appKey}</Alert>}
        </Box>
      </ContentWrapper>
    </>
  );
};

export default ManagementPage;

