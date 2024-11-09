import React, { Component } from "react";
import { Route, NavLink } from "react-router-dom";

export class NavbarLink extends Component {

    render() {
        return (
            <Route path={ this.props.to } exact={ this.props.exact }
                   children={ routeProps=> {
                         return <NavLink activeClassName="active" to={ this.props.to } exact={this.props.exact}>
                                { this.props.children }
                              </NavLink>
                   }} />
        );
    }

}