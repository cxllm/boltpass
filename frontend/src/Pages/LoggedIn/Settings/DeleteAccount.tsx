import { useState } from "react";
import { User } from "../../../App";
import Logo from "../../../Components/Logo";

// Confirmation when user presses delete account on settings page
function DeleteAccount(props: {
	dark: boolean;
	user: User;
	logout: () => void;
}) {
	// Initialise states
	const [password, setPassword] = useState("");
	const [totpCode, setTotpCode] = useState("");
	const [recoveryCode, setRecoveryCode] = useState("");
	const [error, setError] = useState("");
	const [message, setMessage] = useState("");
	const deleteAccount = () => {
		// Delete the account using a DELETE request to the backend
		setError("Please wait...");
		fetch(
			`/api/user/${props.user.user_id}?password=${password}&${
				totpCode ? `totpCode=${totpCode}` : `recovery_code=${recoveryCode}`
			}`,
			{
				method: "DELETE"
			}
		)
			.then((r) => r.json())
			.then((r) => {
				if (r.error) {
					switch (r.error) {
						// inform user if their credentials are incorrect
						case "PASSWORD_NOT_CORRECT":
							setError("Incorrect password entered!");
							break;
						case "TOTP_CODE_NOT_CORRECT":
						case "RECOVERY_CODE_NOT_CORRECT":
							setError("Incorrect 2FA details entered");
							break;
						default:
							setError("Internal server error");
							break;
					}
				} else {
					// if there is no error log the user out and redirect
					if (r.success) {
						setError("");
						setMessage(
							"Your account has been successfully deleted, you will be redirected in 5 seconds"
						);
						setTimeout(() => {
							props.logout();
						}, 5000);
					}
				}
			});
	};
	return (
		<>
			<Logo dark={props.dark} />
			<h1>Delete Account</h1>
			<h2>Are you sure you want to delete your account?</h2>
			<p className="red">
				This action is irreversible and will take effect immediately!
			</p>
			<form
				className="styled-form"
				// allows the user to submit by pressing enter instead of pressing the button
				onSubmit={(e) => {
					e.preventDefault();
					if (
						password &&
						!(
							props.user.tfa_enabled &&
							totpCode.length != 6 &&
							recoveryCode.length != 8
						)
					) {
						deleteAccount();
					}
				}}
			>
				<label>
					<span className="red">
						Please confirm by entering your password{" "}
						{props.user.tfa_enabled
							? "and your two factor authentication details"
							: ""}
					</span>
				</label>
				{/* to confirm account deletion the user must enter their password and their 2FA details (if applicable) */}
				<input
					type="password"
					placeholder="Enter your password"
					required
					name="password"
					onInput={(v) => setPassword(v.currentTarget.value)}
				/>

				{props.user.tfa_enabled ? (
					// allow either a recovery code or TOTP code to be used
					<>
						{" "}
						<h3>Two-Factor Authentication</h3>
						<span className="red">
							Only <b>ONE</b> of the below options is required
						</span>
						<div className="grid">
							<div className="left">
								<label>Enter a one-time passcode</label>
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
								<label>Enter one of your recovery codes</label>
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
				)}
				<button
					type="submit"
					// only allow the account to be deleted if the user enters password and 2FA details where applicable
					disabled={
						!password ||
						(props.user.tfa_enabled &&
							totpCode.length != 6 &&
							recoveryCode.length != 8)
					}
				>
					Delete My Account
				</button>
			</form>

			{/* display error message or success message */}
			{error != "" ? <span className="red">{error}</span> : <></>}
			{message != "" ? <span className="green">{message}</span> : <></>}
		</>
	);
}

export default DeleteAccount;
