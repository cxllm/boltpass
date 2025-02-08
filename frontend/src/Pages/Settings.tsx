import { User } from "../App";

// Currently a placeholder home page until I create the real one.
function Settings(props: { dark: boolean; user: User }) {
	return (
		<>
			<img
				// pick which logo to use based on the theme chosen
				src={`/bolt-pass-${props.dark ? "light" : "dark"}.png`}
				className="logo"
				alt="BoltPass logo"
			/>
			<h1>BoltPass Password Manager</h1>
			<p>You are logged in as {props.user.email}</p>
			<h2>Enable 2FA</h2>
		</>
	);
}

export default Settings;
