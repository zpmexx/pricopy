import React, { Component, lazy, Suspense } from "react";
import { BrowserRouter as Router, Route, Switch }
  from "react-router-dom";
import {Provider} from "react-redux";
import {AdminStoreDataStore} from "./data/DataStore";
import {AuthProviderImpl} from "./components/auth/AuthProviderImpl";

const Page = lazy(() => import("./Page"));

export default class App extends Component {


  render() {
    return <Provider store={AdminStoreDataStore}>
        <AuthProviderImpl>
            <Router>
              <div>
                  <Switch>
                      <Route path="/" render={
                        routeProps =>
                          <Suspense fallback={<h3>Wczytywanie...</h3>}>
                            <Page {...routeProps} />
                          </Suspense>
              } />
                  </Switch>
              </div>
            </Router>
        </AuthProviderImpl>
    </Provider>
  }
}
