import { ActionTypes } from "./ActionTypes";

export const AdminReducer = (storeData, action) => {
    switch (action.type) {
        case ActionTypes.DATA_LOAD:
            return {
                ...storeData,
                [action.payload.dataType]: action.payload.data,
                [`${action.payload.dataType}_total`]: action.payload.total,
                [`${action.payload.dataType}_params`]: action.payload.params
            };
        case ActionTypes.ORDER_SAVE:
            return {
                ...storeData,
                [action.payload.dataType]: action.payload.data,
            };
        case ActionTypes.ORDER_DATA_LOAD:
            return {...storeData, vcanLoadOrder: action.payload}
        case ActionTypes.DATA_SET_PAGESIZE:
            return { ...storeData, pageSize: action.payload }
        case ActionTypes.DATA_CLEAR:
            storeData = undefined
        default:
            return storeData || {};
    }
}