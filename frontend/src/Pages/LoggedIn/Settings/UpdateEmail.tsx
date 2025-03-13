import { User } from "../../../App";
import Logo from "../../../Components/Logo";
import { useState } from "react";
import { emailRegex } from "../../../regex.tsx";

// Page to allow user to update their email
function UpdateEmail(props: { dark: boolean; user: User; logout: () => void }) {
	// initialise state
	const [email, setEmail] = useState("");
	const [emailVerification, setEmailVerification] = useState("");
	const [password, setPassword] = useState("");
	const [error, setError] = useState("");
	const [success, setSuccess] = useState(false);
	const [loggedOut, setLoggedOut] = useState(false);
	const updateEmail = () => {
		// Update email using a PUT request to the server
		setError("Please wait...");
		fetch(`/api/user/${props.user.user_id}/update-email?password=${password}`, {
			method: "PUT",
			body: JSON.stringify({
				email
			})
		})
			.then((r) => r.json())
			.then((r) => {
				if (r.error) {
					switch (r.error) {
						// Let user know if their password is wrong or if the email is already being used by someone else
						case "PASSWORD_NOT_CORRECT":
							setError("Incorrect password entered!");
							break;
						case "EMAIL_IN_USE":
							setError("This email is already in use!");
							break;
						default:
							setError("Internal server error");
							break;
					}
				} else if (r.success) {
					setError("");
					setSuccess(true);
					setTimeout(() => {
						if (!loggedOut) props.logout();
					}, 15000);
				}
			});
	};
	return (
		<>
			<Logo dark={props.dark} />
			<h1>Update Email Address</h1>
			{success ? (
				// display a message explaining what will happen now the email has changed
				<>
					<h2 className="green">
						Your email address has been changed to {email}. You will be logged out in
						15 seconds. To log in again, please verify your email address by following
						the instructions sent to your inbox and enter your credentials on the
						login page.
					</h2>
					<p>
						Click{" "}
						<a
							onClick={() => {
								setLoggedOut(true);
								props.logout();
							}}
						>
							here
						</a>{" "}
						to logout now
					</p>
				</>
			) : (
				<>
					<form
						className="styled-form"
						// allows the user to submit by pressing enter instead of pressing the button
						onSubmit={(e) => {
							e.preventDefault();
							if (
								emailRegex.test(email) &&
								email === emailVerification &&
								password &&
								props.user.email != email
							) {
								updateEmail();
							}
						}}
					>
						<label>Enter your new email (this will be verified): </label>
						<input
							type="email"
							placeholder="Enter your email address"
							required
							onInput={(v) => setEmail(v.currentTarget.value)}
						/>
						{
							// only display if anything has been entered
							email ? (
								email == props.user.email ? (
									<span className="red">
										Your new email can't be the same as your old one!
									</span>
								) : // check if email is valid and display an error message if not
								emailRegex.test(email) ? (
									<span className="green">Email is valid!</span>
								) : (
									<span className="red">Email is not valid</span>
								)
							) : (
								""
							)
						}
						<label>Please confirm your new email: </label>
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
						<button
							type="submit"
							disabled={
								// only allow the user to sign up if the emails match, are valid and a password has been entered
								!(emailRegex.test(email) && email === emailVerification) ||
								!password ||
								email == props.user.email
							}
						>
							Change Email Address
						</button>
					</form>
					{error ? <span className="red">{error}</span> : ""}{" "}
				</>
			)}
		</>
	);
}

export default UpdateEmail;
