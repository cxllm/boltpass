import { useState } from "react";
import { User } from "../../../App";
import { useNavigate, Link, useParams } from "react-router";
import Logo from "../../../Components/Logo";

// Type for when the passwords are requested from the database
export interface Password {
	decrypted: string;
	password_id: string;
	name: string;
	folder_name: string | undefined | null;
	website: string | undefined | null;
	username: string;
	totp_secret: string | undefined | null;
	reused: number;
	leaked: number;
}

// Page that shows all of the users passwords
function Passwords(props: { dark: boolean; user: User; getKey: () => void }) {
	// Folder name can be present if called from /user/passwords/folder/[folderName]
	const { folderName } = useParams();
	// Initialise states
	const [passwords, setPasswords] = useState<Password[]>();
	const [searchQuery, setSearchQuery] = useState("");
	const [requestSent, setRequestSent] = useState(false);
	const navigate = useNavigate();
	const getPasswords = () => {
		// Get the passwords from the database that correspond to this user
		fetch(`/api/user/${props.user.user_id}/passwords?key=${props.getKey()}`)
			.then((r) => r.json())
			.then((r) => {
				if (r.error) {
					return;
				} else {
					setPasswords(r);
				}
			});
	};
	const deleteFolder = () => {
		// Deletes the folder from the database using a DELETE request
		if (!requestSent) {
			// Only sends a request if one hasn't already been sent
			setRequestSent(true);
			fetch(
				`/api/user/${
					props.user.user_id
				}/folder/${folderName}?key=${props.getKey()}`,
				{ method: "DELETE" }
			)
				.then((r) => r.json())
				.then((r) => {
					if (r.error) {
						return;
					} else if (r.success) {
						// Bring back to main password page when deleted
						return navigate("/user/passwords");
					}
				});
		}
	};
	if (!passwords) getPasswords();
	// Filter the results based on a search query
	const filteredResults = passwords?.filter((p) => {
		// If there is no search query or folder, return all items
		if (!searchQuery && !folderName) {
			return true;
		}
		// If there is a folder but no search query show all items in the folder
		else if (folderName && !searchQuery) {
			return p.folder_name == folderName;
		}

		// get the matching items
		const s = searchQuery.toLowerCase();
		if (folderName) {
			return (
				p.folder_name == folderName &&
				(p.name.toLowerCase().includes(s) ||
					p.website?.toLowerCase().includes(s) ||
					p.username.toLowerCase().includes(s))
			);
		}
		return (
			p.name.toLowerCase().includes(s) ||
			p.folder_name?.toLowerCase().includes(s) ||
			p.website?.toLowerCase().includes(s) ||
			p.username.toLowerCase().includes(s)
		);
	});
	return (
		<>
			<Logo dark={props.dark} />
			<h1>Your Passwords{folderName ? ` - ${folderName}` : ""}</h1>
			<div className="buttons">
				<button onClick={() => navigate("/user/passwords/add")}>
					Add Password
				</button>
				{folderName ? (
					<button
						className="red-button"
						onClick={() => {
							deleteFolder();
						}}
					>
						{requestSent ? "Deleting" : "Delete Folder"}
					</button>
				) : (
					""
				)}
			</div>
			{passwords ? (
				<>
					<input
						type="text"
						placeholder="Enter your search query"
						required
						name="search"
						className="search"
						onInput={(v) => setSearchQuery(v.currentTarget.value)}
					/>

					{filteredResults && filteredResults.length >= 1 ? (
						<div className="grid">
							{filteredResults.map((p: Password, i) => (
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
							))}{" "}
						</div>
					) : (
						<span className="red">
							{folderName ? "Folder does not exist!" : "No results found!"}
						</span>
					)}
				</>
			) : (
				<p>Please wait, your passwords are loading...</p>
			)}
		</>
	);
}

export default Passwords;
