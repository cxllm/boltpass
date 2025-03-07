import { useState } from "react";
import { User } from "../../../App";
import { useNavigate, Link } from "react-router";
import Logo from "../../../Components/Logo";

export interface Password {
	decrypted: string;
	password_id: string;
	name: string;
	folder_name: string | undefined | null;
	website: string | undefined | null;
	username: string;
	totp_secret: string | undefined | null;
}
function Passwords(props: { dark: boolean; user: User; getKey: () => void }) {
	const [passwords, setPasswords] = useState<Password[]>();
	const [searchQuery, setSearchQuery] = useState("");
	const navigate = useNavigate();
	const getPasswords = () => {
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
	if (!passwords) getPasswords();
	const filteredResults = passwords?.filter((p) => {
		if (!searchQuery) {
			return true;
		}
		const s = searchQuery.toLowerCase();
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
			<h1>Your Passwords</h1>
			<button onClick={() => navigate("/user/passwords/add")}>Add Password</button>
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
								<div className={i % 2 == 1 ? "right" : "left"}>
									<h2>{p.name}</h2>
									<p>
										Username: {p.username}
										<br />
										Website: {p.website || "None"}
									</p>

									<Link to={`/user/passwords/${p.password_id}`}>View</Link>
								</div>
							))}{" "}
						</div>
					) : (
						<span className="red">No results found!</span>
					)}
				</>
			) : (
				<p>Please wait, your passwords are loading...</p>
			)}
		</>
	);
}

export default Passwords;
