import { useState } from "react";
import { User } from "../../../App";
import Logo from "../../../Components/Logo";
import {
	passwordRegex,
	lowercaseRegex,
	uppercaseRegex,
	numbersRegex,
	specialCharsRegex
} from "../../../regex";
import { FaCheck, FaTimes } from "react-icons/fa";
// Currently a placeholder page until I create the real one.
function UpdatePassword(props: {
	dark: boolean;
	user: User;
	logout: () => void;
}) {
	const [oldPassword, setOldPassword] = useState("");
	const [newPassword, setNewPassword] = useState("");
	const [passwordVerification, setPasswordVerification] = useState("");
	const [error, setError] = useState("");
	const [success, setSuccess] = useState(false);
	const updatePassword = () => {
		setError(
			"Please wait, this operation can take a long time. You will be logged out when it is complete"
		);
		fetch(`/api/user/${props.user.user_id}/password`, {
			method: "PUT",
			body: JSON.stringify({
				old: oldPassword,
				new: newPassword
			})
		})
			.then((r) => r.json())
			.then((r) => {
				if (r.error) {
					switch (r.error) {
						case "PASSWORD_NOT_CORRECT":
							setError("Incorrect password entered!");
							break;
						default:
							setError("Interval server error");
							break;
					}
				} else {
					if (r.success) {
						setSuccess(true);
						setTimeout(() => props.logout(), 3000);
					}
				}
			});
	};
	return (
		<>
			<Logo dark={props.dark} />
			<h1>Update Password</h1>
			<p>
				This operation may take a long time depending on how many passwords you have
				stored as every password must be updated and re-encrypted
			</p>
			{success ? (
				<>
					<h2 className="green">
						Your password has been updated. You will be logged out shortly.
					</h2>
					<p>
						Click <a onClick={props.logout}>here</a> to logout now
					</p>
				</>
			) : (
				<>
					{error ? <h2 className="red">{error}</h2> : ""}
					<form className="login">
						<label>Enter your old password: </label>
						<input
							type="password"
							placeholder="Enter your old password"
							required
							onInput={(v) => setOldPassword(v.currentTarget.value)}
						/>
						<label>Enter your new password: </label>
						<input
							type="password"
							placeholder="Enter your new password"
							required
							onInput={(v) => setNewPassword(v.currentTarget.value)}
						/>
						{
							// only display if anything has been entered
							newPassword != "" ? (
								newPassword == oldPassword ? (
									<span className="red">
										New password can't be the same as your old one!
									</span>
								) : // check if password is secure
								passwordRegex.test(newPassword) ? (
									<span className="green">Password is secure!</span>
								) : (
									// if it isn't secure, display the problems with it by testing it against individual regexes
									<>
										<span>
											Your password is not secure enough.
											<br />
											Requirements:
											<br />- Length 8:{" "}
											{newPassword.length >= 8 ? (
												<FaCheck className="green" />
											) : (
												<FaTimes className="red" />
											)}
											<br />- 1 lowercase letter:{" "}
											{lowercaseRegex.test(newPassword) ? (
												<FaCheck className="green" />
											) : (
												<FaTimes className="red" />
											)}
											<br />- 1 uppercase letter:{" "}
											{uppercaseRegex.test(newPassword) ? (
												<FaCheck className="green" />
											) : (
												<FaTimes className="red" />
											)}
											<br />- 1 number:{" "}
											{numbersRegex.test(newPassword) ? (
												<FaCheck className="green" />
											) : (
												<FaTimes className="red" />
											)}
											<br />- 1 special character:{" "}
											{specialCharsRegex.test(newPassword) ? (
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
						<label>Enter your new password again: </label>
						<input
							type="password"
							placeholder="Enter your new again password"
							required
							onInput={(v) => setPasswordVerification(v.currentTarget.value)}
						/>
						{
							// only display if anything has been entered
							passwordVerification != "" ? (
								// check if the two passwords match and display an error if not
								newPassword === passwordVerification ? (
									<span className="green">Passwords match!</span>
								) : (
									<span className="red">Passwords don't match</span>
								)
							) : (
								""
							)
						}
					</form>
					<button
						onClick={updatePassword}
						disabled={
							// only allow the user to sign up if the emails match, are valid and a password has been entered
							!(
								passwordRegex.test(newPassword) && newPassword === passwordVerification
							) ||
							!oldPassword ||
							oldPassword == newPassword
						}
					>
						Change Password
					</button>
				</>
			)}
		</>
	);
}

export default UpdatePassword;
