import "./App.scss";
import { BrowserRouter, Routes, Route } from "react-router";

import Home from "./Pages/Home";
import "./App.scss";
import NotFound from "./Pages/404";
import PasswordGenerator from "./Pages/PasswordGenerator";
import Navbar from "./Components/Navbar";
import { useState } from "react";
function App() {
	const [dark, setDark] = useState(
		window.localStorage.getItem("dark") != "false"
	);
	console.log(dark);
	const darkMode = () => {
		const string = window.localStorage.getItem("dark");
		let enabled = !(string == "false");
		console.log(enabled);
		enabled = !enabled;
		setDark(enabled);
		window.localStorage.setItem("dark", enabled.toString());
	};
	return (
		<>
			<BrowserRouter>
				<div className={"app " + (dark ? "dark" : "light")}>
					<Navbar setDark={darkMode} dark={dark} />
					<div className="content">
						<Routes>
							<Route path="/" element=<Home dark={dark} /> />
							<Route
								path="/password-generator"
								element=<PasswordGenerator dark={dark} />
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
