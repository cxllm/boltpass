import "./App.scss";
import { BrowserRouter, Routes, Route, Navigate } from "react-router";
import Home from "./Pages/Home";
import "./App.scss";
import NotFound from "./Pages/404";
import PasswordGenerator from "./Pages/PasswordGenerator";
import Navbar from "./Components/Navbar";
import { useState } from "react";
import Login from "./Pages/Login";
import SignUp from "./Pages/SignUp";
import NavbarLoggedIn from "./Components/Navbar-LoggedIn";
import LoggedInHome from "./Pages/LoggedInHome";
import Passwords from "./Pages/Passwords";
import SecureNotes from "./Pages/SecureNotes";
import Settings from "./Pages/Settings";

export interface User {
	user_id: string;
	email: string;
	password_hash: string;
	salt: string;
	totp_enabled: boolean;
	totp_secret: string;
	error?: string;
}
function App() {
	const [dark, setDark] = useState(
		// set the "dark" state to the exisiting element in local storage or true if it doesn't exist
		!(window.localStorage.getItem("dark") == "false")
	);
	const [loggedIn, setLoggedIn] = useState(
		window.localStorage.getItem("userID") ? true : false
	);
	const darkMode = () => {
		// function to update the darkMode prefernces
		const string = window.localStorage.getItem("dark"); // check if dark mode preferences already exist.
		let enabled = !(string == "false"); // if they don't exist, set by default to true
		enabled = !enabled; // reverse the dark mode preference
		setDark(enabled); // update it in react state
		window.localStorage.setItem("dark", enabled.toString()); // update it in local storage
	};

	const getItemFromLocalStorage = (name: string) => {
		const value = window.localStorage.getItem(name);
		try {
			if (value) {
				const data = JSON.parse(value);
				if (data.expiry < Date.now()) {
					window.localStorage.removeItem(name);
					return null;
				} else {
					return data.value;
				}
			}
		} catch {
			return value;
		}
	};

	const logOut = () => {
		window.localStorage.removeItem("userID");
		window.localStorage.removeItem("key");
		setLoggedIn(false);
		return <Navigate to="/" />;
	};
	const getUserInfo = async () => {
		const userID = getItemFromLocalStorage("userID");
		if (userID == null) {
			return undefined;
		}
		return fetch("/api/user/" + userID)
			.then((r) => r.json())
			.then((r: User) => {
				if (r.error) {
					logOut();
					return undefined;
				} else {
					console.log(r);
					return r;
				}
			});
	};
	const [user, setUser] = useState<User>();
	console.log(loggedIn, user, loggedIn && !user);
	if (loggedIn && !user) getUserInfo().then((r) => setUser(r));
	const login = (userID: string, key: string) => {
		const expiry = Date.now() + 24 * 60 * 60 * 1000;
		window.localStorage.setItem(
			"userID",
			JSON.stringify({ value: userID, expiry })
		);
		window.localStorage.setItem("key", JSON.stringify({ value: key, expiry }));
		setLoggedIn(true);
		getUserInfo().then((r) => setUser(r));
	};
	return (
		<>
			<BrowserRouter>
				{/* set up the router allowing for different elements to be rendered depending on the path */}
				<div className={"app " + (dark ? "dark" : "light")}>
					{/* set to dark or light mode depending on the state */}
					{loggedIn ? (
						<NavbarLoggedIn setDark={darkMode} dark={dark} logout={logOut} />
					) : (
						<Navbar setDark={darkMode} dark={dark} />
					)}
					{/* The elements contained with the router act as a template for each page, so each page will include the navbar */}
					<div className="content">
						{/* each page will be contained within the content class which has specific stylings for the content of the page */}
						<Routes>
							{/* Instructs which element to render based on the path entered */}
							<Route
								path="/"
								element={
									loggedIn && user ? (
										<LoggedInHome dark={dark} user={user} />
									) : (
										<Home dark={dark} />
									)
								}
							/>
							<Route
								path="/password-generator"
								element=<PasswordGenerator dark={dark} />
							/>
							<Route
								path="/login"
								element={
									loggedIn ? <Navigate to="/" /> : <Login dark={dark} login={login} />
								}
							/>
							<Route
								path="/sign-up"
								element={
									loggedIn ? <Navigate to="/" /> : <SignUp dark={dark} login={login} />
								}
							/>
							<Route
								path="/user/passwords"
								element={
									loggedIn && user ? (
										<Passwords dark={dark} user={user} />
									) : (
										<Navigate to="/login" />
									)
								}
							/>
							<Route
								path="/user/secure-notes"
								element={
									loggedIn && user ? (
										<SecureNotes dark={dark} user={user} />
									) : (
										<Navigate to="/login" />
									)
								}
							/>
							<Route
								path="/user/settings"
								element={
									loggedIn && user ? (
										<Settings dark={dark} user={user} />
									) : (
										<Navigate to="/login" />
									)
								}
							/>

							<Route path="*" element=<NotFound dark={dark} /> />
						</Routes>
					</div>
				</div>
			</BrowserRouter>
		</>
	);
}

export default App;
