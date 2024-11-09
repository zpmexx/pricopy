import React, { Component } from "react";
import { authWrapper } from "./auth/AuthWrapper";
import { Redirect }  from "react-router-dom";
import { connect} from "react-redux";
import { clearData } from "../data/ActionCreators";
import Globals from "../Globals";

const mapStateToProps = (dataStore) => ({
    dataStore: dataStore
})

const mapDispatchToProps = dispatch => ({
    clearData: () => dispatch(clearData),
    })

export const Signoutp = authWrapper(connect(mapStateToProps, mapDispatchToProps)(class extends Component {

  render() {
    //console.log(this.props.dataStore);
    return (
        <React.Fragment>
            { this.props.signout() }
            <Redirect to={{pathname: Globals.URL_MAIN_PATH, state: {referer: this.props.location}}}/>;
        </React.Fragment>
    )
  }
}))
