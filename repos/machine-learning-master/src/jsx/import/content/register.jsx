/**
 * register.jsx: registration form.
 *
 * @RegisterForm, must be capitalized in order for reactjs to render it as a
 *     component. Otherwise, the variable is rendered as a dom node.
 *
 * Note: this script implements jsx (reactjs) syntax.
 */

import React, { Component } from 'react';
import { Redirect } from 'react-router-dom';
import { setLayout, setSpinner } from '../redux/action/page.jsx';
import setLoginState from '../redux/action/login.jsx';
import ajaxCaller from '../general/ajax-caller.js';
import checkValidString from '../validator/valid-string.js';
import checkValidEmail from '../validator/valid-email.js';
import checkValidPassword from '../validator/valid-password.js';
import PropTypes from 'prop-types';

class RegisterForm extends Component {
    // prob validation: static method, similar to class A {}; A.b = {};
    static propTypes = {
        dispatchLayout: PropTypes.func,
        dispatchSpinner: PropTypes.func,
        user: PropTypes.shape({ name: PropTypes.string.isRequired, }),
    }

    constructor() {
        super()
        this.state = {
            ajax_done_result: null,
            validated_username: true,
            validated_email: true,
            validated_password: true,
            validated_username_server: true,
            validated_email_server: true,
            validated_password_server: true,
            value_username: '',
            value_email: '',
            value_password: '',
        };
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleEmail = this.handleEmail.bind(this);
        this.handlePassword = this.handlePassword.bind(this);
        this.handleUsername = this.handleUsername.bind(this);
    }

    componentWillMount() {
        // update redux store
        const action = setLayout({ layout: 'register' });
        this.props.dispatchLayout(action);
    }

    // send form data to serverside on form submission
    handleSubmit(event) {
        // prevent page reload
        event.preventDefault();

        // display spinner
        const action = setSpinner({ spinner: true });
        this.props.dispatchSpinner(action);

        // local variables
        const ajaxEndpoint = '/register';
        const ajaxArguments = {
            data: new FormData(this.refs.registerForm),
            endpoint: ajaxEndpoint,
        };

        if (
            !!this.state.value_username &&
            !!this.state.value_email &&
            !!this.state.value_password
        ) {
            // asynchronous callback: ajax 'done' promise
            ajaxCaller(
                (asynchObject) => {
                    // Append to DOM
                    if (asynchObject && asynchObject.error) {
                        this.setState({ ajax_done_error: asynchObject.error });
                    } else if (asynchObject) {
                        // local variables
                        const result = asynchObject;
                        const status = (!!result && result.status >= 0) ? result.status : null;

                        // backend validation: server handles one error at a time
                        if (!!status || status == 0) {
                            const action = setSpinner({ spinner: false });
                            switch (status) {
                            case 0:
                                this.setState({ ajax_done_result: result });
                                break;
                            case 1:
                                this.setState({ validated_password_server: false });
                                this.props.dispatchSpinner(action);
                                break;
                            case 2:
                                this.setState({ validated_username_server: false });
                                this.props.dispatchSpinner(action);
                                break;
                            case 3:
                                this.setState({ validated_email_server: false });
                                this.props.dispatchSpinner(action);
                                break;
                            }
                        }
                    }
                },
                // asynchronous callback: ajax 'fail' promise
                (asynchStatus, asynchError) => {
                    if (asynchStatus) {
                        this.setState({ ajax_fail_status: asynchStatus });
                        console.log(`Error Status: ${asynchStatus}`);
                    }
                    if (asynchError) {
                        this.setState({ ajax_fail_error: asynchError });
                        console.log(`Error Thrown: ${asynchError}`);
                    }
                },
                // pass ajax arguments
                ajaxArguments,
            );
        } else {
            if (!this.state.value_username) {
                this.setState({ validated_username: false });
            }
            if (!this.state.value_email) {
                this.setState({ validated_email: false });
            }
            if (!this.state.value_password) {
                this.setState({ validated_password: false });
            }

            const action = setSpinner({ spinner: false });
            this.props.dispatchSpinner(action);
        }
    }

