import { useState } from "react";
import { User } from "../../../App";
import Logo from "../../../Components/Logo";
import { useNavigate } from "react-router";

function AddPassword(props: {
	dark: boolean;
	user: User;
	getKey: () => string;
}) {
	const [password, setPassword] = useState("");
	const [username, setUsername] = useState("");
	const [name, setName] = useState("");
	const [website, setWebsite] = useState("");
	const [totpSecret, setTotpSecret] = useState("");
	const [folder, setFolder] = useState("");
	const [error, setError] = useState("");
	const navigate = useNavigate();
	const addPassword = () => {
		setError("Please wait");
		fetch(`/api/user/${props.user.user_id}/password?key=${props.getKey()}`, {
			method: "POST",
			body: JSON.stringify({
				password,
				username,
				name,
				website,
				totp_secret: totpSecret,
				folder_name: folder
			})
		})
			.then((r) => r.json())
			.then((r) => {
				if (r.error) {
					setError("Internal server error");
				} else {
					return navigate(`/user/passwords/${r.password_id}`);
				}
			});
	};
	return (
		<>
			<Logo dark={props.dark} />
			<h1>Add a Password</h1>
			<form className="login">
				<label>
					Username <span className="red">(Required)</span>
				</label>
				<input
					type="text"
					placeholder="Enter your username"
					required
					name="email"
					onInput={(v) => setUsername(v.currentTarget.value)}
				/>

				<label>
					Password <span className="red">(Required)</span>
				</label>
				<input
					type="password"
					placeholder="Enter your password"
					required
					name="password"
					onInput={(v) => setPassword(v.currentTarget.value)}
				/>
				<label>
					Reference Name <span className="red">(Required)</span>
				</label>
				<input
					type="text"
					placeholder="Enter your reference name"
					required
					name="name"
					onInput={(v) => setName(v.currentTarget.value)}
				/>
				<label>Website</label>
				<input
					type="text"
					placeholder="Enter your website"
					name="website"
					onInput={(v) => setWebsite(v.currentTarget.value)}
				/>
				<label>Folder Name</label>
				<input
					type="text"
					placeholder="Enter your folder name"
					name="folder"
					onInput={(v) => setFolder(v.currentTarget.value)}
				/>
				<label>TOTP Secret</label>
				<input
					type="text"
					placeholder="Enter your TOTP secret"
					name="totp_secret"
					onInput={(v) => setTotpSecret(v.currentTarget.value)}
				/>
			</form>
			<button onClick={addPassword} disabled={!password || !username || !name}>
				Add Password
			</button>
			{error ? <span className="red">{error}</span> : ""}
		</>
	);
}

export default AddPassword;
