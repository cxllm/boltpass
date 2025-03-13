import { useState } from "react";
import { User } from "../../../App";
import Logo from "../../../Components/Logo";
import { useParams, Link } from "react-router";
import { Password } from "./Main";

// Shows the user how many times their password has been reused across their account
function ReusedPasswords(props: {
	dark: boolean;
	user: User;
	getKey: () => string;
}) {
	// Initialise the states and get the password ID
	const { passwordID } = useParams();
	const [passwords, setPasswords] = useState<Password[]>();
	const [error, setError] = useState("");
	const [currentPassword, setCurrentPassword] = useState<Password>();
	const [filteredPasswords, setFilteredPasswords] = useState<Password[]>();

	const getPasswords = () => {
		// get passwords from database that match current one
		fetch(
			`/api/user/${props.user.user_id}/passwords/security?key=${props.getKey()}`
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
					setPasswords(r);
				}
			});
	};
	if (!passwords) getPasswords();
	if (passwords && !filteredPasswords) {
		// get the current password and find the passwords that match the value of the current one
		const i = passwords.findIndex((p) => p.password_id == passwordID);
		if (i == -1) {
			setError("Password not found!");
		} else {
			setCurrentPassword(passwords[i]);
			setFilteredPasswords(
				passwords.filter((p) => {
					console.log(p.password_id == passwordID, p.decrypted);
					if (p.password_id == passwordID) return false;
					return p.decrypted == passwords[i].decrypted;
				})
			);
		}
	}
	return (
		<>
			<Logo dark={props.dark} />
			<h1>
				Reused Passwords {currentPassword ? `- ${currentPassword.name} ` : ""}
			</h1>
			<Link to={`/user/passwords/${passwordID}`}>
				{"<<"} Back to Password Details
			</Link>{" "}
			{passwords && currentPassword && filteredPasswords ? (
				<>
					{
						// if the results have been found and there are 1 or more, show the results, if not give a message to tell the user that they have not reused this password
						filteredPasswords.length > 0 ? (
							<>
								<h2>
									The passwords that have reused the same password as "
									{currentPassword.name}" are:
								</h2>
								<div className="grid">
									{filteredPasswords.map((p, i) => (
										// Add a new element for each password in the results
										<Link to={`/user/passwords/${p.password_id}`}>
											<div className={i % 2 == 1 ? "right" : "left"}>
												<h2>{p.name}</h2>
												<p>
													Username: {p.username}
													<br />
													Website: {p.website || "None"}
												</p>

												<Link to={`/user/passwords/${p.password_id}`}>View</Link>
											</div>
										</Link>
									))}
								</div>
							</>
						) : (
							<span className="green">
								There are no passwords that use the same password as this one!
							</span>
						)
					}
				</>
			) : (
				// display any error
				<p>{error ? <span className="error">{error}</span> : "Loading..."}</p>
			)}
		</>
	);
}

export default ReusedPasswords;
