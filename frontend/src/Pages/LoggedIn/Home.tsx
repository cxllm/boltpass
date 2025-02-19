import { User } from "../../App";
import Logo from "../../Components/Logo";

// Currently a placeholder home page until I create the real one.
function LoggedInHome(props: { dark: boolean; user: User }) {
	return (
		<>
			<Logo dark={props.dark} />
			<h1>BoltPass Password Manager</h1>
			<p>You are logged in as {props.user.email}</p>
		</>
	);
}

export default LoggedInHome;
