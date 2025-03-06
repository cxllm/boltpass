import { useState } from "react";
import { User } from "../../../App";
import Logo from "../../../Components/Logo";
import { useParams } from "react-router";
import { FaCopy, FaCheck } from "react-icons/fa6";

interface Password {
	decrypted: string;
	password_id: string;
	name: string;
	folder_name: string;
	website: string;
	username: string;
	totp_secret: string;
}
function ViewPassword(props: {
	dark: boolean;
	user: User;
	getKey: () => string;
}) {
	const { passwordID } = useParams();
	const [passwordInfo, setPasswordInfo] = useState<Password>();
	const [error, setError] = useState("");
	const [show, setShow] = useState(false);
	const [copiedUser, setCopiedUser] = useState(false);
	const [copiedPass, setCopiedPass] = useState(false);
	const [copiedCode, setCopiedCode] = useState(false);
	const [tfaCode, setTfaCode] = useState("");
	const getCodeValidTime = () => {
		return 30 - (Math.floor(Date.now() / 1000) % 30);
	};
	const [timeLeftOnCode, setTimeLeftOnCode] = useState<number>(
		getCodeValidTime()
	);
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
	const get2FACode = async () => {
		if (!passwordInfo?.totp_secret) {
			return null;
		}
		console.log(new Date().toTimeString());
		const data = await (
			await fetch(`/api/generate-totp-code?secret=${passwordInfo.totp_secret}`)
		).json();
		setTfaCode(data);
		setCopiedCode(false);
	};
	const copy = (value: string) => {
		navigator.clipboard.writeText(value);
	};
	if (!passwordInfo) getPassword();
	if (passwordInfo?.totp_secret && !tfaCode) {
		get2FACode(); // generate code on loading the website
		// The interval used in the timeout means that the code is refreshed whenever the next minute passes or the next 30 seconds past the minute passes
		setTimeout(() => {
			get2FACode();
			// set the interval after the timeout to be every 30 seconds, so on the minute and on 30 seconds past the minute
			setInterval(() => {
				get2FACode();
			}, 30000);
		}, getCodeValidTime() * 1000);

		setInterval(() => {
			setTimeLeftOnCode(getCodeValidTime());
		}, 1000);
	}
	return (
		<>
			<Logo dark={props.dark} />
			<h1>Password Details {passwordInfo ? `- ${passwordInfo.name} ` : ""}</h1>
			{passwordInfo ? (
				<>
					<div className="grid">
						<div className="left">
							<h2>Login Credentials</h2>
							<p>
								Username: <span>{passwordInfo.username}</span>{" "}
								<a
									onClick={() => {
										copy(passwordInfo.username);
										setCopiedUser(true);
									}}
								>
									{copiedUser ? <FaCheck /> : <FaCopy />}
								</a>
							</p>
							<p>
								Password: <span>{show ? passwordInfo.decrypted : "HIDDEN"}</span>{" "}
								<a
									onClick={() => {
										copy(passwordInfo.decrypted);
										setCopiedPass(true);
									}}
								>
									{copiedPass ? <FaCheck /> : <FaCopy />}
								</a>
							</p>
							<button onClick={() => setShow(!show)}>{show ? "Hide" : "Show"}</button>
						</div>
						<div className="right">
							<h2>Details</h2>
							<p>Name: {passwordInfo.name}</p>
							<p>Folder: {passwordInfo.folder_name || "None"}</p>
							<p>
								2FA Code:{" "}
								{tfaCode ? (
									<span>
										{tfaCode}{" "}
										<a
											onClick={() => {
												copy(tfaCode);
												setCopiedCode(true);
											}}
										>
											{copiedCode ? <FaCheck /> : <FaCopy />}
										</a>
										<br />
										<span className="red">
											Refreshes in {timeLeftOnCode} second{timeLeftOnCode != 1 ? "s" : ""}
										</span>
									</span>
								) : (
									"None"
								)}
							</p>
						</div>
					</div>
				</>
			) : (
				<h2>{error ? <span className="error">error</span> : "Loading..."}</h2>
			)}
		</>
	);
}

export default ViewPassword;
