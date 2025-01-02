// 404 page
function NotFound(props: { dark: boolean }) {
	return (
		<>
			<img
				// pick which logo to use based on the theme chosen
				src={`/bolt-pass-${props.dark ? "light" : "dark"}.png`}
				className="logo"
				alt="BoltPass logo"
			/>
			<h1>Page Not Found</h1>
			<p className="not-found">
				The page {window.location.pathname} was not found on the server{" "}
				<a href="/">{"<<"} Go back home</a>
			</p>
		</>
	);
}

export default NotFound;
