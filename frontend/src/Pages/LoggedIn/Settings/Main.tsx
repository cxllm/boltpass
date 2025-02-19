import { User } from "../../../App";
import { useNavigate } from "react-router";
import Logo from "../../../Components/Logo";

// Currently a placeholder settings page until I create the real one.
function Settings(props: { dark: boolean; user: User }) {
	const navigate = useNavigate();
	return (
		<>
			<Logo dark={props.dark} />
			<h1>BoltPass Password Manager - Account Settings</h1>
			<div className="grid">
				<div>
					<h2>Change Email</h2>
					<p>Current Email: {props.user.email}</p>
					<button onClick={() => navigate("./email")}>Change Email</button>
				</div>
				<div>
					<h2>Change Password</h2>
					<p>This may take a few minutes.</p>
					<button onClick={() => navigate("./password")}>Change Password</button>
				</div>
				<div>
					<h2>Two-Factor Authentication</h2>
					<p>Active: {props.user.totp_enabled ? "Yes" : "No"}</p>
					<button onClick={() => navigate("./2fa")}>
						{props.user.totp_enabled ? "Disable" : "Enable"}
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
