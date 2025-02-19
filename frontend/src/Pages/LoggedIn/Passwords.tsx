import { User } from "../../App";
import Logo from "../../Components/Logo";

// Currently a placeholder passwords page until I create the real one.
function Passwords(props: { dark: boolean; user: User }) {
	return (
		<>
			<Logo dark={props.dark} />
			<h1>Your Passwords</h1>
			<p>You are logged in as {props.user.email}</p>
		</>
	);
}

export default Passwords;
