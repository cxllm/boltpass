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
				<a href="/">{"<<"} Go back home</a>
			</p>
		</>
	);
}

export default NotFound;
