import { useState } from "react";
import { FaCopy, FaKey } from "react-icons/fa6";

function PasswordGenerator(props: { dark: boolean }) {
	const [length, setLength] = useState(20);
	const [uppercase, setUppercase] = useState(true);
	const [numbers, setNumbers] = useState(true);
	const [special, setSpecial] = useState(true);
	const [password, setPassword] = useState("");
	const [copied, setCopied] = useState(false);

	const generate = () => {
		setCopied(false);
		fetch(
			`/api/generate-password?numbers=${numbers ? "True" : "False"}&uppercase=${
				uppercase ? "True" : "False"
			}&specialchars=${special ? "True" : "False"}&length=${length || 20}`
		)
			.then((r) => r.json())
			.then((r) => {
				if (r.password) setPassword(r.password);
			});
	};

	return (
		<>
			<img
				src={`/Bolt%20Pass%20${props.dark ? "Light" : "Dark"}.png`}
				className="logo"
				alt="BoltPass logo"
			/>
			<h1>Password Generator</h1>

			<form className="password-generator">
				<label className="slider">
					<input
						type="range"
						min="4"
						max="200"
						step="1"
						value={length}
						onInput={(v) => setLength(parseInt(v.currentTarget.value))}
					/>
					Length: {length}
				</label>
				<label>
					<input
						type="checkbox"
						onInput={() => setUppercase(!uppercase)}
						checked={uppercase}
					/>
					Uppercase Letters
				</label>
				<label>
					<input
						type="checkbox"
						onInput={() => setNumbers(!numbers)}
						checked={numbers}
					/>
					Numbers (0-9)
				</label>
				<label>
					<input
						type="checkbox"
						onInput={() => setSpecial(!special)}
						checked={special}
					/>
					Special Characters (!@#$%^&*)
				</label>
			</form>
			<button onClick={generate}>
				<FaKey /> Generate
			</button>
			{password ? (
				<>
					<h2>Generated Password: {password}</h2>
					<button
						onClick={() => {
							setCopied(true);
							navigator.clipboard.writeText(password);
						}}
					>
						<FaCopy /> {copied ? "Copied!" : "Copy to Clipboard"}
					</button>
				</>
			) : (
				""
			)}
		</>
	);
}

export default PasswordGenerator;
