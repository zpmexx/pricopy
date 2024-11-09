import React, { Component } from "react";
import {NavbarHeader} from "./NavbarHeader";
import {NavbarLink} from "./NavbarLink";
import Globals from "../../Globals";

export class Navbar extends Component {

    render() {
        let shrinked_class = this.props.shrinked ? " shrink" : "";
        return (
            <nav className={"side-navbar" + shrinked_class}>
                <div className={"side-navbar-wrapper"}>
                    <NavbarHeader/>
                    <div className="main-menu">
                        <ul id="side-main-menu" className="side-menu list-unstyled">
    						<li><a id="main-nav" href="#" onClick={this.props.shrinkMenu}>Menu</a></li>
                            <li><NavbarLink key={"orders"} to={Globals.URL_MAIN_PATH+"orders"}>Zamówienia</NavbarLink></li>
                        </ul>
                    </div>
                    </div>
            </nav>
        );
    }

}
