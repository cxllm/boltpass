import { Link, useNavigate } from "react-router";
import Logo from "../Components/Logo";
// The page that shows when a user verifies their email
function EmailVerifed(props: { dark: boolean }) {
	const navigate = useNavigate();
	// redirect after 5 seconds
	setTimeout(() => {
		navigate("/login");
	}, 5000);
	return (
		<>
			<Logo dark={props.dark} />
			<h1>Your Email Address has been verified!</h1>
			<p>
				You will now be redirected to the login page. If this does not work, please
				press <Link to="/login">here</Link>
			</p>
		</>
	);
}

export default EmailVerifed;
