import { useState } from "react";
import { User } from "../../../App";
import { useNavigate } from "react-router";
import Logo from "../../../Components/Logo";

interface Password {
	decrypted: string;
	name: string;
	folder_name: string | undefined | null;
	website: string | undefined | null;
	username: string;
	totp_secret: string | undefined | null;
}
function Passwords(props: { dark: boolean; user: User; getKey: () => void }) {
	const [passwords, setPasswords] = useState<Password[]>();
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
	return (
		<>
			<Logo dark={props.dark} />
			<h1>Your Passwords</h1>
			<button onClick={() => navigate("/user/passwords/add")}>Add Password</button>
			{passwords ? (
				passwords.map((p) => p.name)
			) : (
				<p>Please wait, your passwords are loading...</p>
			)}
		</>
	);
}

export default Passwords;
