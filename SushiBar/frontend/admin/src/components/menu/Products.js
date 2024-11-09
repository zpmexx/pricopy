import React, {Component} from 'react';
import { connect } from "react-redux";
import { loadData } from "../../data/ActionCreators";
import { DataTypes } from "../../data/ActionTypes";

export const productsWrapper = (ProductsTable) => {

    const mapStateToProps = (dataStore) => ({
        dataStore: dataStore
    });

    const mapDispatchToProps = dispatch => ({
        loadData: (...args) => dispatch(loadData(...args)),
    });

    class Products extends Component {
        constructor(props) {
            super(props);
            this.props.loadData(DataTypes.PRODUCTS);
        }
        render() {
            const { products } = this.props.dataStore;
            return (
                <ProductsTable products={products || []}/>
            );
        }
    }

    return connect(mapStateToProps, mapDispatchToProps)(Products);
};

