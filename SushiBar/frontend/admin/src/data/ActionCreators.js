import { ActionTypes } from "./ActionTypes";
import { RestDataSource } from "./RestDataSource";

const dataSource = new RestDataSource();

export const loadData = (dataType, params) => (
    {
        type: ActionTypes.DATA_LOAD,
        payload: dataSource.GetData(dataType, params).then( response => {
                return ({
                    dataType,
                    data: response.data,
                    total: Number(response.headers["x-total-count"]),
                    params
                })
            }
        ).catch(error => {
                return ({
                    dataType,
                    data: {error: error.response.status},
                    params
                })
            }
        )
    });

export const loadOrder =  (dataType, params, slug) => (
    {
        type: ActionTypes.DATA_LOAD,
        payload: dataSource.GetData(dataType, params, slug).then( response => {
                return ({
                    dataType,
                    data: response.data,
                })
            }
        ).catch(error => {
                return ({
                    dataType,
                    data: {error: error.response.status},
                })
            }
        )
    });

export const saveOrder = (dataType, order, params, slug) => (
    {
        type: ActionTypes.ORDER_SAVE,
        payload: dataSource.UpdateData(dataType, order, params, slug).then( response =>
          ({ dataType,
             data: response.data,
          })
        ).catch(error => {
                return ({
                    dataType,
                    data: {error: error.response.status},
                })
            }
        )
    });

export const canLoadOrder = (v) =>
    ({type: ActionTypes.ORDER_DATA_LOAD, payload: v});

export const setPageSize = (newSize) =>
  ({ type: ActionTypes.DATA_SET_PAGESIZE, payload: newSize });

export const clearData = () =>
    ({type: ActionTypes.DATA_CLEAR})