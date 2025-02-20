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
import LoggedInHome from "./Pages/LoggedIn/Home";
import Passwords from "./Pages/LoggedIn/Passwords";
import SecureNotes from "./Pages/LoggedIn/SecureNotes";
import Settings from "./Pages/LoggedIn/Settings/Main";
import DeleteAccount from "./Pages/LoggedIn/Settings/DeleteAccount";
import Update2FA from "./Pages/LoggedIn/Settings/UpdateTOTP";
import UpdateEmail from "./Pages/LoggedIn/Settings/UpdateEmail";
import UpdatePassword from "./Pages/LoggedIn/Settings/UpdatePassword";

export interface User {
	user_id?: string;
	email?: string;
	password_hash?: string;
	salt?: string;
	tfa_enabled?: boolean;
	totp_secret?: string;
	error?: string;
}
function App() {
	const [dark, setDark] = useState(
		// set the "dark" state to the exisiting element in local storage or true if it doesn't exist
		!(window.localStorage.getItem("dark") == "false")
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
		// function to get item from local storage
		const value = window.localStorage.getItem(name);
		try {
			// if the value has expired then get rid of it
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
	const [loggedIn, setLoggedIn] = useState(
		getItemFromLocalStorage("userID") ? true : false
	);

	const getUserInfo = async () => {
		// function to get user info
		// gets user id from local storage
		const userID = getItemFromLocalStorage("userID");
		if (userID == null) {
			return {};
		}
		// fetchs user info from database
		return fetch("/api/user/" + userID)
			.then((r) => r.json())
			.then((r: User) => {
				if (r.error) {
					logOut();
					return {};
				} else {
					return r;
				}
			});
	};
	const [user, setUser] = useState<User>({});
	if (loggedIn && !user.user_id) getUserInfo().then((r) => setUser(r));
	const logIn = (userID: string, key: string) => {
		// function to login user
		// local storage does not have a built in expiry functionality, so expiry has to be done automatically
		// this means the maximum period of time a user can be logged in for is 1 day
		const expiry = Date.now() + 24 * 60 * 60 * 1000;
		window.localStorage.setItem(
			"userID",
			JSON.stringify({ value: userID, expiry })
		);
		window.localStorage.setItem("key", JSON.stringify({ value: key, expiry }));
		setLoggedIn(true);
		getUserInfo().then((r) => setUser(r));
		return <Navigate to="/" />;
	};
	const logOut = () => {
		// Get rid of user id and key values when user logs out
		window.localStorage.removeItem("userID");
		window.localStorage.removeItem("key");
		setLoggedIn(false);
		setUser({});
		// redirect to home page
		return <Navigate to="/" />;
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
									loggedIn ? <Navigate to="/" /> : <Login dark={dark} login={logIn} />
								}
							/>
							<Route
								path="/sign-up"
								element={
									loggedIn ? <Navigate to="/" /> : <SignUp dark={dark} login={logIn} />
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
							<Route
								path="/user/settings/delete"
								element={
									loggedIn && user ? (
										<DeleteAccount dark={dark} user={user} logout={logOut} />
									) : (
										<Navigate to="/login" />
									)
								}
							/>
							<Route
								path="/user/settings/2fa"
								element={
									loggedIn && user ? (
										<Update2FA dark={dark} user={user} logout={logOut} />
									) : (
										<Navigate to="/login" />
									)
								}
							/>
							<Route
								path="/user/settings/email"
								element={
									loggedIn && user ? (
										<UpdateEmail dark={dark} user={user} logout={logOut} />
									) : (
										<Navigate to="/login" />
									)
								}
							/>
							<Route
								path="/user/settings/password"
								element={
									loggedIn && user ? (
										<UpdatePassword dark={dark} user={user} logout={logOut} />
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
