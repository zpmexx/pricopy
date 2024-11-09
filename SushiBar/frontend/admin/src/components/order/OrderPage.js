import React, { Component } from "react";
import { OrderList } from "./OrderList";
import {OrderHeader} from "./OrderHeader";
import {OrderPageConnector} from "./OrderPageConnector";
import {OrderPaginationControls} from "./OrderPaginationControls";

const OrdersPages = OrderPageConnector(OrderPaginationControls);

export class OrderPage extends Component {
    render()  {
        const { orders, openOrder, actualOrder } = this.props;
        return <React.Fragment>
            <OrderHeader/>
            <div className="page-status">
                <div className="container-fluid">
                    <div className="d-flex align-items-center justify-content-between">
                        {/*<div className="page-status-order">*/}
                        {/*    <select className="page-status-order-devices form-control" name="devices">*/}
                        {/*        <option value="status">Wybierz status zamówienia</option>*/}
                        {/*        <option value="status">Wybierz status zamówienia</option>*/}
                        {/*        <option value="status">Wybierz status zamówienia</option>*/}
                        {/*    </select>*/}
                        {/*    /!*<button className="btn btn-secondary btn-sm" type="button">Odśwież</button>*!/*/}
                        {/*</div>*/}
                        {/*<div className="page-status-date">*/}
                        {/*    <div className="interval-time">Przedział czasowy</div>*/}
                        {/*    <div className="interval-time-option">*/}
                        {/*        <select className="interval-time-option-devices selectpicker" name="devices" data-width="100%">*/}
                        {/*            <option value="time">Dzień</option>*/}
                        {/*            <option value="time">Miesiąc</option>*/}
                        {/*            <option value="time">Rok</option>*/}
                        {/*        </select>*/}
                        {/*    </div>*/}
                        {/*    <div className="interval-date">*/}
                        {/*        <label htmlFor="start">Data od</label>*/}
                        {/*        <input type="date" id="start" />*/}
                        {/*        <label htmlFor="end">Data od</label>*/}
                        {/*        <input type="date" id="end" />*/}
                        {/*    </div>*/}
                        {/*</div>*/}
                    </div>
                </div>
            </div>
            <div className="page-order">
                <div className="container-fluid">
                    <div className="d-flex align-items-center justify-content-end">
                        {/*<div className="page-order-search">*/}
                        {/*    <input className={"form-control mr-sm-2"} type="search" name="search" placeholder="Szukaj" style={{width: "186px"}} />*/}
                        {/*</div>*/}
                        <div className="page-order-side">
                            <OrdersPages/>
                        </div>
                    </div>
                </div>
            </div>
            <div className="page-category">
                <div className="container-fluid">
                    <table className="table table-hover table-responsive-md table-striped">
                        <thead>
                        <tr>
                            <th scope="col"><input type="checkbox" /></th>
                            <th scope="col">Numer</th>
                            <th scope="col">Status</th>
                            <th scope="col">Imię i Nazwisko</th>
                            <th scope="col">Przedmioty</th>
                            <th scope="col">Uwagi</th>
                            <th scope="col">Kwota</th>
                            <th scope="col">Data zamówienia</th>
                        </tr>
                        </thead>
                        <tbody>
                            <OrderList orders={orders} openOrder={openOrder} actualOrder={actualOrder}/>
                        </tbody>
                    </table>
                </div>
            </div>
            <div className="page-category-option">
                <div className="container-fluid">
                    <div className="category-button form-inline m-2 d-flex flex-row justify-content-start align-items-center ">
                        {/*Zaznaczone*/}
                        {/*<select className={"category-button-devices form-control"} name="devices" style={{marginRight: "5px", marginLeft: "5px"}}>*/}
                        {/*    <option value="delete">usuń</option>*/}
                        {/*    <option value="delete">usuń</option>*/}
                        {/*    <option value="delete">usuń</option>*/}
                        {/*</select>*/}
                        {/*<button className="btn btn-secondary btn-sm" type="button">Wykonaj</button>*/}
                    </div>
                </div>
            </div>
        </React.Fragment>
    }
}