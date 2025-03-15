import { User } from "../../App";
import Logo from "../../Components/Logo";
import { Link } from "react-router";

// Logged in home page
function LoggedInHome(props: { dark: boolean; user: User }) {
	return (
		<>
			<Logo dark={props.dark} />
			<h1>BoltPass Password Manager</h1>
			<p>You are logged in as {props.user.email}</p>
			<p>
				BoltPass is a secure password manager that strives to make your online
				experience safer and more secure. To find out more about how it works,
				please visit our <Link to="/about">about page</Link>
			</p>
		</>
	);
}

export default LoggedInHome;
