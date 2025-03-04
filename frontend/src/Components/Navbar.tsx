import { Navbar, Nav } from "react-bootstrap";
import { Component } from "react";
import { Link } from "react-router";
import { FaLightbulb, FaMoon } from "react-icons/fa6";

export default class Navigation extends Component<
	{
		setDark: () => void;
		dark: boolean;
	},
	{ pathname: string }
> {
	// intialise the state with empty pathname
	state = {
		pathname: ""
	};
	render() {
		if (this.state.pathname == "") {
			// update to current pathname
			this.setState({ pathname: window.location.pathname });
		}
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
							activeKey={this.state.pathname}
							defaultActiveKey="/"
							onSelect={(selectedKey) => {
								// updates the current pathname when a link is pressed (only works when a Nav.Link is pressed)
								this.setState({ pathname: selectedKey || "/" });
							}}
						>
							{" "}
							<Navbar.Brand
								as={Link}
								to="/"
								// Brand is not recognised as a Nav.Link so current pathname must be updated manually
								onClick={() => this.setState({ pathname: "/" })}
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
							activeKey={this.state.pathname}
							defaultActiveKey="/"
							onSelect={(selectedKey) => {
								// updates the current pathname when a link is pressed (only works when a Nav.Link is pressed)
								this.setState({ pathname: selectedKey || "/" });
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
								onClick={() => this.props.setDark()}
								style={{ fontSize: "30px", cursor: "pointer" }}
							>
								{this.props.dark ? <FaLightbulb /> : <FaMoon />}
							</Navbar.Brand>
						</Nav>
					</Navbar.Collapse>
				</Navbar>
			</>
		);
	}
}
