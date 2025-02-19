import { useState } from "react";
import { User } from "../../../App";
//import { useNavigate } from "react-router";
import Logo from "../../../Components/Logo";

function Update2FA(props: { dark: boolean; user: User }) {
	const [passcode, setPasscode] = useState("");
	const [recoveryCode, setRecoveryCode] = useState("");
	const [password, setPassword] = useState("");
	const disable2FA = () => {
		return;
	};
	return (
		<>
			<Logo dark={props.dark} />
			<h1>BoltPass Password Manager - Update 2FA</h1>
			{props.user.totp_enabled ? (
				<>
					<h2>Disable 2FA</h2>
					<p>
						To disable 2FA please enter your password and either a one-time passcode
						or recovery key below
						<br />
						<span className="red">
							You only need to fill in ONE out these two options
						</span>
					</p>
					<form className="login">
						<input
							type="password"
							placeholder="Enter your password"
							required
							name="password"
							onInput={(v) => setPassword(v.currentTarget.value)}
						/>
						<div className="grid">
							<div>
								<label>Enter a one-time passcode</label>
								<input
									type="number"
									placeholder="Enter your OTP"
									minLength={6}
									maxLength={6}
									name="passcode"
									onInput={(v) => setPasscode(v.currentTarget.value)}
								/>
							</div>
							<div>
								<label>Enter one of your recovery codes</label>
								<input
									type="text"
									placeholder="Enter your recovery code"
									minLength={8}
									maxLength={8}
									name="recovery"
									onInput={(v) => setRecoveryCode(v.currentTarget.value)}
								/>
							</div>
						</div>
					</form>
					<button
						disabled={
							!password ||
							!(passcode.toString().length != 6 && recoveryCode.toString().length != 8)
						}
						onClick={disable2FA}
					>
						Disable 2FA
					</button>
				</>
			) : (
				<></>
			)}
		</>
	);
}

export default Update2FA;
