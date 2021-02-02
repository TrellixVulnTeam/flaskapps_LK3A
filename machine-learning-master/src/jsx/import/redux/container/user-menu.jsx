/**
 * user-menu.jsx: redux store for the main user menu.
 *
 * Note: this script implements jsx (reactjs) syntax.
 *
 * Note: importing 'named export' (multiple export statements in a module),
 *       requires the object being imported, to be surrounded by { brackets }.
 *
 */

import React from 'react';
import { connect } from 'react-redux';
import UserMenu from '../../navigation/user-menu.jsx';
import setLogoutState from '../action/logout.jsx';

// transforms redux state tree to react properties
const mapStateToProps = (state) => {
  // validate username
    if (state && state.user && !!state.user.name) {
        var username = state.user.name
    } else {
        var username = 'anonymous'
    }

  // return redux to state
    return {
        user: {
            name: username
        }
    }
}

// wraps each function of the object to be dispatch callable
const mapDispatchToProps = (dispatch) => {
    return {
        dispatchLogout: dispatch.bind(setLogoutState)
    }
}

// pass selected properties from redux state tree to component
const UserMenuState = connect(
    mapStateToProps,
    mapDispatchToProps
)(UserMenu)

// indicate which class can be exported, and instantiated via 'require'
export default UserMenuState
