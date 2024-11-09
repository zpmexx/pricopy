import React, { Component } from "react";
import { OrderPaginationButtons } from "./OrderPaginationButtons";

export class OrderPaginationControls extends Component {
  constructor(props) {
    super(props);
    this.pageSizes = this.props.sizes || [10, 25, 100];
    this.handlePageSizeChange = this.handlePageSizeChange.bind(this);
  }

  handlePageSizeChange(ev) {
    this.props.setPageSize(ev.target.value);
  }
  
  render() {
    return <div className="m-2 d-flex">
      <div className="form-inline justify-content-center">
        <select className="form-control"
          onChange={(e) => this.handlePageSizeChange(e)}
          value={this.props.pageSize || this.pageSizes[0]}>
          {this.pageSizes.map(s =>
            <option value={s} key={s}>{s} na stronie</option>
          )}
        </select>
      </div>
      <div className="text-center m-1">
        <OrderPaginationButtons currentPage={this.props.currentPage}
          pageCount={this.props.pageCount}
          navigate={this.props.navigateToPage} />
      </div>
    </div>
  }
}          