    handlePassword(event) {
        const password = event.target.value;
        const check = !!checkValidPassword(password);
        if (!check) {
            const action = setSpinner({ spinner: false });
            this.props.dispatchSpinner(action);
        }

        this.setState({ validated_password_server: true });
        this.setState({ validated_password: check });
        this.setState({ value_password: password });
    }

    handleUsername(event) {
        const username = event.target.value;
        const check = !!checkValidString(username);
        if (!check) {
            const action = setSpinner({ spinner: false });
            this.props.dispatchSpinner(action);
        }

        this.setState({ validated_username_server: true });
        this.setState({ validated_username: check });
        this.setState({ value_username: username });
    }

    handleEmail(event) {
        const email = event.target.value;
        const check = !!checkValidEmail(email);
        if (!check) {
            const action = setSpinner({ spinner: false });
            this.props.dispatchSpinner(action);
        }

        this.setState({ validated_email_server: true });
        this.setState({ validated_email: check });
        this.setState({ value_email: email });
    }

    // triggered when 'state properties' change
    render() {
        // frontend validation
        const usernameClass = this.state.validated_username ? '' : 'invalid';
        const passwordClass = this.state.validated_password ? '' : 'invalid';

        if (this.state.validated_email) {
            var emailClass = '';
            var emailNote = '';
        } else {
            var emailClass = 'invalid';
            var emailNote = (
                <span className={emailClass}>
                    {'Please provide a valid email.'}
                </span>
            );
        }

        // backend validation
        if (!this.state.validated_password_server) {
            var passwordNote = (
                <span className='invalid'>
                    {'(Password requirement not met)'}
                </span>
            );
        } else {
            var passwordNote = null;
        }

        if (!this.state.validated_username_server) {
            var usernameNote = (
                <span className='invalid'>
                    {'(Username is taken)'}
                </span>
            );
        } else {
            var usernameNote = null;
        }

        if (!this.state.validated_email_server) {
            var emailNote = (
                <span className='invalid'>
                    {'(Email has already registered)'}
                </span>
            );
        } else {
            var emailNote = null;
        }

        if (
            this.state.ajax_done_result &&
            this.state.ajax_done_result.status == '0'
        ) {
            var redirect = <Redirect to='/login' />;
        } else {
            var redirect = null;
        }

        return (
            <form
                onSubmit={this.handleSubmit}
                ref='registerForm'
            >
                {redirect}
                <div className='form-group'>
                    <label className={`form-label ${usernameClass}`}>
                        {'Username'}
                    </label>
                    <input
                        className='input-block'
                        name='user[login]'
                        onInput={this.handleUsername}
                        placeholder='Pick a username'
                        type='text'
                        value={this.state.value_username}
                    />
                    <p className={`note ${usernameClass}`}>
                        {'This will be your username. {usernameNote}'}
                    </p>
                </div>

                <div className='form-group'>
                    <label className={`form-label ${emailClass}`}>
                        {'Email Address'}
                    </label>
                    <input
                        className='input-block'
                        name='user[email]'
                        onInput={this.handleEmail}
                        placeholder='Your email address'
                        type='text'
                        value={this.state.value_email}
                    />
                    <p className='note'>
                        {`
                            You will get updates regarding account changes,
                            or activitites. This email address will not be
                            shared with anyone. ${emailNote}
                        `}
                    </p>
                </div>

                <div className='form-group'>
                    <label className={`form-label ${passwordClass}`}>
                        {'Password'}
                    </label>
                    <input
                        className='input-block'
                        name='user[password]'
                        onInput={this.handlePassword}
                        placeholder='Create a password'
                        type='password'
                        value={this.state.value_password}
                    />
                    <p className={`note ${passwordClass}`}>
                        {`
                            Use at least one letter, one numeral,
                            and ten characters. ${passwordNote}
                        `}
                    </p>
                </div>

                <input
                    className='btn btn-primary'
                    type='submit'
                    value='Create an account'
                />
            </form>
        );
    }
}

// indicate which class can be exported, and instantiated via 'require'
export default RegisterForm;
