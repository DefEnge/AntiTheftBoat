import React from "react";
import axios from "axios";
import { TextField, Button, Container, Typography, Box, Paper, Link } from "@mui/material";
import { useForm, SubmitHandler } from "react-hook-form";

interface LoginFormInputs {
	email: string;
	password: string;
}

const LoginPage: React.FC = () => {
	const {
		register,
		handleSubmit,
		formState: { errors },
	} = useForm<LoginFormInputs>();

	const onSubmit: SubmitHandler<LoginFormInputs> = async (data) => {
		try {
			const response = await axios.post("#", data);
			console.log("Login successful", response.data);
			// Handle successful login (e.g., save token, redirect user)
		} catch (error) {
			console.error("Login error", error);
			alert("Login failed. Please try again.");
		}
	};

	return (
		<Box sx={{ display: "flex", justifyContent: "center", alignItems: "center", height: "100vh", width: "100vw", padding: 2, boxSizing: "border-box" }}>

			<Container component="main" maxWidth="xs" sx={{ display: "flex", justifyContent: "center", alignItems: "center", minWidth: 0 }}>
				<Paper elevation={3} sx={{ padding: 4, textAlign: "center", width: "100%", maxWidth: 400, margin: "auto" }}>
					<Typography variant="h5" gutterBottom>
						Login
					</Typography>
					<Box component="form" onSubmit={handleSubmit(onSubmit)} sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
						<TextField
							fullWidth
							label="Email"
							{...register("email", { required: "Email is required" })}
							error={!!errors.email}
							helperText={errors.email?.message}
						/>
						<TextField
							fullWidth
							label="Password"
							type="password"
							{...register("password", { required: "Password is required" })}
							error={!!errors.password}
							helperText={errors.password?.message}
						/>
						<Button type="submit" variant="contained" fullWidth>
							Login
						</Button>
					</Box>
					<Box sx={{ display: "flex", justifyContent: "space-between", marginTop: 2, flexWrap: "wrap" }}>
						<Link href="#" variant="body2">
							Forgot password?
						</Link>
						<Link href="#" variant="body2">
							Don't have an account? Sign Up
						</Link>
					</Box>
				</Paper>
			</Container>
		</Box>
	);
};

export default LoginPage;

