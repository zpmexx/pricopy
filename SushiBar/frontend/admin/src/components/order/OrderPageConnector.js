import { connect } from "react-redux";
import { withRouter } from "react-router-dom";
import { setPageSize } from "../../data/ActionCreators";
import Globals from "../../Globals";

const mapStateToProps = dataStore => dataStore;
const mapDispatchToProps = { setPageSize };

const mergeProps = (dataStore, actionCreators, router) => {
  let pageCount = Math.ceil((dataStore.orders_total || dataStore.pageSize || Globals.PAGE_SIZE_MIN) / (dataStore.pageSize || Globals.PAGE_SIZE_MIN));
  let currentPage =  router.match.params.page > pageCount ? pageCount : router.match.params.page;
    return {
  ...dataStore, ...router, ...actionCreators,
  currentPage: Number(currentPage),
  pageCount: pageCount,
  navigateToPage: (page) => {
    router.history.push(Globals.URL_MAIN_PATH+`orders/${page}`)
  },
}
}

export const OrderPageConnector = (PageComponent) =>
  withRouter(connect(mapStateToProps, mapDispatchToProps,
    mergeProps)(PageComponent))  