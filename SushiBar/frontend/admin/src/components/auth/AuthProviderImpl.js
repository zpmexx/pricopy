import React, { Component } from "react";
import Axios from "axios";
import { AuthContext } from "./AuthContext";
import { AuthUrl} from "../../data/Urls";

export class AuthProviderImpl extends Component {

  constructor(props) {
    super(props);
    const webToken = localStorage.getItem('webToken') || '';
    const refreshToken = localStorage.getItem('refreshToken') || '';
    const userid = localStorage.getItem('userid') || null;
    const username = localStorage.getItem('username') || null;
    const useradmin = localStorage.getItem('useradmin') || null;
    if(webToken.length>0) {
      this.state = {
        isAuthenticated: true,
        webToken: webToken,
        refreshToken: refreshToken,
        user: {
            userid: userid,
            username: username,
            isAdmin: useradmin
          }
      }
    }
    else
      this.state = {
        isAuthenticated: false,
        webToken: null,
        refreshToken: null,
        user: {
            userid: null,
            username: null,
            isAdmin: null
          }
      }

  }

  authenticate = (credentials) => {
    return Axios.post(AuthUrl+"obtain/", credentials).then(response => {
      if (response.status === 200) {
        if (response.data.admin !== true)
          throw new Error("Nieprawidłowe dane uwierzytelniające!");

      //console.log("Signin: ", response.data.access);
        localStorage.setItem("webToken", response.data.access);
        localStorage.setItem("refreshToken", response.data.refresh);

        this.setState({
          isAuthenticated: true,
          webToken: response.data.access,
          refreshToken: response.data.refresh,
          user: {
            userid: response.data.userid,
            username: response.data.username,
            isAdmin: response.data.admin
          }
        });

        localStorage.setItem("userid", this.state.user.userid);
        localStorage.setItem("username", this.state.user.username);
        localStorage.setItem("useradmin", this.state.user.admin);
        // console.log("ui", this.state.user.userid);

        const nextPage = localStorage.getItem("nextPage");
        if(nextPage !== undefined && nextPage !== null)
          window.location.href = nextPage;
      } else {
        throw new Error("Nieprawidłowe dane uwierzytelniające!");
      }
    })
  };

  signout = () => {
    //console.log("Signout");
    localStorage.removeItem("webToken");
    localStorage.removeItem("refreshToken");
    localStorage.removeItem("nextPage");
    localStorage.removeItem("userid");
    localStorage.removeItem("username");
    localStorage.removeItem("useradmin");
    this.setState({ isAuthenticated: false, webToken: null, refreshToken: null,
    user: {
        userid: null,
        username: null,
        isAdmin: null
    }});
  };

  render = () =>
    <AuthContext.Provider value={{
        ...this.state,
        authenticate: this.authenticate, signout: this.signout }}>
      {this.props.children}
    </AuthContext.Provider>
}