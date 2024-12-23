import { Link } from "react-router";

function NotFound() {
	return (
		<>
			<div>
				<Link to="/">
					<img src="/Bolt%20Pass%20Dark.png" className="logo" alt="Vite logo" />
				</Link>
			</div>
			<h1>Page Not Found</h1>
			<Link to="../">Go back</Link>
		</>
	);
}

export default NotFound;
