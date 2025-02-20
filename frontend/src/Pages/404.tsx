import { Link } from "react-router";
import Logo from "../Components/Logo";
// 404 page
function NotFound(props: { dark: boolean }) {
	return (
		<>
			<Logo dark={props.dark} />
			<h1>Page Not Found</h1>
			<p className="not-found">
				The page {window.location.pathname} was not found on the server
				<br />
				<Link to="/">{"<<"} Go back home</Link>
			</p>
		</>
	);
}

export default NotFound;
