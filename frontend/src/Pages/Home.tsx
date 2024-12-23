function Home(props: { dark: boolean }) {
	return (
		<>
			<img
				src={`/Bolt%20Pass%20${props.dark ? "Light" : "Dark"}.png`}
				className="logo"
				alt="BoltPass logo"
			/>
			<h1>BoltPass Password Manager</h1>
		</>
	);
}

export default Home;
