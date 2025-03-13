import Logo from "../Components/Logo";

// Provides information about the service and why users should trust it
function About(props: { dark: boolean }) {
	return (
		<>
			<Logo dark={props.dark} />
			<h1>Information About BoltPass</h1>
			<h2>What is BoltPass?</h2>
			<p className="justify">
				BoltPass is a secure password manager that stores your passwords for you so
				you only have to remember one, your password to access this site. This
				allows you to use unique, secure passwords for each one of your online
				accounts, so if one gets hacked, the others won't be at risk.
			</p>
			<hr />
			<h2>Why should I trust BoltPass?</h2>
			<p className="justify">
				Studies have shown that a large amount of Internet users don't trust
				password managers because of the amount of sensitive information you entrust
				in these services. Below you can find some information about how BoltPass
				works and how your data is kept secure.
			</p>
			<div className="grid">
				<div className="left">
					<h3>Your Master Password</h3>
					<p>
						Your master password is the password you use when you sign up to BoltPass.
						It is never stored on the server in readable format. It is stored such
						that it cannot be decrypted, so the only way it can be verified is when
						you enter it again so it can be encrypted again. This password is used to
						generate the encryption key, which is why it is not possible to reset your
						password if you forget it, as we have no way of decrypting your passwords
						without it.
					</p>
				</div>
				<div className="right">
					<h3>Password Storage</h3>
					<p>
						All passwords entered into BoltPass are encrypted before being stored on
						the server. The encryption key for this is not stored on our servers and
						is instead generated each time you enter your password. If you use the
						same password across different websites, each one is stored in a
						different, random way, making it impossible to tell. Without the
						encryption key, no one can access your passwords, even with access to the
						database.
					</p>
				</div>
				<div className="left">
					<h3>Encryption</h3>
					<p>
						BoltPass uses the industry standard AES-256 encryption algorithm to
						encrypt your passwords. It uses keys that are 256 bits long, which leaves
						over 10<sup>77</sup> combinations. The key is generated using your master
						password and an algorithm called Password-Based Key Derivation Function 2
						(PBKDF2) which allows the key to be retrieved each time you log in rather
						than stored on the server.
					</p>
				</div>
				<div className="right">
					<h3>Database Access</h3>
					<p>
						All sensitive data stored on the server is encrypted such that even if
						someone had access to the database, they would not be able to decipher any
						of the content stored. Furthermore, the only person with access to the
						database is the creator of this website, who does not have access to any
						encryption keys and can only see the structure of the database, and how
						many entries are contained
					</p>
				</div>
			</div>
		</>
	);
}

export default About;
