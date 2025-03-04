import { User } from "../../../App";
import { useNavigate } from "react-router";
import Logo from "../../../Components/Logo";

// Currently a placeholder settings page until I create the real one.
function Settings(props: { dark: boolean; user: User }) {
	const navigate = useNavigate();
	return (
		<>
			<Logo dark={props.dark} />
			<h1>Account Settings</h1>
			<div className="grid">
				<div>
					<h2>Change Email Address</h2>
					<p>Update your account's email for logging in and contact</p>
					<p>Current Email Address: {props.user.email}</p>
					<button onClick={() => navigate("./email")}>Change Email Address</button>
				</div>
				<div>
					<h2>Change Password</h2>
					<p>Update your master password to access your account</p>
					<p>This may take a few minutes.</p>
					<button onClick={() => navigate("./password")}>Change Password</button>
				</div>
				<div>
					<h2>Two-Factor Authentication</h2>
					<p>An additional layer of security on your account</p>
					<p>Active: {props.user.tfa_enabled ? "Yes" : "No"}</p>
					<button onClick={() => navigate("./2fa")}>
						{props.user.tfa_enabled ? "Disable" : "Enable"}
					</button>
				</div>
				<div>
					<h2>Delete Account</h2>
					<p>
						Delete your account and all the data associated with it
						<br />
						<span className="red">This action is irreversible!</span>
					</p>
					<button onClick={() => navigate("./delete")}>Delete Account</button>
				</div>
			</div>
		</>
	);
}

export default Settings;
