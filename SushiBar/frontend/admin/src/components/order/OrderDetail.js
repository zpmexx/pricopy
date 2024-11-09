import React, {Component} from "react";

import {loadOrder, canLoadOrder, saveOrder} from "../../data/ActionCreators";
import {authWrapper} from "../auth/AuthWrapper";
import {connect} from "react-redux";
import {DataTypes} from "../../data/ActionTypes";
import ProductTable from "./product/ProductTable";
import Globals from "../../Globals";

const mapStateToProps = (dataStore) => ({
    dataStore: dataStore
})

const mapDispatchToProps = {
    loadOrder,
    saveOrder,
    canLoadOrder
}

export const OrderDetail =
    authWrapper(connect(mapStateToProps, mapDispatchToProps)(
        class extends Component {

            constructor(props) {
                super(props);

                this.state = {
                    oldId: 0,
                }

                this.scrollRef = React.createRef();
                this.refreshData = this.refreshData.bind(this);
                this.saveOrder = this.saveOrder.bind(this);
                this.statusOrderChangeEvent = this.statusOrderChangeEvent.bind(this);
            }

            statusOrderChangeEvent(status) {
                this.props.saveOrder(DataTypes.ORDER, {
                    ...this.props.dataStore.order,
                    status: status
                }, {}, this.props.dataStore.order.id);
                setTimeout(this.props.refreshOrders, 500);

            }

            saveOrder() {
                //this.props.saveOrder(DataTypes.ORDER, )
            }

            refreshData() {
                this.props.loadOrder(DataTypes.ORDER, {}, this.props.id);
            }

            componentDidUpdate() {
                //console.log("OrderDetail: ", this.props.id, " Old id: ", this.state.oldId);
                //  console.log("Can: ", this.props);
                //if(this.props.id != this.state.oldId) {
                if (this.props.dataStore.vcanLoadOrder) {
                    //console.log("Can: ", this.props.vcanLoadOrder);
                    this.props.canLoadOrder(false);
                    this.setState({oldId: this.props.id});
                    this.refreshData();
                    this.scrollRef.current.scrollIntoView({ behavior: 'smooth', block: 'start' });

                }
            }

            componentDidMount() {
                //console.log("OrderDetail: mount", this.props.id);
                this.setState({oldId: this.props.id});
                this.props.loadOrder(DataTypes.ORDER, {}, this.props.id);
                this.scrollRef.current.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }

            render() {
                const {order} = this.props.dataStore;
                return (
                        <React.Fragment>
                            <div className="page-order-details" ref={this.scrollRef}>
                                { order !== undefined && order.error === undefined ?
                                    <React.Fragment>
                                            <div className="container-fluid">
                                                <div
                                                    className="page-order-details-button d-flex align-items-center justify-content-between">
                                                    <div>
                                                        { order.status === Globals.ORDERS.STRING_ORDER_STATUS.paid ?
                                                            <button type="button" className="btn btn-warning button-status btn-sm" onClick={() => this.statusOrderChangeEvent(Globals.ORDERS.STRING_ORDER_STATUS.accept)}>Przyjmij do realizacji</button>
                                                            : ""
                                                        }
                                                        {order.status > Globals.ORDERS.STRING_ORDER_STATUS.new && order.status < Globals.ORDERS.STRING_ORDER_STATUS.complete ?
                                                            <button type="button" className="btn btn-success button-status btn-sm" onClick={() => this.statusOrderChangeEvent(Globals.ORDERS.STRING_ORDER_STATUS.complete)}>Zrealizowane</button>
                                                            : ""
                                                        }
                                                        { order.status < Globals.ORDERS.STRING_ORDER_STATUS.complete ?
                                                            <button type="button" className="btn btn-info button-status btn-sm" onClick={() => this.statusOrderChangeEvent(Globals.ORDERS.STRING_ORDER_STATUS.cancel)}>Anuluj</button>
                                                            : ""
                                                        }
                                                        {/*<button type="button" className="btn btn-danger button-status btn-sm" onClick={() => this.statusOrderChangeEvent(Globals.ORDERS.STRING_ORDER_STATUS.delete)}>Usuń zamówienie</button>*/}
                                                    </div>
                                                    <div>
                                                        {/*<button type="button" className="btn btn-secondary button-print"*/}
                                                        {/*        style={{marginRight: "17px"}}>Drukuj*/}
                                                        {/*</button>*/}
                                                        <button type="button" className="close" data-dismiss="modal" aria-label="Close" onClick={() => this.props.openOrder(0, false)}>
                                                            <span aria-hidden="true">&times;</span>
                                                        </button>
                                                    </div>
                                                </div>
                                            </div>
                                            <div className="page-order-refresh clearAfter">
                                                <div className="container-fluid clearAfter d-flex align-items-center">
                                                    <div className="page-order-number">
                                                        Nr zamówienia: {order ? order.orderId : ""}
                                                    </div>
                                                    <div className="page-order-status d-flex align-items-center">
                                                        <div style={{marginRight: "5px", float: "left"}}>Status:</div>
                                                        <select name="devices" className="form-control" value={order.status} onChange={e => this.statusOrderChangeEvent(e.target.value)}>
                                                            { Object.entries(Globals.ORDERS.ORDER_STATUS).map(([a, p]) =>
                                                                    <option value={a}>{p}</option>
                                                            )}
                                                        </select>
                                                    </div>
                                                    <div className="page-order-date">
                                                        Data i godzina zam.:
                                                    </div>
                                                    <div className="page-order-time">
                                                        {new Intl.DateTimeFormat("pl-PL", {
                                                            year: "numeric",
                                                            month: "numeric",
                                                            day: "numeric",
                                                            hour: "numeric",
                                                            minute: "numeric",
                                                          }).format(Date.parse(order.created))}
                                                    </div>
                                                </div>
                                            </div>
                                            <div className="page-order-board">
                                                <div className="container-fluid">
                                                    <div className="page-order-board-main row flex-row d-flex">
                                                        <div className="page-order-board-status col-md-8">
                                                            <div className="order-meal">
                                                                Zamówione dania:
                                                            </div>
                                                            <ProductTable products={order.order_items}/>
                                                            <div className="d-flex align-items-center justify-content-between">
                                                                <div>
                                                                    <div className="method-pay">
                                                                        Metoda płatności: płatność online
                                                                    </div>
                                                                    {/*<div className="discount">*/}
                                                                    {/*    Rabat: 10%*/}
                                                                    {/*</div>*/}
                                                                </div>
                                                                <div>
                                                                    <div className="order-price">
                                                                        Zamówienie: {new Intl.NumberFormat("pl-PL", {
                                                                                        style: "currency",
                                                                                        currency: "PLN",
                                                                                        minimumFractionDigits: 2,
                                                                                        maximumFractionDigits: 2
                                                                                      }).format(order.total_price)}
                                                                    </div>
                                                                    <div className="order-delivery">
                                                                        Koszt dostawy: 19 zł
                                                                    </div>
                                                                    <div className="order-summary">
                                                                        <b>Razem: {new Intl.NumberFormat("pl-PL", {
                                                                                        style: "currency",
                                                                                        currency: "PLN",
                                                                                        minimumFractionDigits: 2,
                                                                                        maximumFractionDigits: 2
                                                                        }).format(order.total_price+19)}</b>
                                                                    </div>
                                                                    {/*<div className="order-discount">*/}
                                                                    {/*    Po rabacie: 355,50 zł*/}
                                                                    {/*</div>*/}
                                                                </div>
                                                            </div>
                                                            {/*<div className="order-history">*/}
                                                            {/*    <div className="history">*/}
                                                            {/*        Historia zamówienia:*/}
                                                            {/*    </div>*/}
                                                            {/*    <div className="order-completed d-flex align-items-center justify-content-between">*/}
                                                            {/*        <div>Zamówienia zrealizowane</div>*/}
                                                            {/*        <div>05.05.2020 16:13</div>*/}
                                                            {/*    </div>*/}
                                                            {/*    <div className="order-accepted d-flex align-items-center justify-content-between">*/}
                                                            {/*        <div>Zamówienia przyjęte do realizacji</div>*/}
                                                            {/*        <div>05.05.2020 16:13</div>*/}
                                                            {/*    </div>*/}
                                                            {/*    <div className="order-paid d-flex align-items-center justify-content-between">*/}
                                                            {/*        <div>Zamówienia opłacone</div>*/}
                                                            {/*        <div>05.05.2020 16:13</div>*/}
                                                            {/*    </div>*/}
                                                            {/*    <div className="order-placed d-flex align-items-center justify-content-between">*/}
                                                            {/*        <div>Złożone zamówienia</div>*/}
                                                            {/*        <div>05.05.2020 16:13</div>*/}
                                                            {/*    </div>*/}
                                                            {/*</div>*/}
                                                            {/*<div className="order-other">*/}
                                                            {/*    Inne zamówienia użytkownika:*/}
                                                            {/*</div>*/}
                                                            {/*<table className="table table-hover table-responsive-md" style={{borderBottom: "1px solid", fontSize: "11px"}}>*/}
                                                            {/*    <thead>*/}
                                                            {/*        <tr>*/}
                                                            {/*            <th scope="col">Numer</th>*/}
                                                            {/*            <th scope="col">Status</th>*/}
                                                            {/*            <th scope="col">Przedmioty</th>*/}
                                                            {/*            <th scope="col">Kwota</th>*/}
                                                            {/*            <th scope="col">Data złożenia</th>*/}
                                                            {/*        </tr>*/}
                                                            {/*    </thead>*/}
                                                            {/*    <tbody>*/}
                                                            {/*        <tr>*/}
                                                            {/*            <th scope="row">1</th>*/}
                                                            {/*            <td>opłacone</td>*/}
                                                            {/*            <td>Hambuger</td>*/}
                                                            {/*            <td>120 zł</td>*/}
                                                            {/*            <td>2020.05.05</td>*/}
                                                            {/*        </tr>*/}
                                                            {/*    </tbody>*/}
                                                            {/*</table>*/}
                                                        </div>

                                                        <div className="page-order-board-contact col-md-4">
                                                            <div className="user-data">
                                                                Dane użytkownika:
                                                            </div>
                                                            <div className="name-user">
                                                                {order.user_first_last_name}
                                                            </div>
                                                            <div className="number-user">
                                                                tel. {order.phone_number}
                                                            </div>
                                                            {/*<div className="email-user">*/}
                                                            {/*    {order.}*/}
                                                            {/*</div>*/}
                                                            <br/>
                                                            <div className="delivery-address">
                                                                Adres dostawy:
                                                            </div>
                                                            <div className="address-user">
                                                                ul. {order.street} {order.house_number}{order.flat_number !== "" ? "/"+order.flat_number : ""}<br/>
                                                                {order.city}, {order.postal_code}
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                    </React.Fragment> : ""
                                    }
                            </div>
                        </React.Fragment>
                    )
            }
        }
))
