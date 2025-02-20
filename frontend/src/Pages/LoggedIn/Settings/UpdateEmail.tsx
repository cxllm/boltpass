import { User } from "../../../App";
import Logo from "../../../Components/Logo";
// Currently a placeholder page until I create the real one.
function UpdateEmail(props: { dark: boolean; user: User; logout: () => void }) {
	return (
		<>
			<Logo dark={props.dark} />
			<h1>BoltPass Password Manager</h1>
			<p>The secure solution to your online needs</p>
		</>
	);
}

export default UpdateEmail;
