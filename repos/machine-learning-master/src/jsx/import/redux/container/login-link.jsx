/**
 * login-link.jsx: redux store for login, and logout processes.
 *
 * Note: this script implements jsx (reactjs) syntax.
 *
 * Note: importing 'named export' (multiple export statements in a module),
 *       requires the object being imported, to be surrounded by { brackets }.
 *
 */

import React from 'react';
import { connect } from 'react-redux';
import LoginLink from '../../navigation/menu-items/login.jsx';
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
const LoginLinkState = connect(
    mapStateToProps,
    mapDispatchToProps
)(LoginLink)

// indicate which class can be exported, and instantiated via 'require'
export default LoginLinkState
