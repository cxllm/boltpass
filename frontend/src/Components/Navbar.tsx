import { Navbar, Nav } from "react-bootstrap";
import { useState, useEffect } from "react";
import { Link, useLocation } from "react-router";
import { FaLightbulb, FaMoon } from "react-icons/fa6";

export default function Navigation(props: {
	setDark: () => void;
	dark: boolean;
}) {
	const location = useLocation();

	// intialise the state with current pathname
	const [pathname, setPathname] = useState(location.pathname);
	// update pathname state when it path changes
	useEffect(() => {
		setPathname(location.pathname);
	}, [location]);
	// The Navbar used is a bootstrap style one as this provides better responsive design for mobile
	return (
		<>
			<Navbar
				collapseOnSelect
				expand="lg"
				variant="dark"
				style={{
					animation: "none",
					padding: "10px 20px",
					color: "#fff"
				}}
				className="nav"
				sticky="top"
			>
				<Navbar.Toggle
					aria-controls="responsive-navbar-nav"
					style={{ textAlign: "left" }}
				/>
				<Navbar.Collapse id="responsive-navbar-nav">
					<Nav
						className="me-auto"
						activeKey={pathname}
						defaultActiveKey="/"
						onSelect={() => {
							// updates the current pathname when a link is pressed (only works when a Nav.Link is pressed)
							setPathname(location.pathname);
						}}
					>
						{" "}
						<Navbar.Brand
							as={Link}
							to="/"
							// Brand is not recognised as a Nav.Link so current pathname must be updated manually
							onClick={() => setPathname(location.pathname)}
							className="brand"
						>
							<img
								src="/bolt-pass-light.png"
								width="30"
								height="30"
								className="d-inline-block align-top"
								alt="BoltPass Logo"
							/>
						</Navbar.Brand>
						<Nav.Link eventKey="/" as={Link} to="/">
							Home
						</Nav.Link>
						<Nav.Link eventKey="/about" as={Link} to="/about">
							About BoltPass
						</Nav.Link>
						<Nav.Link
							eventKey="/password-generator"
							as={Link}
							to="/password-generator"
						>
							Password Generator
						</Nav.Link>
					</Nav>
					<Nav
						style={{ paddingRight: "10px" }}
						activeKey={pathname}
						defaultActiveKey="/"
						onSelect={() => {
							// updates the current pathname when a link is pressed (only works when a Nav.Link is pressed)
							setPathname(location.pathname);
						}}
					>
						<Nav.Link eventKey="/login" as={Link} to="/login">
							Login
						</Nav.Link>{" "}
						<Nav.Link eventKey="/sign-up" as={Link} to="/sign-up">
							Sign Up
						</Nav.Link>{" "}
					</Nav>
					<Nav>
						<Navbar.Brand
							// allows user to select light or dark mode
							onClick={() => props.setDark()}
							style={{ fontSize: "30px", cursor: "pointer" }}
						>
							{props.dark ? <FaLightbulb /> : <FaMoon />}
						</Navbar.Brand>
					</Nav>
				</Navbar.Collapse>
			</Navbar>
		</>
	);
}
