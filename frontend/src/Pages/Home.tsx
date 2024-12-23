import { useState } from "react";
import { Link } from "react-router";
function Home() {
	const [count, setCount] = useState(0);

	return (
		<>
			<div>
				<Link to="/">
					<img src="/Bolt%20Pass%20Dark.png" className="logo" alt="Vite logo" />
				</Link>
			</div>
			<h1>BoltPass Password Manager</h1>
			<div className="card">
				<button onClick={() => setCount((count) => count + 1)}>
					count is {count}
				</button>
				<p>
					Edit <code>src/App.tsx</code> and save to test HMR
				</p>
			</div>
			<p className="read-the-docs">
				Click on the Vite and React logos to learn more
			</p>
		</>
	);
}

export default Home;
