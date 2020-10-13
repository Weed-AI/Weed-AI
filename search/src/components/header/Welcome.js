import React from "react"

import "./Welcome.css"
import Logo from "../../assets/images/sih_logo.svg"
import About from "./About"

const Welcome = ({ element }) => {
    return (
        <main>
            <section className="welcome">
                <div ref={element}>
                    <img src={Logo} alt="logo" className="welcome--logo" />
                    <p>WeedID is an open source, searchable, weeds image platform designed to facilitate the research and development of machine learning algorithms for weed recognition in cropping systems. It brings together existing datasets, enables users to contribute their own data and pulls together custom datasets for straightforward download.</p>
                    <button className="welcome__cta-primary">Contact us</button>
                </div>
            </section>
            <About />
        </main>
    )
}

export default Welcome