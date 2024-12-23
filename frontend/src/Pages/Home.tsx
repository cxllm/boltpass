function Home(props: { dark: boolean }) {
	return (
		<>
			<img
				src={`/bolt-pass-${props.dark ? "light" : "dark"}.png`}
				className="logo"
				alt="BoltPass logo"
			/>
			<h1>BoltPass Password Manager</h1>
		</>
	);
}

export default Home;
