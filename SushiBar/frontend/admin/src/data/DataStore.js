import {createStore, applyMiddleware, compose} from "redux";
import { AdminReducer } from "./AdminReducer";
import { asyncActions } from "./AsyncMiddleware";
import {CommonReducer} from "./CommonReducer";

export const AdminStoreDataStore = createStore(CommonReducer(AdminReducer), applyMiddleware(asyncActions));