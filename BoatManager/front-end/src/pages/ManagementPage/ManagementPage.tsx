import React, { useState } from "react";
import { Box, Button, TextField, Alert, colors, Typography } from '@mui/material';
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
      setMessage("");

      const requestData = {
        deviceId,
        cognome,
        nome,
        targa
      };

      const response = await axios.post("http://127.0.0.1:5000/register", requestData, {
        headers: { "Content-Type": "application/json" }
      });

      console.log(response.data);

      // Update state with the response
      setDeviceId(response.data.deviceId);
      setDevEui(response.data.devEui);
      setAppKey(response.data.appKey);
      setMessage("Device added successfully!");
    } catch (error) {
      console.error("Error adding device", error);
      setMessage("Error adding device.");
    }
    setDeviceId("");
    setCognome("");
    setNome("");
    setTarga("");
  };

  return (
    <>
      <ContentWrapper>
        <NavBar />

        <FormWrapper>
          <Typography variant="h3" gutterBottom sx={{ color: "black", fontFamily: "sans-serif" }}>Register device</Typography>
          <Box component="form" sx={{
            display: "flex", flexWrap: "wrap", flexDirection: "column", justifyContent: "center",
            alignItems: "center",
          }}>

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
              onChange={(e) => setTarga(e.target.value)} sx={{ paddingBottom: "10%" }} />
          </Box>
          <Box component="div" sx={{ display: " flex", flexWrap: "wrap", flexDirection: "row", justifyContent: "space-between", }}>
            <Button variant="contained" sx={{ margin: "1rem" }} onClick={handleAddDevice} >Add device</Button>
          </Box>
        </FormWrapper>
        <Box component="div" sx={{ position: "relative", display: " flex", flexWrap: "wrap", flexDirection: "inherit", justifyContent: "space-between" }}>
          {<Alert>{message}test</Alert>}
          {<Alert>{"DevEui: " + devEui}</Alert>}
          {<Alert>{"Appkey: " + appKey}</Alert>}
        </Box>
      </ContentWrapper>

    </>
  );
};

export default ManagementPage;

