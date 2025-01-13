import { useState } from "react";
import { FaCheck, FaTimes } from "react-icons/fa";
// Sign up page
function SignUp(props: { dark: boolean }) {
	// Regex to verify if an email is valid
	const emailRegex =
		/^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
	// Regex to verify if password is secure
	const passwordRegex =
		/^(?=.*[0-9])(?=.*[A-Z])(?=.*[a-z])(?=.*[^0-9A-Za-z]).{8,}$/;
	// Regexes to find the individual problems with a password (no lowercase, uppercase, numbers or special chars)
	const lowercaseRegex = /^.*[a-z]+.*$/;
	const uppercaseRegex = /^.*[A-Z]+.*$/;
	const numbersRegex = /^.*[0-9]+.*$/;
	const specialCharsRegex = /^.*[^0-9A-Za-z]+.*$/;
	// states for email, password and their verification steps, used to compare with regex and each other to ensure all data entered into the form is valid
	const [email, setEmail] = useState("");
	const [emailVerification, setEmailVerification] = useState("");
	const [password, setPassword] = useState("");
	const [passwordVerification, setPasswordVerification] = useState("");
	const [error, setError] = useState("");

	const signUp = () => {
		// PLACEHOLDER UNTIL FUNCTION IS COMPLETED
		fetch("http://localhost:3000/api/sign-up", {
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
					case "EMAIL_IN_USE":
						setError("The email entered is already in use!");
						break;
					case undefined:
						setError("");
						break;
					default:
						setError("Internal Server Error");
						break;
				}
			});
		console.log("Submitted Information: ");
		console.log("Email Address:", email);
		console.log("Password:", password);
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
			<h1>Create an account</h1>
			<form className="login">
				<label>Email: </label>
				<input
					type="email"
					placeholder="Enter your email address"
					required
					onInput={(v) => setEmail(v.currentTarget.value)}
				/>
				{
					// only display if anything has been entered
					email ? (
						// check if email is valid and display an error message if not
						emailRegex.test(email) ? (
							<span className="green">Email is valid!</span>
						) : (
							<span className="red">Email is not valid</span>
						)
					) : (
						""
					)
				}
				<label>Please confirm your email: </label>
				<input
					type="email"
					placeholder="Enter your email address again"
					required
					onInput={(v) => setEmailVerification(v.currentTarget.value)}
				/>
				{
					// only display if anything has been entered
					emailVerification ? (
						// check if emails match and display an error message if not
						email === emailVerification ? (
							<span className="green">Emails match!</span>
						) : (
							<span className="red">Emails do not match</span>
						)
					) : (
						""
					)
				}
				<label>Password: </label>

				<input
					type="password"
					placeholder="Enter your password"
					required
					onInput={(v) => setPassword(v.currentTarget.value)}
				/>
				{
					// only display if anything has been entered
					password != "" ? (
						// check if password is secure
						passwordRegex.test(password) ? (
							<span className="green">Password is secure!</span>
						) : (
							// if it isn't secure, display the problems with it by testing it against individual regexes
							<>
								<span>
									Your password is not secure enough.
									<br />
									Requirements:
									<br />- Length 8:{" "}
									{password.length >= 8 ? (
										<FaCheck className="green" />
									) : (
										<FaTimes className="red" />
									)}
									<br />- 1 lowercase letter:{" "}
									{lowercaseRegex.test(password) ? (
										<FaCheck className="green" />
									) : (
										<FaTimes className="red" />
									)}
									<br />- 1 uppercase letter:{" "}
									{uppercaseRegex.test(password) ? (
										<FaCheck className="green" />
									) : (
										<FaTimes className="red" />
									)}
									<br />- 1 number:{" "}
									{numbersRegex.test(password) ? (
										<FaCheck className="green" />
									) : (
										<FaTimes className="red" />
									)}
									<br />- 1 special character:{" "}
									{specialCharsRegex.test(password) ? (
										<FaCheck className="green" />
									) : (
										<FaTimes className="red" />
									)}
								</span>
							</>
						)
					) : (
						""
					)
				}
				<label>Please enter your password again: </label>
				<input
					type="password"
					placeholder="Enter your password"
					required
					onInput={(v) => setPasswordVerification(v.currentTarget.value)}
				/>
				{
					// only display if anything has been entered
					passwordVerification != "" ? (
						// check if the two passwords match and display an error if not
						password === passwordVerification ? (
							<span className="green">Passwords match!</span>
						) : (
							<span className="red">Passwords don't match</span>
						)
					) : (
						""
					)
				}
			</form>
			{error ? <span className="red">{error}</span> : ""}
			<button
				onClick={signUp}
				disabled={
					// only allow the user to sign up if the passwords and emails match and are both valid
					!(emailRegex.test(email) && email === emailVerification) ||
					!(passwordRegex.test(password) && password === passwordVerification)
				}
			>
				Sign Up
			</button>
		</>
	);
}

export default SignUp;
