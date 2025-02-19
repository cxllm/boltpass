function Logo(props: { dark: boolean }) {
	return (
		<img
			// pick which logo to use based on the theme chosen
			src={`/bolt-pass-${props.dark ? "light" : "dark"}.png`}
			className="logo"
			alt="BoltPass logo"
		/>
	);
}

export default Logo;
