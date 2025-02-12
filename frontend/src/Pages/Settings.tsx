import { User } from "../App";

// Currently a placeholder settings page until I create the real one.
function Settings(props: { dark: boolean; user: User }) {
	return (
		<>
			<img
				// pick which logo to use based on the theme chosen
				src={`/bolt-pass-${props.dark ? "light" : "dark"}.png`}
				className="logo"
				alt="BoltPass logo"
			/>
			<h1>BoltPass Password Manager - Account Settings</h1>
			<h2>User Details</h2>
			<p>Email: {props.user.email}</p>
			<p>User ID: {props.user.user_id}</p>
			<h2>Two-Factor Authentication</h2>
			<p>Active: {props.user.totp_enabled ? "Yes" : "No"}</p>
		</>
	);
}

export default Settings;
