import React, {Component} from 'react';
import PropTypes from "prop-types";

class ProductTableItem extends Component {
    render() {
        const { index, product_name, quantity, price } = this.props;
        return (
                <tr>
                    <th scope="row">{index+1}</th>
                    <td>{product_name}</td>
                    <td>{quantity}</td>
                    <td>{new Intl.NumberFormat("pl-PL", {
                    style: "currency",
                    currency: "PLN",
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2
                  }).format(price)}</td>
                    <td>{new Intl.NumberFormat("pl-PL", {
                    style: "currency",
                    currency: "PLN",
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2
                  }).format(price*quantity)}</td>
                </tr>
        );
    }
}

ProductTableItem.propTypes = {
    product: PropTypes.array
}

export default ProductTableItem;