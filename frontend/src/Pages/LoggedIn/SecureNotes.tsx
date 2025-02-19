import { User } from "../../App";
import Logo from "../../Components/Logo";

// Currently a placeholder secure notes page until I create the real one.
function SecureNotes(props: { dark: boolean; user: User }) {
	return (
		<>
			<Logo dark={props.dark} />
			<h1>Your Secure Notes</h1>
			<p>You are logged in as {props.user.email}</p>
		</>
	);
}

export default SecureNotes;
