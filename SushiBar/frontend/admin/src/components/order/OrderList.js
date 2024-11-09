import React, { Component } from "react";
import Globals from "../../Globals";

export class OrderList extends Component {

    constructor(props) {
        super(props);

        this.state =
        {
            orderStatus: Globals.ORDERS.ORDER_STATUS,
        }

        //console.log("OderList: ", this.props);
    }

  render() {
    if (this.props.orders == null || this.props.orders.length === 0 || this.props.orders.error === 401) {
      return <tr><td><h5 className="p-2">Brak zamówień</h5></td></tr>
    }
    return this.props.orders.map(p => {
        let trclass = "cursor-pointer";
        trclass += this.props.actualOrder.showOrder && this.props.actualOrder.orderId === p.id ? " table-primary" : "";
        return <React.Fragment key={p.id}>
          <tr key={p.id} onClick={() => this.props.openOrder(p.id)} className={trclass}>
              <th scope="row"><input type="checkbox" key={p.id} /></th>
              <td>{p.orderId}</td>
              <td>{this.state.orderStatus[p.status]}</td>
              <td>{p.user_first_last_name}</td>
              <td>{ p.order_items.map( (o , index) => o.product_name + (index < p.order_items.length-1 ? ", " : "")) }</td>
              <td>{p.comments}</td>
              <td>{new Intl.NumberFormat("pl-PL", {
                    style: "currency",
                    currency: "PLN",
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2
                  }).format(p.total_price)}</td>
              <td>{new Intl.DateTimeFormat("pl-PL", {
                year: "numeric",
                month: "numeric",
                day: "numeric"
              }).format(Date.parse(p.created))}</td>
          </tr>
        </React.Fragment>
    })
  }
}
