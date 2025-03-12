import { useState, useEffect } from "react";
import { User } from "../../../App";
import Logo from "../../../Components/Logo";
import { useParams, useNavigate, Link } from "react-router";
import { FaCopy, FaCheck } from "react-icons/fa6";
import { Password } from "./Main";

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
	const [deletePressed, setDeletePressed] = useState(0);
	const navigate = useNavigate();
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
	const deletePassword = () => {
		fetch(
			`/api/user/${
				props.user.user_id
			}/password/${passwordID}?key=${props.getKey()}`,
			{
				method: "DELETE"
			}
		)
			.then((r) => r.json())
			.then((r) => {
				if (r.error) {
					setError("Internal server error");
				} else {
					if (r) {
						navigate("/user/passwords");
					}
				}
			});
	};
	const get2FACode = async () => {
		if (!passwordInfo?.totp_secret) {
			return null;
		}
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
	// generate code on loading the website
	if (passwordInfo?.totp_secret && !tfaCode) get2FACode();
	// deactivates the intervals when the user leaves the page
	useEffect(() => {
		// The interval used in the timeout means that the code is refreshed whenever the next minute passes or the next 30 seconds past the minute passes
		let interval1: number;
		const timer: number = setTimeout(() => {
			get2FACode();
			// set the interval after the timeout to be every 30 seconds, so on the minute and on 30 seconds past the minute
			interval1 = setInterval(() => {
				get2FACode();
			}, 30000);
		}, getCodeValidTime() * 1000);

		const interval2: number = setInterval(() => {
			setTimeLeftOnCode(getCodeValidTime());
		}, 1000);
		return () => {
			// clear the intevarls when the user leaves
			clearTimeout(timer);
			clearInterval(interval1);
			clearInterval(interval2);
		};
	});

	return (
		<>
			<Logo dark={props.dark} />
			<h1>Password Details {passwordInfo ? `- ${passwordInfo.name} ` : ""}</h1>
			<Link to="/user/passwords">{"<<"} Back to Passwords</Link>
			{passwordInfo ? (
				<>
					<div className="grid">
						<div className="full-length">
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
								</a>{" "}
								<a onClick={() => setShow(!show)}>{show ? "Hide" : "Show"}</a>
							</p>
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
										</a>{" "}
										<span className="red">
											Refreshes in {timeLeftOnCode} second{timeLeftOnCode != 1 ? "s" : ""}
										</span>
									</span>
								) : (
									"None"
								)}
							</p>
						</div>
						<div className="left">
							<h2>Details</h2>
							<p>Name: {passwordInfo.name}</p>
							<p>
								Folder:{" "}
								{passwordInfo.folder_name ? (
									<Link to={`/user/passwords/folder/${passwordInfo.folder_name}`}>
										{passwordInfo.folder_name}
									</Link>
								) : (
									"None"
								)}
							</p>
							<p>Website: {passwordInfo.website || "None"}</p>
						</div>
						<div className="right">
							<h2>Security</h2>
							<p>
								{passwordInfo.leaked > 0 || passwordInfo.reused > 1 ? (
									<span className="red">
										You should change your password! See below for details
									</span>
								) : (
									<span className="green">
										Your password is secure! See below for details
									</span>
								)}
							</p>
							<p>
								This password has been leaked{" "}
								{passwordInfo.leaked == 0 ? (
									<span className="green">0 times</span>
								) : (
									<span className="red">
										{passwordInfo.leaked} time{passwordInfo.leaked == 1 ? "" : "s"}
									</span>
								)}
							</p>
							<p>
								You have reused this password{" "}
								{passwordInfo.reused == 0 ? (
									<span className="green">0 times</span>
								) : (
									<span className="red">
										{passwordInfo.reused} time{passwordInfo.reused == 1 ? "" : "s"}
									</span>
								)}{" "}
							</p>
							{passwordInfo.reused > 0 ? (
								<p>
									To see which other entries use this password, click{" "}
									<Link to={`/user/passwords/${passwordID}/reused`}>here</Link>
								</p>
							) : (
								""
							)}
						</div>
					</div>
					<div className="buttons">
						<button onClick={() => navigate(`/user/passwords/${passwordID}/edit`)}>
							Edit Password
						</button>

						<button
							className="red-button"
							onClick={() => {
								if (deletePressed == 1) {
									deletePassword();
								}
								setDeletePressed(deletePressed + 1);
							}}
						>
							{deletePressed == 1
								? "Are you sure? Press again to confirm"
								: deletePressed == 0
								? "Delete this password"
								: "Deleting password..."}
						</button>
						<br />
					</div>
				</>
			) : (
				<p>{error ? <span className="error">error</span> : "Loading..."}</p>
			)}
		</>
	);
}

export default ViewPassword;
