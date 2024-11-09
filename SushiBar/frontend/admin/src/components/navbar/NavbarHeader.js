import React, { Component } from "react";
import {authWrapper} from "../auth/AuthWrapper";

export const NavbarHeader = authWrapper(class extends Component {

    render() {
        return (
            <div className={"sidenav-header d-flex align-items-center justify-content-center flex-column"}>
                <div className={"sidenav-header-inner text-center"}>
                    <span>Witaj {this.props.user.username}</span>
                </div>
                {/*<img src="images/profil_1.jpg" alt="person" className={"img-fluid rounded-circle"}/>*/}

                <button className={"btn btn-primary button-status btn-sm"} onClick={this.props.signout}>Wyloguj</button>
            </div>
        );
    }

})