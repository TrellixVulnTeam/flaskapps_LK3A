/**
 * page.jsx: send current support vector 'submit button' boolean, indication
 *           whether it should be displayed to the redux store.
 *
 */

function setSvButton(action) {
    return {
        type: 'SUBMIT-SV-ANALYSIS',
        button: {
            submit_analysis: action.button.submit_analysis
        }
    };
}

function setGotoResultsButton(action) {
    return {
        type: 'GOTO-RESULTS',
        button: {
            goto_results: action.button.goto_results
        }
    };
}

function setResultsButton(action) {
    return {
        type: 'SET-RESULTS-BUTTON',
        button: {
            review_results: action.button.review_results
        }
    };
}

function setLayout(action) {
    return {
        type: 'SET-LAYOUT',
        layout: action.layout
    };
}

function setContentType(action) {
    return {
        type: 'SET-CONTENT-TYPE',
        content_type: action.layout
    };
}

function setSpinner(action) {
    return {
        type: 'SET-SPINNER',
        spinner: action.spinner
    };
}

function setRangeSlider(action) {
    if (action.type.toLowerCase() == 'penalty') {
        return {
            type: 'SET-PENALTY-SLIDER',
            slider: { penalty: action.slider.penalty }
        };
    }
    else if (action.type.toLowerCase() == 'gamma') {
        return {
            type: 'SET-GAMMA-SLIDER',
            slider: { gamma: action.slider.gamma }
        };
    }
}

// indicate which class can be exported, and instantiated via 'require'
export {
    setSvButton,
    setGotoResultsButton,
    setLayout,
    setContentType,
    setResultsButton,
    setSpinner,
    setRangeSlider
}
