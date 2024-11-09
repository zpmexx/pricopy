const Globals = {
    PAGE_SIZE_MIN: 10,
    ORDERS: {
        ORDER_STATUS: {
            1: "Nowe",
            2: "Opłacone",
            3: "W trakcie realizacji",
            4: "Zrealizowane",
            5: "Anulowane"
        },
        STRING_ORDER_STATUS: {
            "new": 1,
            "paid": 2,
            "accept": 3,
            "complete": 4,
            "cancel": 5,
            "delete": 6
        }
    },
    URL_MAIN_PATH: "/kuchnia/",
}

export default Globals;