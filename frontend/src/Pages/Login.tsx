import { Link } from "react-router";
import { useState } from "react";

// Login page
function Login(props: { dark: boolean }) {
	// Regex to verify if an email is valid
	const emailRegex =
		/^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
	// states for storing email and password
	const [email, setEmail] = useState("");
	const [password, setPassword] = useState("");
	const [error, setError] = useState("");
	const login = () => {
		fetch("/api/login", {
			method: "POST",
			body: JSON.stringify({
				email: email,
				password: password
			}),
			headers: {
				"Content-Type": "application/json"
			}
		})
			.then((r) => r.json())
			.then((r) => {
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
				console.log(r);
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
			<h2>
				THIS PAGE IS CURRENTLY UNDER CONSTRUCTION AND WILL NOT FUNCTION AS EXPECTED
			</h2>
			<h1>Login</h1>
			<p>
				Don't have an account? <Link to="/sign-up">Create an account</Link>
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
			</form>
			{error ? <span className="red">{error}</span> : ""}
			<button
				onClick={login}
				disabled={
					// only allow the user to login if email is valid and password exists
					!emailRegex.test(email) || !password
				}
			>
				Login
			</button>
		</>
	);
}

export default Login;
