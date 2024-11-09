import React, {Component} from 'react';

class ProductsTableHeader extends Component {
    render() {
        return (
            <thead>
                <tr>
                    <th>
                        Nr.
                    </th>
                    <th>
                        Nazwa
                    </th>
                    <th>
                        Cena
                    </th>
                </tr>
            </thead>
        );
    }
}

export default ProductsTableHeader;