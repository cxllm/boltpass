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
	state = {
		pathname: ""
	};
	render() {
		if (this.state.pathname == "") {
			this.setState({ pathname: window.location.pathname });
		}
		console.log(this.state.pathname);
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
								console.log(selectedKey);
								this.setState({ pathname: selectedKey || "/" });
							}}
						>
							{" "}
							<Navbar.Brand
								as={Link}
								to="/"
								onClick={() => this.setState({ pathname: "/" })}
								className="brand"
							>
								<img
									src="/Bolt%20Pass%20Light.png"
									width="30"
									height="30"
									className="d-inline-block align-top"
									alt="BoltPass Logo"
								/>
							</Navbar.Brand>
							<Nav.Link eventKey="/" as={Link} to="/">
								Home
							</Nav.Link>
							<Nav.Link
								eventKey="/password-generator"
								as={Link}
								to="/password-generator"
							>
								Password Generator
							</Nav.Link>
						</Nav>
						<Nav style={{ paddingRight: "10px" }}>
							<Nav.Link as={Link} to="/login">
								Login
							</Nav.Link>{" "}
						</Nav>
						<Nav>
							<Navbar.Brand
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
