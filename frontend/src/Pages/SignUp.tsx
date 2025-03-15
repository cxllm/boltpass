import { useState } from "react";
import { FaCheck, FaTimes } from "react-icons/fa";
import { Link, useNavigate } from "react-router";
import Logo from "../Components/Logo";
import { emailRegex, passwordRegex } from "../regex.tsx";
// Sign up page
function SignUp(props: {
	dark: boolean;
	login: (userID: string, key: string) => void;
}) {
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
	const navigate = useNavigate();

	const signUp = () => {
		setError("Please wait...");
		fetch("/api/sign-up", {
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
				if (r.error) {
					// Display relevant error message
					switch (r.error) {
						case "EMAIL_IN_USE":
							setError("The email entered is already in use!");
							break;
						default:
							setError("Internal Server Error");
							break;
					}
				} else setError("");
				// log the user in if it is a valid combination
				if (r.key && r.user_id) {
					navigate("/verify-email");
				}
			});
	};
	return (
		<>
			<Logo dark={props.dark} />
			<h1>Create an account</h1>
			<p>
				Already have an account? <Link to="/login">Login</Link>
			</p>
			<p className="red">
				If you forgot your password, you will not be able to reset it due to the
				nature of how passwords are stored, so make sure it is something memorable
				or that you keep it somewhere safe.
			</p>
			<form
				className="styled-form"
				onSubmit={(e) => {
					e.preventDefault();
					if (
						emailRegex.test(email) &&
						email === emailVerification &&
						passwordRegex.test(password) &&
						password === passwordVerification
					) {
						signUp();
					}
				}}
			>
				<label>Email (this will be verified): </label>
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
				<button
					type="submit"
					disabled={
						// only allow the user to sign up if the passwords and emails match and are both valid
						!(emailRegex.test(email) && email === emailVerification) ||
						!(passwordRegex.test(password) && password === passwordVerification)
					}
				>
					Sign Up
				</button>
			</form>
			{error ? <span className="red">{error}</span> : ""}
		</>
	);
}

export default SignUp;
