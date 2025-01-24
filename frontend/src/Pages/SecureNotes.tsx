import { User } from "../App";

// Currently a placeholder secure notes page until I create the real one.
function SecureNotes(props: { dark: boolean; user: User }) {
	return (
		<>
			<img
				// pick which logo to use based on the theme chosen
				src={`/bolt-pass-${props.dark ? "light" : "dark"}.png`}
				className="logo"
				alt="BoltPass logo"
			/>
			<h1>Your Secure Notes</h1>
			<p>You are logged in as {props.user.email}</p>
		</>
	);
}

export default SecureNotes;
