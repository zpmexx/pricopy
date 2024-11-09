import React, { Component } from "react";
import {Navbar} from "./navbar/Navbar";
import {Header} from "./Header";
import { Content } from "./Content";
import {authWrapper} from "./auth/AuthWrapper";

export const Admin = authWrapper(class extends Component {

constructor(props) {
        super(props);

        this.state = {
            shrinked: false
        }

        this.shrinkMenu = this.shrinkMenu.bind(this);
    }

    shrinkMenu() {
        this.setState({shrinked: !this.state.shrinked})
    }

  render() {
    let shrinked_class = this.state.shrinked ? " active" : "";
    return (
        <React.Fragment>
            <Navbar shrinked={this.state.shrinked} shrinkMenu={this.shrinkMenu}/>
            <div className={"page" + shrinked_class}>
              <Header/>
              <Content />
            </div>
        </React.Fragment>
    )
  }

})