import React, {Component} from 'react';
import PropTypes from 'prop-types';
import ProductsTableHeader from "./ProductsTableHeader";
import ProductsTableItem from "./ProductsTableItem";

class ProductsTable extends Component {
    render() {
        const { products } = this.props;
        return (
            <table className={"table table-hover table-responsive-md table-striped"}>
                <ProductsTableHeader/>
                <tbody>
                    { products.map((product, index) => <ProductsTableItem product={product} index={index} key={product.slug}/>) }
                </tbody>
            </table>
        );
    }
}

ProductsTable.propTypes = {
    products: PropTypes.array,
};

export default ProductsTable;
