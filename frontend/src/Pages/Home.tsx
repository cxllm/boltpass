// Currently a placeholder home page until I create the real one.
function Home(props: { dark: boolean }) {
	return (
		<>
			<img
				// pick which logo to use based on the theme chosen
				src={`/bolt-pass-${props.dark ? "light" : "dark"}.png`}
				className="logo"
				alt="BoltPass logo"
			/>
			<h1>BoltPass Password Manager</h1>
		</>
	);
}

export default Home;
