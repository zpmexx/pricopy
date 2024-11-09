import React, { Component } from "react";
import { authWrapper } from "./components/auth/AuthWrapper";
import { Route, Switch }
  from "react-router-dom";
import {AuthPrompt} from "./components/auth/AuthPrompt";
import {Admin} from "./components/Admin";

export default authWrapper(class extends Component {

  render() {
    return (
        <React.Fragment>
            <Switch>
              {
                !this.props.isAuthenticated &&
                    <Route component={AuthPrompt} />
              }
              <Route path="/" component={Admin} />
            </Switch>
        </React.Fragment>
    )
  }
})
