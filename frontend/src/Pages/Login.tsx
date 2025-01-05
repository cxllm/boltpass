import { Link } from "react-router";

// Login page
function Login(props: { dark: boolean }) {
	return (
		<>
			<img
				// pick which logo to use based on the theme chosen
				src={`/bolt-pass-${props.dark ? "light" : "dark"}.png`}
				className="logo"
				alt="BoltPass logo"
			/>
			<h2>
				THIS PAGE IS CURRENTLY UNDER CONSTRUCTION AND WILL NOT FUNCTION AS EXPECTED
			</h2>
			<h1>Login</h1>
			<p>
				Don't have an account? <Link to="/sign-up">Create an account</Link>
			</p>
			<form className="login">
				<label htmlFor="email">E-Mail: </label>
				<input
					type="text"
					placeholder="Enter your e-mail address"
					required
					name="email"
				/>

				<label>Password: </label>
				<input
					type="password"
					placeholder="Enter your password"
					required
					name="password"
				/>
			</form>
			<button>Login</button>
		</>
	);
}

export default Login;
