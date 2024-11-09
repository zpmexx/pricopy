import React, { Component } from "react";
import {NavbarLink} from "./navbar/NavbarLink";
import { Route } from "react-router-dom";
import Globals from "../Globals";

export class Header extends Component {

    render() {
        return (
            <header className="header">
                <nav className="navbar">
                    <div className="container-fluid">
                        <ul className="main-chapter">
                            <li className="main-chapter-item">
                                <NavbarLink key={"main"} to={Globals.URL_MAIN_PATH} exact={true}>Panel Administratora</NavbarLink>
                                <Route path={Globals.URL_MAIN_PATH+"orders/"}>
                                    >
                                    <NavbarLink key={"orders"} to={Globals.URL_MAIN_PATH+"orders/"} exact={true}>Zamówienia</NavbarLink>
                                </Route>
                            </li>
                            {/*<li class="main-chapter-item active">*/}
                            {/*</li>*/}
                        </ul>
                        {/*<div class="navbar-holder d-flex align-items-center justify-content-between">*/}
                        {/*    <div class="navbar-header">*/}
                        {/*        <span>Panel Administratora</span>*/}
                        {/*    </div>*/}
                        {/*</div>*/}
                    </div>
                </nav>
            </header>
        )
    }

}