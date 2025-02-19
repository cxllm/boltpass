import { useState } from "react";
import { User } from "../../../App";
import { useNavigate } from "react-router";
import Logo from "../../../Components/Logo";

// Confirmation when user presses delete account on settings page
function DeleteAccount(props: {
	dark: boolean;
	user: User;
	logout: () => void;
}) {
	const [password, setPassword] = useState("");
	const [error, setError] = useState("");
	const [message, setMessage] = useState("");
	const navigate = useNavigate();
	const deleteAccount = () => {
		setMessage("Please wait...");
		fetch(`/api/user/${props.user.user_id}?password=${password}`, {
			method: "DELETE"
		})
			.then((r) => r.json())
			.then((r) => {
				switch (r.error) {
					case "PASSWORD_NOT_CORRECT":
						setError("Incorrect password entered!");
						break;
					case undefined:
						break;
					default:
						setError("Internal server error");
						break;
				}
				if (!r.error) {
					if (r.success) {
						setMessage(
							"Your account has been successfully deleted, you will be redirected in 5 seconds"
						);
						setTimeout(() => {
							props.logout();
							navigate("/");
						}, 5000);
					}
				}
			});
	};
	return (
		<>
			<Logo dark={props.dark} />
			<h1>BoltPass Password Manager - Delete Account</h1>
			<h2>Are you sure you want to delete your account?</h2>
			<p className="red">
				This action is irreversible and will take effect immediately!
			</p>
			<form className="login">
				<label>
					<span className="red">Please confirm by entering your password</span>
				</label>
				<input
					type="password"
					placeholder="Enter your password"
					required
					name="password"
					onInput={(v) => setPassword(v.currentTarget.value)}
				/>
			</form>
			<button disabled={!password} onClick={deleteAccount}>
				Delete My Account
			</button>
			{error != "" ? <span className="red">{error}</span> : <></>}
			{message != "" ? <span className="green">{message}</span> : <></>}
		</>
	);
}

export default DeleteAccount;
