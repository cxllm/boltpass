import { Link } from "react-router";
import Logo from "../Components/Logo";
// Currently a placeholder home page until I create the real one.
function Home(props: { dark: boolean }) {
	return (
		<>
			<Logo dark={props.dark} />
			<h1>BoltPass Password Manager</h1>
			<p>
				BoltPass is a secure password manager that strives to make your online
				experience safer and more secure. To find out more about how it works,
				please visit our <Link to="/about">about page</Link>
			</p>
		</>
	);
}

export default Home;
