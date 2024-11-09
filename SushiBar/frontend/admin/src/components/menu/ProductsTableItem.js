import React, {Component} from 'react';

class ProductsTableItem extends Component {
    render() {
        const { product, index } = this.props;
        return (
            <tr key={product.slug}>
                <td>
                    { index+1 }
                </td>
                <td>
                    { product.name }
                </td>
                <td>
                    { product.price }
                </td>
            </tr>
        );
    }
}

export default ProductsTableItem;