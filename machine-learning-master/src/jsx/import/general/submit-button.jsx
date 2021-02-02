/**
 * submit-button.jsx: append dynamic submit button.
 *
 * @Submit, must be capitalized in order for reactjs to render it as a
 *     component. Otherwise, the variable is rendered as a dom node.
 *
 * Note: this script implements jsx (reactjs) syntax.
 */

import React, { Component } from 'react';
import PropTypes from 'prop-types';

class Submit extends Component {
    // prob validation: static method, similar to class A {}; A.b = {};
    static propTypes = {
        btnDisabled: PropTypes.bool,
        btnValue: PropTypes.string,
        cssClass: PropTypes.string,
        onClick: PropTypes.func,
    }

    render() {
        const disabled = this.props.btnDisabled ? true : false;
        const buttonValue = this.props.btnValue ? this.props.btnValue : 'Submit';
        const clickCallback = this.props.onClick ? this.props.onClick : null;
        const cssClass = this.props.cssClass ? this.props.cssClass : 'form-submit';

        return (
            <input
                className={cssClass}
                disabled={disabled}
                onClick={clickCallback}
                type='submit'
                value={buttonValue}
            />
        );
    }
}

// indicate which class can be exported, and instantiated via 'require'
export default Submit;
