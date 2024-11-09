import React from "react";

export const AuthContext = React.createContext({
  isAuthenticated: false,
  webToken: null,
  refreshToken: null,
  user: {
    userid: null,
    username: null,
    isAdmin: null
  },
  authenticate: (username, password) => { },
  signout: () => { }
})