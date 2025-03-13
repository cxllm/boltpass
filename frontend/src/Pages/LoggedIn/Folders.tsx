import { useState } from "react";
import { User } from "../../App";
import { Link } from "react-router";
import Logo from "../../Components/Logo";

export interface Folder {
	folder_name: string;
	user_id: string;
	items: number;
}
// Shows the users their folders
function Folders(props: { dark: boolean; user: User }) {
	// Initialise states
	const [folders, setFolders] = useState<Folder[]>();
	const [searchQuery, setSearchQuery] = useState("");
	const getFolders = () => {
		// Get the folders from the database
		fetch(`/api/user/${props.user.user_id}/folders`)
			.then((r) => r.json())
			.then((r) => {
				if (r.error) {
					return;
				} else {
					setFolders(r);
				}
			});
	};
	if (!folders) getFolders();
	// get folders to match search query
	const filteredResults = folders?.filter((f) => {
		if (!searchQuery) {
			return true;
		}
		const s = searchQuery.toLowerCase();
		return f.folder_name.toLowerCase().includes(s);
	});
	return (
		<>
			<Logo dark={props.dark} />
			<h1>Your Folders</h1>
			<p>
				To create a new folder, add or edit a password with the folder name you
				would like to add
			</p>
			{folders ? (
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
							{filteredResults.map((f: Folder, i) => (
								// create an element for each folder that matches
								<Link to={`/user/passwords/folder/${f.folder_name}`}>
									<div className={i % 2 == 1 ? "right" : "left"}>
										<h2>{f.folder_name}</h2>
										<p>
											Number of Passwords: {f.items}
											<br />
										</p>

										<Link to={`/user/passwords/folder/${f.folder_name}`}>View</Link>
									</div>{" "}
								</Link>
							))}{" "}
						</div>
					) : (
						<span className="red">No results found!</span>
					)}
				</>
			) : (
				<p>Please wait, your folders are loading...</p>
			)}
		</>
	);
}

export default Folders;
