import React from "react"
import "./Navbar.css"
import Logo from "../../assets/images/sih_logo.svg"

const Navbar = ({ sticky }) => (
    <nav className={sticky ? "navbar navbar-sticky" : "navbar"}>
        <div className="navbar--logo-holder">
            {sticky ? <img src={Logo} alt="logo" className="navbar--logo" /> : null}
            <h1> WeedID Explorer</h1>
        </div>
        <ul className="navbar--link">
            <li className="navbar--link-item">Home</li>
            <li className="navbar--link-item">About</li>
            <li className="navbar--link-item">Search</li>
        </ul>
    </nav>
)
export default Navbar