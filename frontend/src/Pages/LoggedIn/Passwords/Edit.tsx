import { useState } from "react";
import { User } from "../../../App";
import Logo from "../../../Components/Logo";
import { useParams, Link } from "react-router";
import { Password } from "./Main";
function EditPassword(props: {
	dark: boolean;
	user: User;
	getKey: () => string;
}) {
	const { passwordID } = useParams();
	const [passwordInfo, setPasswordInfo] = useState<Password>();
	const [error, setError] = useState("");
	//const navigate = useNavigate();
	const getPassword = () => {
		fetch(
			`/api/user/${
				props.user.user_id
			}/password/${passwordID}?key=${props.getKey()}`
		)
			.then((r) => r.json())
			.then((r) => {
				if (r.error) {
					switch (r.error) {
						default:
						case "USER_ID_INVALID":
							break;
						case "PASSWORD_ID_INVALID":
							setError("Password not found!");
							break;
					}
				} else {
					setPasswordInfo(r);
				}
			});
	};
	const editPassword = () => {
		console.log(passwordInfo);
		fetch(`/api/user/${props.user.user_id}/password/${passwordID}/edit`, {
			method: "PUT",
			body: JSON.stringify(passwordInfo)
		});
	};
	if (!passwordInfo) getPassword();
	return (
		<>
			<Logo dark={props.dark} />
			<h1>
				Edit Password Details {passwordInfo ? `- ${passwordInfo.name} ` : ""}
			</h1>
			<Link to="/user/passwords">{"<<"} Back to Passwords</Link>
			{passwordInfo ? (
				<>
					<form className="login">
						<label>
							Username <span className="red">(Required)</span>
						</label>
						<input
							type="text"
							placeholder="Enter your username"
							defaultValue={passwordInfo.username}
							required
							name="email"
							onInput={(v) => {
								passwordInfo.username = v.currentTarget.value;
								setPasswordInfo(passwordInfo);
							}}
						/>
						<label>
							Password <span className="red">(Required)</span>
						</label>
						<input
							type="password"
							placeholder="Enter your password"
							required
							name="password"
							onInput={(v) => {
								passwordInfo.decrypted = v.currentTarget.value;
								setPasswordInfo(passwordInfo);
							}}
						/>
						<label>
							Reference Name <span className="red">(Required)</span>
						</label>
						<input
							type="text"
							placeholder="Enter your reference name"
							defaultValue={passwordInfo.name}
							required
							name="name"
							onInput={(v) => {
								passwordInfo.name = v.currentTarget.value;
								setPasswordInfo(passwordInfo);
							}}
						/>
						<label>Website</label>
						<input
							type="text"
							placeholder="Enter your website"
							defaultValue={passwordInfo.website || undefined}
							name="website"
							onInput={(v) => {
								passwordInfo.website = v.currentTarget.value;
								setPasswordInfo(passwordInfo);
							}}
						/>
						<label>Folder Name</label>
						<input
							type="text"
							placeholder="Enter your folder name"
							defaultValue={passwordInfo.folder_name || undefined}
							name="folder"
							onInput={(v) => {
								passwordInfo.folder_name = v.currentTarget.value;
								setPasswordInfo(passwordInfo);
							}}
						/>
						<label>TOTP Secret</label>
						<input
							type="text"
							placeholder="Enter your TOTP secret"
							defaultValue={passwordInfo.totp_secret || undefined}
							name="totp_secret"
							onInput={(v) => {
								passwordInfo.totp_secret = v.currentTarget.value;
								setPasswordInfo(passwordInfo);
							}}
						/>
					</form>
					<button
						onClick={editPassword}
						disabled={
							!passwordInfo.decrypted || !passwordInfo.username || !passwordInfo.name
						}
					>
						Update Password
					</button>
				</>
			) : (
				<p>{error ? <span className="error">error</span> : "Loading..."}</p>
			)}
		</>
	);
}

export default EditPassword;
