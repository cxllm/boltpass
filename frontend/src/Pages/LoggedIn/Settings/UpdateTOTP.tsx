import { useState } from "react";
import { User } from "../../../App";
//import { useNavigate } from "react-router";
import Logo from "../../../Components/Logo";

function Update2FA(props: { dark: boolean; user: User; logout: () => void }) {
	const [totpCode, setTotpCode] = useState("");
	const [recoveryCode, setRecoveryCode] = useState("");
	const [password, setPassword] = useState("");
	const [error, setError] = useState("");
	const [message, setMessage] = useState("");
	const [downloaded, setDownloaded] = useState(false);
	const [tfaConfig, setTfaConfig] = useState<{
		secret: string;
		image: string;
		recovery_codes: string[];
	}>();
	const disable2FA = () => {
		setError("Please wait...");
		fetch(
			`/api/user/${props.user.user_id}/2fa?password=${password}&${
				totpCode ? `totp_code=${totpCode}` : `recovery_code=${recoveryCode}`
			}`,
			{
				method: "PUT",
				body: JSON.stringify({
					tfa_enabled: false,
					totp_secret: ""
				})
			}
		)
			.then((r) => r.json())
			.then((r) => {
				if (r.error) {
					switch (r.error) {
						case "PASSWORD_NOT_CORRECT":
							setError("Incorrect password entered!");
							break;
						case "TOTP_CODE_NOT_CORRECT":
							setError("Invalid 2FA code entered!");
							break;
						case "RECOVERY_CODE_NOT_CORRECT":
							setError("Invalid recovery code entered!");
							break;
						default:
							setError("Internal Server Error");
							break;
					}
				} else {
					if (!r.enabled) {
						setError("");
						setMessage(
							"Two-Factor Authentication has been disabled! You must now login again, redirecting in 5 seconds..."
						);
						setTimeout(() => {
							props.logout();
						}, 5000);
					}
				}
			});
	};
	const enable2FA = () => {
		setError("Please wait...");
		fetch(`/api/verify-totp?code=${totpCode}&secret=${tfaConfig?.secret}`)
			.then((r) => r.json)
			.then((r) => {
				if (!r) {
					setError("Incorrect code entered!");
				} else {
					fetch(`/api/user/${props.user.user_id}/2fa?password=${password}`, {
						method: "PUT",
						body: JSON.stringify({
							tfa_enabled: true,
							totp_secret: tfaConfig?.secret,
							codes: tfaConfig?.recovery_codes
						})
					})
						.then((s) => s.json())
						.then((s) => {
							if (s.error) {
								switch (s.error) {
									case "PASSWORD_NOT_CORRECT":
										setError("Incorrect password entered!");
										break;
									default:
										setError("Internal server error");
								}
							} else {
								if (s.enabled) {
									setError("");
									setMessage(
										"Two-Factor Authentication has been enabled! You must now login again, redirecting in 5 seconds..."
									);
									setTimeout(() => {
										props.logout();
									}, 5000);
								}
							}
						});
				}
			});
	};
	const getTfaConfig = () => {
		return fetch(`/api/generate-totp?name=${props.user.email}`)
			.then((r) => r.json())
			.then((r) => setTfaConfig(r));
	};
	const downloadRecoveryCodes = () => {
		setDownloaded(true);
		const element = document.createElement("a");
		const file = new Blob(
			tfaConfig?.recovery_codes.map((r) => r + "\n"),
			{ type: "text/plain" }
		);
		element.href = URL.createObjectURL(file);
		element.download = `boltpass-recovery-codes-${props.user.email}.txt`;
		document.body.appendChild(element);
		element.click();
	};

	if (!tfaConfig && props.user.email) getTfaConfig();
	return (
		<>
			<Logo dark={props.dark} />
			{props.user.tfa_enabled ? (
				<>
					<h1>Disable Two Factor Authentication (2FA)</h1>
					<p>
						To disable 2FA please enter your password and either a one-time passcode
						or recovery key below
						<br />
					</p>
					<form className="login">
						<label className="red">
							Please confirm by entering your password and one of the options below
						</label>
						<input
							type="password"
							placeholder="Enter your password"
							required
							name="password"
							onInput={(v) => setPassword(v.currentTarget.value)}
						/>
						<span className="red">
							You only need to fill in ONE out of the two options below
						</span>
						<div className="grid">
							<div className="left">
								<label>Enter a one-time passcode</label>
								<input
									type="number"
									placeholder="Enter your OTP"
									minLength={6}
									maxLength={6}
									name="passcode"
									onInput={(v) => setTotpCode(v.currentTarget.value)}
								/>
							</div>
							<div className="right">
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
							(totpCode.toString().length != 6 && recoveryCode.toString().length != 8)
						}
						onClick={disable2FA}
					>
						Disable 2FA
					</button>
					{error ? <span className="red">{error}</span> : ""}
					{message ? <span className="green">{message}</span> : ""}
				</>
			) : (
				<>
					<h1>Enable Two Factor Authentication (2FA)</h1>
					<p>
						2FA provides your account with an additional layer of security by using a
						randomly generated secret key and generating a 6-digit code based on the
						current time. These codes refresh every 30 seconds.
					</p>
					{tfaConfig ? (
						<>
							<div className="grid">
								<div className="left">
									<h2>Authenticators</h2>
									<p>
										Scan the QR code below in an authenticator app such as Google
										Authenticator or Authy
									</p>
									<div className="image-center">
										<img src={tfaConfig.image} className="qrcode" />
									</div>
									<p>
										Alternatively, you can manually enter the secret key below:
										<br />
										Secret: <span>{tfaConfig.secret}</span>{" "}
										<a onClick={() => navigator.clipboard.writeText(tfaConfig.secret)}>
											Copy
										</a>
									</p>
								</div>
								<div className="right">
									<h2>Recovery Codes</h2>
									<h3>Please read the following carefully</h3>
									<p>
										If you ever lose access to your authenticator, the only way to get
										into your account will be using one of these recovery codes.
										<br />
										<span className="red">
											Please store these codes in a secure location as this is the only way
											to recover your account if you can't use your authenticator.
										</span>
										<br />
										You will have 8 recovery codes, and once you have used a code, it will
										no longer be accepted. Ensure you re-setup 2FA before they have all
										been used.
										<br />
										You cannot enable two factor authentication without downloading these
										codes to your device.
									</p>
									<button onClick={downloadRecoveryCodes}>
										Download Recovery Codes
									</button>
								</div>
							</div>
							<p>
								To add this configuration to your account, please enter your password
								below, and the code generated by your authenticator app
							</p>
							<form className="login">
								<label>Enter your password</label>
								<input
									type="password"
									placeholder="Enter your password"
									required
									name="password"
									onInput={(v) => setPassword(v.currentTarget.value)}
								/>
								<label>
									Enter the one-time passcode generated by your authenticator
								</label>
								<input
									type="number"
									placeholder="Enter your OTP"
									minLength={6}
									maxLength={6}
									name="passcode"
									onInput={(v) => setTotpCode(v.currentTarget.value)}
								/>
							</form>

							<button
								disabled={!password || totpCode.toString().length != 6 || !downloaded}
								onClick={enable2FA}
							>
								Enable 2FA
							</button>
							{!downloaded ? (
								<span className="red">
									You have not downloaded your recovery codes!
								</span>
							) : (
								""
							)}
							{error ? <span className="red">{error}</span> : ""}
							{message ? <span className="green">{message}</span> : ""}
						</>
					) : (
						<p>Please wait while the configuration loads...</p>
					)}
				</>
			)}
		</>
	);
}

export default Update2FA;
