
import { Box, Typography, Button } from "@mui/material";
import { useNavigate } from "react-router-dom";

const Unauthorized = () => {
	const navigate = useNavigate();

	return (
		<Box
			sx={{
				display: "flex",
				flexDirection: "column",
				alignItems: "center",
				justifyContent: "center",
				height: "100vh",
				textAlign: "center",
			}}
		>
			<Typography variant="h3" color="error" sx={{ mb: 2 }}>
				403 - Access Denied
			</Typography>
			<Typography variant="body1" sx={{ mb: 3 }}>
				You do not have permission to view this page.
			</Typography>
			<Button variant="contained" color="primary" onClick={() => navigate("/")}>
				Go to Home
			</Button>
		</Box>
	);
};

export default Unauthorized;
