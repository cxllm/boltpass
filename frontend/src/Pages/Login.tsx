import { Link, useNavigate } from "react-router";
import { useState } from "react";
import Logo from "../Components/Logo";

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
	const [totpCode, setTotpCode] = useState("");
	const [recoveryCode, setRecoveryCode] = useState("");
	const navigate = useNavigate();
	const login = () => {
		setError("Please wait...");
		fetch(`/api/login?email=${email}&password=${password}`)
			.then((r) => r.json())
			.then((r) => {
				if (r.error) {
					// Display relevant error message
					switch (r.error) {
						case "EMAIL_NOT_REGISTERED":
						case "PASSWORD_NOT_CORRECT":
							setError("The email and password combination is incorrect!");
							break;
						case "USER_EMAIL_NOT_VERIFIED":
							navigate("/verify-email");
							break;
						default:
							setError("Internal Server Error");
							break;
					}
				}
				// Check if it is a valid combination
				else if (r.key && r.user_id) {
					// Check if the user has 2FA enabled, and if they do, require it to be completed
					if (r.tfa_enabled && !totp && !recoveryCode) {
						setError("");
						setTotp(true);
					}
					// the function is called again after the user enters their totp details, so in this case, log them in if the code matches
					else if (totp && totpCode) {
						// display the relevant error message
						if (totpCode.length != 6) {
							setError("Invalid TOTP code entered");
						} else {
							fetch(`/api/verify-totp?secret=${r.totp_secret}&code=${totpCode}`)
								.then((s) => s.json())
								.then((s) => {
									if (s.error) {
										setError("Internal Server Error");
									} else setError("");
									// if the code is valid, log the user in
									if (s == true) {
										props.login(r.user_id, r.key);
									} else {
										// if the code is invalid, show an error
										setError("Invalid TOTP code entered!");
									}
								});
						}
					} else if (totp && recoveryCode) {
						fetch(
							`/api/user/${r.user_id}/verify-recovery-code?password=${password}&recovery_code=${recoveryCode}`
						)
							.then((r) => r.json())
							.then((s) => {
								if (s.error) {
									switch (s.error) {
										case "PASSWORD_NOT_CORRECT":
											setError("Incorrect password entered!");
											break;
										default:
											setError("Internal Server Error");
									}
								} else setError("");

								if (s == true) {
									props.login(r.user_id, r.key);
								} else {
									setError("Invalid recovery code entered!");
								}
							});
					} else {
						// if no 2FA, just log the user in
						props.login(r.user_id, r.key);
					}
				}
			});
	};
	return (
		<>
			<Logo dark={props.dark} />
			<h1>Login</h1>
			<p>
				Don't have an account? <Link to="/sign-up">Sign up</Link>
			</p>
			<form
				className="styled-form"
				onSubmit={(e) => {
					e.preventDefault();
					if (
						emailRegex.test(email) &&
						password &&
						!(totp && totpCode.length != 6 && recoveryCode.length != 8)
					) {
						login();
					}
				}}
			>
				<label htmlFor="email">Email: </label>
				<input
					type="text"
					placeholder="Enter your email address"
					required
					readOnly={totp}
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
					readOnly={totp}
					onInput={(v) => setPassword(v.currentTarget.value)}
				/>
				{
					//only show if 2FA is enabled
					totp ? (
						<>
							<h3>Two-Factor Authentication</h3>
							<span className="red">
								Only <b>ONE</b> of the below options is required
							</span>
							<div className="grid">
								<div className="left">
									<label>Enter a one-time passcode (6 numbers)</label>
									<input
										type="number"
										placeholder="Enter your OTP"
										minLength={6}
										maxLength={6}
										name="passcode"
										onInput={(v) => setTotpCode(v.currentTarget.value)}
									/>
								</div>
								<div className="right">
									<label>Enter a recovery code (8 alphanumeric chars)</label>
									<input
										type="text"
										placeholder="Enter your recovery code"
										minLength={8}
										maxLength={8}
										name="recovery"
										onInput={(v) => setRecoveryCode(v.currentTarget.value)}
									/>
								</div>
							</div>
						</>
					) : (
						""
					)
				}
				<button
					type="submit"
					disabled={
						// only allow the user to login if email is valid and password exists, and if totp has been entered (where relevant)
						!emailRegex.test(email) ||
						!password ||
						(totp && totpCode.length != 6 && recoveryCode.length != 8)
					}
				>
					Login
				</button>
			</form>
			{error ? <span className="red">{error}</span> : ""}
		</>
	);
}

export default Login;
