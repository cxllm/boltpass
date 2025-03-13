import { useState } from "react";
import { User } from "../../../App";
import Logo from "../../../Components/Logo";
import { useParams, Link } from "react-router";
import { Password } from "./Main";
import { useNavigate } from "react-router";

// Page to allow user to edit a password in the database
function EditPassword(props: {
	dark: boolean;
	user: User;
	getKey: () => string;
}) {
	// Initialise states and get the password ID from parameteres
	const { passwordID } = useParams();
	const [passwordInfo, setPasswordInfo] = useState<Password>();
	const [error, setError] = useState("");
	const [requestSent, setRequestSent] = useState(false);
	const [initialPass, setInitialPass] = useState("");
	const navigate = useNavigate();
	const getPassword = () => {
		// Gets the password information
		fetch(
			`/api/user/${
				props.user.user_id
			}/password/${passwordID}?key=${props.getKey()}`
		)
			.then((r) => r.json())
			.then((r) => {
				if (r.error) {
					// Check for error
					switch (r.error) {
						default:
						case "USER_ID_INVALID":
							break;
						case "PASSWORD_ID_INVALID":
							setError("Password not found!");
							break;
					}
				} else {
					// Get info if no error
					setError("");
					setPasswordInfo(r);
					setInitialPass(r.decrypted);
				}
			});
	};
	const editPassword = () => {
		// Updates password in database with a PUT request
		setError("Updating password, please wait...");
		if (!requestSent) {
			setRequestSent(true);
			fetch(
				`/api/user/${
					props.user.user_id
				}/password/${passwordID}?key=${props.getKey()}`,
				{
					method: "PUT",
					// send the new password info
					body: JSON.stringify(passwordInfo)
				}
			)
				.then((r) => r.json())
				.then((r) => {
					// check for error, if not redirect to the password info page
					if (r.error) {
						setError("Internal server error");
					} else {
						navigate(`/user/passwords/${passwordID}`);
					}
				});
		}
	};
	// When the site is first opened, get the password details
	if (!passwordInfo) getPassword();
	return (
		<>
			<Logo dark={props.dark} />
			<h1>
				Edit Password Details {passwordInfo ? `- ${passwordInfo.name} ` : ""}
			</h1>
			<Link to={`/user/passwords/${passwordID}`}>
				{"<<"} Back to Password Details
			</Link>
			{
				// display any error
				error ? <span className="red">{error}</span> : ""
			}
			{
				// only show this if the password was found
				passwordInfo ? (
					<>
						<form
							className="styled-form"
							// allows the user to submit by pressing enter instead of pressing the button
							onSubmit={(e) => {
								e.preventDefault();
								if (
									passwordInfo.decrypted &&
									passwordInfo.username &&
									passwordInfo.name
								) {
									editPassword();
								}
							}}
						>
							<label>
								Username <span className="red">(Required)</span>
							</label>
							<input
								type="text"
								placeholder="Enter your username"
								defaultValue={passwordInfo.username}
								required
								name="email"
								onInput={(v) => {
									passwordInfo.username = v.currentTarget.value;
									setPasswordInfo(passwordInfo);
								}}
							/>
							<label>Password (Leave blank for no change)</label>
							<input
								type="password"
								placeholder="Enter your password"
								name="password"
								onInput={(v) => {
									passwordInfo.decrypted = v.currentTarget.value || initialPass;
									setPasswordInfo(passwordInfo);
								}}
							/>
							<label>
								Reference Name <span className="red">(Required)</span>
							</label>
							<input
								type="text"
								placeholder="Enter your reference name"
								defaultValue={passwordInfo.name}
								required
								name="name"
								onInput={(v) => {
									passwordInfo.name = v.currentTarget.value;
									setPasswordInfo(passwordInfo);
								}}
							/>
							<label>Website</label>
							<input
								type="text"
								placeholder="Enter your website"
								defaultValue={passwordInfo.website || undefined}
								name="website"
								onInput={(v) => {
									passwordInfo.website = v.currentTarget.value;
									setPasswordInfo(passwordInfo);
								}}
							/>
							<label>Folder Name</label>
							<input
								type="text"
								placeholder="Enter your folder name"
								defaultValue={passwordInfo.folder_name || undefined}
								name="folder"
								onInput={(v) => {
									passwordInfo.folder_name = v.currentTarget.value;
									setPasswordInfo(passwordInfo);
								}}
							/>
							<label>TOTP Secret</label>
							<input
								type="text"
								placeholder="Enter your TOTP secret"
								defaultValue={passwordInfo.totp_secret || undefined}
								name="totp_secret"
								onInput={(v) => {
									passwordInfo.totp_secret = v.currentTarget.value;
									setPasswordInfo(passwordInfo);
								}}
							/>
							<button
								type="submit"
								// ensure all the required fields are present
								disabled={
									!passwordInfo.decrypted || !passwordInfo.username || !passwordInfo.name
								}
							>
								Update Password
							</button>
						</form>
					</>
				) : (
					<p>Loading...</p>
				)
			}
		</>
	);
}

export default EditPassword;
