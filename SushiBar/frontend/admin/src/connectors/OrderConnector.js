import React, {Component} from "react";
import { connect } from "react-redux";
import { withRouter } from "react-router-dom";
import {loadData, canLoadOrder} from "../data/ActionCreators";
import { DataTypes } from "../data/ActionTypes";
import { OrderPage } from "../components/order/OrderPage";
import {authWrapper} from "../components/auth/AuthWrapper";
import Globals from "../Globals";
import {Signoutp } from "../components/Signoutp";
import {OrderDetail} from "../components/order/OrderDetail";

const mapStateToProps = (dataStore) => ({
    dataStore: dataStore
})

const mapDispatchToProps = dispatch => ({
    loadData: (...args) => dispatch(loadData(...args)),
    canLoadOrder: (...args) => dispatch(canLoadOrder(...args))
})

export const OrderConnector =
    authWrapper(withRouter(connect(mapStateToProps, mapDispatchToProps)(
        class extends Component {
            constructor(props) {
                super(props);

                let timer = null;

                this.state = {
                    dataLoaded: false,
                    showOrder: false,
                    orderId: 0,
                }
                this.openOrder = this.openOrder.bind(this);
                this.closeOrder = this.closeOrder.bind(this);
                this.refreshOrders = this.refreshOrders.bind(this);
                const params = new URLSearchParams(this.props.history.location.search);
                const _orderId = params.get('order');
                if (_orderId) {
                    //console.log("_orderId ", _orderId);
                    this.setState({
                        orderId: _orderId,
                        showOrder: true
                    });
                }
            }

            refreshOrders() {
                this.getData(true);
            }

            openOrder(id, show = true) {
                //console.log(id);
                this.setState({
                    orderId: id,
                    showOrder: show
                });
                this.props.canLoadOrder(show);
                this.props.history.push({
                    path: this.props.history.path,
                    search: '?order='+id
                })
            }

            closeOrder() {
                this.setState({
                    orderId: 0,
                    showOrder: false
                });
                this.props.canLoadOrder(false);
            }

            componentDidUpdate() {
                //console.log("Admcon: ", this.props, "ss ", this.props.pageSize)
                this.getData();
            }

            render() {
                return (
                    <React.Fragment>
                        {
                            this.state.dataLoaded && this.props.dataStore.orders !== undefined && this.props.dataStore.orders.error === 401 ?
                                 <Signoutp/> :
                                <React.Fragment>
                                    <OrderPage orders={this.props.dataStore.orders} actualOrder={{orderId: this.state.orderId, showOrder: this.state.showOrder}} openOrder={this.openOrder}/>
                                    {this.state.showOrder ? <OrderDetail {...this.props} id={this.state.orderId} openOrder={this.openOrder} refreshOrders={this.refreshOrders}/> : ""}
                                </React.Fragment>
                        }
                    </React.Fragment>
                    )
            }

            componentDidMount() {
                //this.props.loadData(DataTypes.ORDERS);
                this.getData();
                this.setState({dataLoaded: true});
                const params = new URLSearchParams(this.props.history.location.search);
                //console.log("Params: ", params.get('order'));
                const _orderId = params.get('order');
                if (_orderId) {
                    this.openOrder(_orderId);
                }
                this.timer = setInterval(() => this.getData(true), 1000);
            }

            getData(trig=false) {
                const dsData = this.props.dataStore.orders_params || {};
                if (this.props.dataStore.orders_total && this.props.match.params.page > (Math.ceil(this.props.dataStore.orders_total / (this.props.dataStore.pageSize || Globals.PAGE_SIZE_MIN)) || 1)) {
                    window.history.pushState({}, null, Globals.URL_MAIN_PATH+`orders/1`);
                }
                const rtData = {
                  page_size: this.props.dataStore.pageSize || Globals.PAGE_SIZE_MIN,
                  page: this.props.match.params.page <= (Math.ceil(this.props.dataStore.orders_total / (this.props.dataStore.pageSize || Globals.PAGE_SIZE_MIN)) || 1) ? this.props.match.params.page : 1
                }


                if (Object.keys(rtData).find(key => dsData[key] !== rtData[key]) || trig) {
                  this.props.loadData(DataTypes.ORDERS, rtData);
                }
                //this.props.loadData(DataTypes.ORDERS, rtData);
              }

            componentWillUnmount() {
                //console.log("Umount");
                this.setState({dataLoaded: false});
                clearInterval(this.timer);
            }
        }
)))