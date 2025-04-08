import React, { useState, useEffect } from "react";
import { Box, Typography, Card, CardContent, Grid, Chip, Alert } from '@mui/material';
import axios from "axios";
import { NavBar } from "../../components";
import { ContentWrapper } from "../../components/Wrapper/style";
import WarningIcon from '@mui/icons-material/Warning';

interface DeviceData {
    deviceId: string;
    username: string;
    targa: string;
    allerta: boolean;  // Corretto: allerta è direttamente nell'oggetto device
    status: number;
}

interface DeviceResponse {
    device: DeviceData;
}

const AlertPage: React.FC = () => {
    const [devices, setDevices] = useState<DeviceResponse[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string>("");

    // Fetch devices on component mount
    useEffect(() => {
        fetchDevices();

        // Set up polling to refresh data every 30 seconds
        const intervalId = setInterval(fetchDevices, 30000);

        // Clean up interval on component unmount
        return () => clearInterval(intervalId);
    }, []);

    const fetchDevices = async () => {
        try {
            setLoading(true);
            const response = await axios.post("http://127.0.0.1:5000/devices", { "AuthToken": localStorage.getItem("AuthToken") });

            // Filtra i dispositivi per mostrare solo quelli con allerta=true
            const alertDevices = response.data.filter((item: DeviceResponse) => item.device.allerta === true);

            setDevices(alertDevices);
            setError("");
        } catch (err) {
            console.error("Error fetching devices", err);
            setError("Impossibile caricare i dispositivi in allerta. Riprova più tardi.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <>
            <ContentWrapper>
                <NavBar />

                <Typography variant="h3" gutterBottom sx={{
                    color: "white",
                    fontFamily: "sans-serif",
                    margin: "2rem"
                }}>
                    Dispositivi in Allerta
                </Typography>

                {error && (
                    <Alert severity="error" sx={{ margin: "1rem 2rem" }}>{error}</Alert>
                )}

                {loading ? (
                    <Typography variant="body1" sx={{ margin: "2rem", color: "white" }}>
                        Caricamento dispositivi in allerta...
                    </Typography>
                ) : devices.length === 0 ? (
                    <Box sx={{
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                        justifyContent: 'center',
                        minHeight: '200px',
                        margin: '2rem',
                        padding: '2rem',
                        backgroundColor: 'rgba(255, 255, 255, 0.1)',
                        borderRadius: '8px'
                    }}>
                        <Typography variant="h5" sx={{ color: "white", marginBottom: "1rem" }}>
                            Nessun dispositivo in allerta
                        </Typography>
                        <Typography variant="body1" sx={{ color: "white" }}>
                            Al momento non ci sono dispositivi che richiedono attenzione.
                        </Typography>
                    </Box>
                ) : (
                    <Grid container spacing={3} sx={{ padding: "1rem 2rem" }}>
                        {/* Alert device cards */}
                        {devices.map((deviceItem) => (
                            <Grid item xs={12} sm={6} md={4} key={deviceItem.device.deviceId}>
                                <Card sx={{
                                    height: '100%',
                                    display: 'flex',
                                    flexDirection: 'column',
                                    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.5)',
                                    animation: 'blinkingBackground 2s infinite'
                                }}>
                                    <CardContent>
                                        <Box sx={{
                                            display: 'flex',
                                            justifyContent: 'space-between',
                                            alignItems: 'flex-start'
                                        }}>
                                            <Typography variant="h5" component="div" gutterBottom sx={{ color: 'white' }}>
                                                {deviceItem.device.deviceId}
                                            </Typography>
                                            <Box>
                                                <Chip
                                                    icon={<WarningIcon />}
                                                    label="ALLERTA"
                                                    color="error"
                                                    variant="filled"
                                                    sx={{ fontWeight: 'bold' }}
                                                />
                                            </Box>
                                        </Box>
                                        <Typography variant="body1" sx={{ color: 'white' }}>
                                            Utente: {deviceItem.device.username}
                                        </Typography>
                                        <Typography variant="body1" sx={{ color: 'white' }}>
                                            Targa: {deviceItem.device.targa}
                                        </Typography>
                                        <Typography
                                            variant="body1"
                                            sx={{
                                                color: 'white',
                                                fontWeight: 'bold',
                                                marginTop: '1rem'
                                            }}
                                        >
                                            STATO: IN ALLARME
                                        </Typography>
                                        <Typography
                                            variant="caption"
                                            sx={{
                                                color: 'rgba(255, 255, 255, 0.8)',
                                                display: 'block',
                                                marginTop: '0.5rem'
                                            }}
                                        >
                                            Ultimo aggiornamento: {new Date().toLocaleTimeString()}
                                        </Typography>
                                    </CardContent>
                                </Card>
                            </Grid>
                        ))}
                    </Grid>
                )}
            </ContentWrapper>

            {/* Add a style tag for the blinking animation */}
            <style jsx global>{`
                @keyframes blinkingBackground {
                    0% { background-color: rgba(255, 0, 0, 0.7); }
                    50% { background-color: rgba(255, 50, 50, 0.5); }
                    100% { background-color: rgba(255, 0, 0, 0.7); }
                }
            `}</style>
        </>
    );
};

export default AlertPage;
