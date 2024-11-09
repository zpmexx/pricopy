import React, {Component} from 'react';
import {productsWrapper} from "./Products";
import ProductsTable from "./ProductsTable";

const ProductsWithProductsTable = productsWrapper(ProductsTable);

class ProductsPage extends Component {
    render() {
        return (
            <ProductsWithProductsTable/>
        );
    }
}

export default ProductsPage;

