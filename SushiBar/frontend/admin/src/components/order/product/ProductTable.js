import React, {Component} from 'react';
import PropTypes from "prop-types";
import ProductTableItem from "./ProductTableItem";

class ProductTable extends Component {
    render() {
        const { products } = this.props;
        return (
                <table className="table table-hover table-responsive-md" style={{borderBottom: "1px solid"}}>
                    <thead>
                        <tr>
                            <th scope="col">Nr</th>
                            <th scope="col">Nazwa</th>
                            <th scope="col">Ilość</th>
                            <th scope="col">Cena</th>
                            <th scope="col">Wartość</th>
                        </tr>
                    </thead>
                    <tbody>
                        { products.map( (product, index) => <ProductTableItem index={index} {...product}/>) }
                    </tbody>
                </table>
        );
    }
}

ProductTable.propTypes= {
    products: PropTypes.array
}

export default ProductTable;

