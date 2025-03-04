import Logo from "../Components/Logo";
// Currently a placeholder home page until I create the real one.
function VerifyEmail(props: { dark: boolean }) {
	return (
		<>
			<Logo dark={props.dark} />
			<h1>Email Verification</h1>
			<p>
				Please check the inbox for the email you signed up with and follow the
				instructions. If you don't see an email, please ensure you check your
				junk/spam folder.
			</p>
		</>
	);
}

export default VerifyEmail;
