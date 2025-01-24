import { User } from "../App";

// Currently a placeholder passwords page until I create the real one.
function Passwords(props: { dark: boolean; user: User }) {
	return (
		<>
			<img
				// pick which logo to use based on the theme chosen
				src={`/bolt-pass-${props.dark ? "light" : "dark"}.png`}
				className="logo"
				alt="BoltPass logo"
			/>
			<h1>Your Passwords</h1>
			<p>You are logged in as {props.user.email}</p>
		</>
	);
}

export default Passwords;
