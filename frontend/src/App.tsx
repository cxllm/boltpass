import "./App.scss";
import { BrowserRouter, Routes, Route } from "react-router";
import Home from "./Pages/Home";
import "./App.scss";
import NotFound from "./Pages/404";
function App() {
	return (
		<>
			<div className="app">
				<BrowserRouter>
					<Routes>
						<Route path="/" element=<Home /> />
						<Route path="*" element=<NotFound /> />
					</Routes>
				</BrowserRouter>
			</div>
		</>
	);
}

export default App;
