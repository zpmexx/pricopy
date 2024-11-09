import React, { Component } from "react";
import {Redirect, Route, Switch} from "react-router-dom";
import {OrderConnector} from "../connectors/OrderConnector";
import {Contact} from "./contact/Contact";
import ProductsPage from "./menu/ProductsPage";
import Globals from "../Globals";

export class Content extends Component {
    render() {
        return (
                <Switch>
                    <Redirect from={Globals.URL_MAIN_PATH} to={Globals.URL_MAIN_PATH+"orders/1"} exact={true} />
                    <Redirect from={Globals.URL_MAIN_PATH+"orders"} to={Globals.URL_MAIN_PATH+"orders/1"} exact={true} />
                    <Route path={Globals.URL_MAIN_PATH+"orders/:page?"}
                       render={(routeProps) =>
                            <OrderConnector {...routeProps}/>
                       }/>
                    <Route path={Globals.URL_MAIN_PATH+"contact"} component={Contact}/>
                    <Route path={Globals.URL_MAIN_PATH+"menu"} render={(props) => <ProductsPage {...props}/>}/>
                    <Redirect to={Globals.URL_MAIN_PATH} />
                </Switch>
        )
    }
}