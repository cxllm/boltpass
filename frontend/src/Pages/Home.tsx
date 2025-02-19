import Logo from "../Components/Logo";
// Currently a placeholder home page until I create the real one.
function Home(props: { dark: boolean }) {
	return (
		<>
			<Logo dark={props.dark} />
			<h1>BoltPass Password Manager</h1>
			<p>The secure solution to your online needs</p>
		</>
	);
}

export default Home;
