import React, { Component } from "react";
import { withRouter } from "react-router-dom";
import { authWrapper } from "./AuthWrapper";
import { ValidatedForm } from "../../forms/ValidatedForm";

export const AuthPrompt = withRouter(authWrapper(class extends Component {

  constructor(props) {
    super(props);
    this.state = {
      errorMessage: null
    }
    this.defaultAttrs = { required: true };
    this.formModel = [
      { label: "Username", labelText: "Nazwa użytkownika", 
          attrs: { defaultValue: "admin" } },
      { label: "Password", labelText: "Hasło", 
          attrs: { type: "password" } },
    ];
  }

  authenticate = (credentials) => {
    this.props.authenticate(credentials)
      .catch(err => {
          let message = err.message;
          if (err.response && err.response.status === 401)
              message = "Nieprawidłowe dane uwierzytelniające!";
          this.setState({ errorMessage: message })
      })
      .then(this.props.history.push(this.props.location));
  }
  
  render = () =>
    <div className="container h-100 mt-5">
        <div className={"row h-100 justify-content-center align-items-center"}>
            <div className={"col-8 border rounded"}>
              <div className="row">
                <div className="col bg-dark text-white">
                  <div className="navbar-brand">Panel zamówień</div>
                </div>
              </div>
              <div className="row">
                <div className="col m-2">
                  {this.state.errorMessage != null &&
                    <h4 className="bg-danger text-center text-white m-1 p-2">
                      {this.state.errorMessage}
                    </h4>
                  }
                  <ValidatedForm formModel={this.formModel}
                    defaultAttrs={this.defaultAttrs}
                    submitCallback={this.authenticate}
                    submitText="Zaloguj"
                    cancelCallback={() => this.props.history.push("/")}
                  />
                </div>
              </div>
            </div>
      </div>
    </div>
}))  