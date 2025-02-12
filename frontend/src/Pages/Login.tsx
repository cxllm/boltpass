import { Link, useNavigate } from "react-router";
import { useState } from "react";

// Login page
function Login(props: {
	dark: boolean;
	login: (userID: string, key: string) => void;
}) {
	// Regex to verify if an email is valid
	const emailRegex =
		/^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
	// states for storing email, password and totp codes
	const [email, setEmail] = useState("");
	const [password, setPassword] = useState("");
	const [error, setError] = useState("");
	const [totp, setTotp] = useState(false);
	const [totpCode, setTotpCode] = useState(0);
	const navigate = useNavigate();
	const login = () => {
		fetch(`/api/login?email=${email}&password=${password}`)
			.then((r) => r.json())
			.then((r) => {
				// Display relevant error message
				switch (r.error) {
					case "EMAIL_NOT_REGISTERED":
					case "PASSWORD_NOT_CORRECT":
						setError("The email and password combination is incorrect!");
						break;
					case undefined:
						setError("");
						break;
					default:
						setError("Internal Server Error");
						break;
				}
				// Check if it is a valid combination
				if (r.key && r.user_id) {
					// Check if the user has 2FA enabled, and if they do, require it to be completed
					if (r.totp_enabled && !totp) {
						setTotp(true);
					}
					// the function is called again after the user enters their totp details, so in this case, log them in if the code matches
					else if (totp) {
						// display the relevant error message
						if (totpCode.toString().length != 6) {
							setError("Invalid TOTP code entered");
						} else {
							fetch(`/api/verify-totp?secret=${r.totp_secret}&code=${totpCode}`)
								.then((s) => s.json())
								.then((s) => {
									switch (s.error) {
										// display the relevant error message
										case undefined:
											setError("");
											break;
										default:
											setError("Internal Server Error");
											break;
									}
									// if the code is valid, log the user in
									if (s == true) {
										props.login(r.user_id, r.key);
										navigate("/");
									} else {
										// if the code is invalid, show an error
										setError("Invalid TOTP code entered!");
									}
								});
						}
					} else {
						// if no 2FA, just log the user in
						props.login(r.user_id, r.key);
						navigate("/");
					}
				}
			});
	};
	return (
		<>
			<img
				// pick which logo to use based on the theme chosen
				src={`/bolt-pass-${props.dark ? "light" : "dark"}.png`}
				className="logo"
				alt="BoltPass logo"
			/>
			<h1>Login</h1>
			<p>
				Don't have an account? <Link to="/sign-up">Sign up</Link>
			</p>
			<form className="login">
				<label htmlFor="email">Email: </label>
				<input
					type="text"
					placeholder="Enter your email address"
					required
					name="email"
					onInput={(v) => setEmail(v.currentTarget.value)}
				/>
				{email != "" && !emailRegex.test(email) ? (
					<span className="red">Invalid email address entered!</span>
				) : (
					""
				)}

				<label>Password: </label>
				<input
					type="password"
					placeholder="Enter your password"
					required
					name="password"
					onInput={(v) => setPassword(v.currentTarget.value)}
				/>
				{
					//only show if 2FA is enabled
					totp ? (
						<>
							<label>
								<span className="red">Two-Factor Authentication Code Required</span>
							</label>
							<input
								type="number"
								placeholder="Enter your 2FA code"
								maxLength={6}
								minLength={6}
								required
								name="input"
								onInput={(v) => setTotpCode(Number(v.currentTarget.value))}
							/>
						</>
					) : (
						""
					)
				}
			</form>
			{error ? <span className="red">{error}</span> : ""}
			<button
				onClick={login}
				disabled={
					// only allow the user to login if email is valid and password exists, and if totp has been entered (where relevant)
					!emailRegex.test(email) ||
					!password ||
					(totp && totpCode.toString().length != 6)
				}
			>
				Login
			</button>
		</>
	);
}

export default Login;
