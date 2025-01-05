import "./App.scss";
import { BrowserRouter, Routes, Route } from "react-router";

import Home from "./Pages/Home";
import "./App.scss";
import NotFound from "./Pages/404";
import PasswordGenerator from "./Pages/PasswordGenerator";
import Navbar from "./Components/Navbar";
import { useState } from "react";
import Login from "./Pages/Login";
import SignUp from "./Pages/SignUp";
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
	return (
		<>
			<BrowserRouter>
				{/* set up the router allowing for different elements to be rendered depending on the path */}
				<div className={"app " + (dark ? "dark" : "light")}>
					{/* set to dark or light mode depending on the state */}
					<Navbar setDark={darkMode} dark={dark} />
					{/* The elements contained with the router act as a template for each page, so each page will include the navbar */}
					<div className="content">
						{/* each page will be contained within the content class which has specific stylings for the content of the page */}
						<Routes>
							{/* Instructs which element to render based on the path entered */}
							<Route path="/" element=<Home dark={dark} /> />
							<Route
								path="/password-generator"
								element=<PasswordGenerator dark={dark} />
							/>
							<Route path="/login" element=<Login dark={dark} /> />
							<Route path="/sign-up" element=<SignUp dark={dark} /> />

							<Route path="*" element=<NotFound dark={dark} /> />
						</Routes>
					</div>
				</div>
			</BrowserRouter>
		</>
	);
}

export default App;
