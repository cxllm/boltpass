import { useState } from "react";
import { FaCopy, FaKey } from "react-icons/fa6";
import Logo from "../Components/Logo";

function PasswordGenerator(props: { dark: boolean }) {
	// creates a new item in the state for each property that can be modified in the generator password
	const [length, setLength] = useState(20);
	const [uppercase, setUppercase] = useState(true);
	const [numbers, setNumbers] = useState(true);
	const [special, setSpecial] = useState(true);
	// state for the generated password
	const [password, setPassword] = useState("");
	// state for if the user has copied it or not
	const [copied, setCopied] = useState(false);

	const generate = () => {
		// function to generate a password
		setCopied(false); // as the password has just been generated, set copied to false
		fetch(
			`/api/generate-password?numbers=${numbers ? "True" : "False"}&uppercase=${
				uppercase ? "True" : "False"
			}&specialchars=${special ? "True" : "False"}&length=${length || 20}`
		) // get the password from the backend using the specified parameters
			.then((r) => r.json()) // convert to json
			.then((r) => {
				// get the password and set it into the state
				// assuming there is no error, otherwise the r.password item would not exist
				if (r.password) setPassword(r.password);
			});
	};

	return (
		<>
			<Logo dark={props.dark} />
			<h1>Password Generator</h1>
			<form className="password-generator">
				<label className="slider">
					{/* Slider for length of password */}
					<input
						type="range"
						min="4"
						max="200"
						step="1"
						value={length}
						// update the length state when it changes
						onInput={(v) => setLength(parseInt(v.currentTarget.value))}
					/>
					Length: {length}
				</label>
				<label>
					<input
						// checkbox for uppercase letters
						type="checkbox"
						// update state on changes
						onInput={() => setUppercase(!uppercase)}
						checked={uppercase}
					/>
					Uppercase Letters
				</label>
				<label>
					<input
						// checkbox for numbers
						type="checkbox"
						// update state on changes
						onInput={() => setNumbers(!numbers)}
						checked={numbers}
					/>
					Numbers (0-9)
				</label>
				<label>
					<input
						// checkbox for special characters
						type="checkbox"
						// update state on changes
						onInput={() => setSpecial(!special)}
						checked={special}
					/>
					Special Characters (!@#$%^&*)
				</label>
			</form>
			{/* when the button is pressed, generate a password based on the conditions given by the user */}
			<button onClick={generate}>
				<FaKey /> Generate
			</button>
			{
				// if the password hasn't been generated yet, don't show anything
				password ? ( // if it has, show the below
					<>
						<h2 className="generator">Generated Password: {password}</h2>
						<button
							// button to copy the password to the clipboard
							onClick={() => {
								setCopied(true);
								navigator.clipboard.writeText(password);
							}}
						>
							<FaCopy />{" "}
							{
								// the text on the button is updated based on whether it has been copied or not
								copied ? "Copied!" : "Copy to Clipboard"
							}
						</button>
					</>
				) : (
					""
				)
			}
		</>
	);
}

export default PasswordGenerator;
