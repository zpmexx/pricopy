import { DataTypes } from "./ActionTypes";

const protocol = "https";
const hostname = "sushibar.soft21.pl";

export const RestUrls = {
  [DataTypes.ORDERS]: `${protocol}://${hostname}/api/menu/orders/`,
  [DataTypes.ORDER]: `${protocol}://${hostname}/api/menu/orders/`,
  [DataTypes.PRODUCTS]: `${protocol}://${hostname}/api/menu/`,
}

export const AuthUrl = `${protocol}://${hostname}/api/token/`;