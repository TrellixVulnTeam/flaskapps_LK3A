var Router = ReactRouter.Router;
var Route = ReactRouter.Route;
var browserHistory = ReactRouter.browserHistory;

//global variable to store origin url (e.g http://localhost:5000)
var origin = window.location.origin;

// Helper to show materialize toasts
function toast(message){
   Materialize.toast(message, 5000);
}

var PollForm = React.createClass({

  getInitialState: function(e){
    // set initial state of form inputs

    // close poll in 24 hours by default
    var close_date = new Date();
    close_date.setHours(close_date.getHours() + 23);
    close_date = close_date.getTime() / 1000;


    return {title: '', option: '', options: [], close_date: close_date}
  },

  handleTitleChange: function(e){
    //change title as the user types
    this.setState({title: e.target.value});
  },

  handleOptionChange: function(e){
    this.setState({option: e.target.value});
  },

  handleOptionAdd: function(e){
    //update poll options and reset options to an empty string
    this.setState({
    options: this.state.options.concat({name: this.Option.value}),
    option: ''
    });
  },

  componentDidMount: function(){

    var url =  origin + '/api/polls/options'

    //get all options
    $.ajax({
      url: url,
      dataType: 'json',
      cache: false,
      success: function(options) {
        // Initialize autocomplete form element
        $('input.autocomplete').autocomplete({
          data: options
        });

      }.bind(this),
      error: function(xhr, status, err) {
        console.error(url, status, err.toString());
      }.bind(this)
    });

  },

  handleSubmit: function(e){
    e.preventDefault();
    var title = this.state.title;
    var options = this.state.options;
    var close_date = this.state.close_date;

    var data = {title: title,
                options: options.map(function(x){return x.name}),
                close_date: close_date
              };

    var url =  origin + '/api/polls';

    // make post request
    $.ajax({
      url: url,
      dataType: 'json',
      type: 'POST',
      data: JSON.stringify(data),
      contentType: 'application/json; charset=utf-8',
      success: function(data){
        toast(data.message);
      }.bind(this),
      error: function(xhr, status, err){
        toast('Poll creation failed: ' + err.toString());
      }.bind(this)
    });
  },

  render: function(){

    return (
      <div className="container">
        <div className="row">
          <div id="poll" className="card col s12 m5">
            <form onSubmit={this.handleSubmit}>
              <h5 className="center">Create a poll</h5>

              <div className="input-field col s12">
                <i className="material-icons prefix">mode_edit</i>
                <input id="title" type="text" onChange={this.handleTitleChange} required />
                <label htmlFor="title">Title</label>
              </div>

              <div className="input-field col s12">
                <i className="material-icons prefix">speaker_notes</i>

                {/* We're using refs because for some weird reason react doesn't trap the change event triggered by
                    Materialize css autocomplete's widget, The input is still a controlled componenet
                    so we can clear the option field once an option is added */}
                <input id="options" type="text" className="autocomplete" ref={(input) => { this.Option = input; }}
                onChange={this.handleOptionChange} value={this.state.option} />
                <label htmlFor="options">Option</label>
              </div>

              <div id="create-poll" className="input-field col s12">
                <button className="waves-effect waves-light btn" type="button" onClick={this.handleOptionAdd}><i className="material-icons left">playlist_add</i>Add option</button>
                <button className="waves-effect waves-light btn" type="submit"><i className="material-icons left">cloud</i>Save</button>
              </div>
              <br />
            </form>
          </div>

          <div className="center">
            <LivePreview title={this.state.title} options={this.state.options} classContext={'col s12 m7'} />
          </div>
        </div>
      </div>
    );
  }
});

var LivePreview = React.createClass({

  getInitialState: function(){
    return {selected_option: '', disabled: 0};
  },

  handleOptionChange: function(e){
    this.setState({selected_option: e.target.value });
  },


  voteHandler: function(e){
    e.preventDefault();

    var data = {"poll_title": this.props.title, "option": this.state.selected_option};

    //calls props handler
    this.props.voteHandler(data);

    //disable the button
    this.setState({disabled: 1});

  },

  componentDidMount: function(){

    $(document).ready(function(){
      $('.collapsible').collapsible();
    });

  },

  render: function(){
    var options = this.props.options.map(function(option){

      if(option.name) {

        // calculate progress bar percentage
        var progress = Math.round((option.vote_count / this.props.total_vote_count) * 100) || 0
        var current = {width: progress+"%"}

        return (

          <li key={option.name}>
            <div className="collapsible-header">
              <p>
                <input name="options" type="radio" id={option.name} value={option.name} onChange={this.handleOptionChange} />
                <label htmlFor={option.name}>{option.name}</label>
              </p>
              <div className="progress">
                <div className="determinate" style={current}></div>
              </div>
            </div>
            <div className="collapsible-body"><p>{option.name}</p></div>
          </li>
        );
      }
    }.bind(this));

    return(

            <div className={this.props.classContext}>
              <div className="card blue-grey darken-3">
                <div className="card-content white-text">
                  <span className="card-title">{this.props.title}</span>

                  <form onSubmit={this.voteHandler}>
                    <ul className="collapsible" data-collapsible="accordion">
                      {options}
                    </ul>

                    <div className="card-action">
                      <button type="submit" disabled={this.state.disabled}
                      className="btn btn-success">Vote!</button>
                        <p>{this.props.total_vote_count} Votes so far
                        <i style={{marginLeft: '10px', paddingRight: '5px', verticalAlign: 'middle'}} className="tiny material-icons">schedule</i>
                        {this.props.close_date}</p>
                    </div>
                  </form>
                </div>
              </div>
            </div>
          )
        }
      });


var LivePreviewProps = React.createClass({

  voteHandler: function(data){

    var url =  origin + '/api/poll/vote'

    // make patch request
    $.ajax({
      url: url,
      dataType: 'json',
      type: 'PATCH',
      data: JSON.stringify(data),
      headers: {"Authorization": "Bearer " + localStorage.getItem('id_token')},
      contentType: 'application/json; charset=utf-8',
      success: function(data){
        // Show toast
        toast(data.message, 4000);

        this.setState({selected_option: ''});
        this.props.loadPollsFromServer();
      }.bind(this),

      error: function(xhr, status, err){
        err = err.toString();
        Rollbar.error(err);
      }.bind(this),

      statusCode: {
      401: function (response) {
         swat('Oops!', 'You have to login before you can vote', 'error');
       }
     }
   });

  },


  render: function(){
    var polls = this.props.polls.Polls.map(function(poll){

      var minutes = Math.floor((Date.parse(poll.close_date) - Date.now()) / (60000));
      var time_remaining = '';

      if(minutes > 1 && minutes < 59){
        time_remaining += minutes + ' minutes remaining';
      }

      else if(minutes < 1380){
        var hours =  Math.floor(minutes / 60);
        time_remaining += hours + ' hours remaining';
      }

      else {
        var days = Math.floor(minutes / (24 * 60));
        time_remaining += days + ' days remaining';
      }

      return (
        <LivePreview key={poll.title} title={poll.title} options={poll.options}
        total_vote_count={poll.total_vote_count} voteHandler={this.voteHandler}
        close_date={time_remaining} classContext={this.props.classContext} />
    );
  }.bind(this));

    return (
          <div className="section">
            <div className="row">
              <div className="row">
                {polls}
              </div>
            </div>
        </div>
    );
  }
});

var AllPolls = React.createClass({

  getInitialState: function(){
    // pollName is available as a prop
    this.pollName = this.props.routeParams.pollName

    this.classContext = this.pollName ? 'col s12 m4 offset-m4' : 'col 12 m4'
    return {polls: {'Polls': []}, header: '', loading: true};
  },

  loadPollsFromServer: function(){

    if(this.pollName){
        var url = origin + '/api/poll/' + this.pollName

    } else {
        var url = origin + '/api/polls'
        this.setState({header: 'Latest polls'})
    }

    //make get request
    $.ajax({
      url: url,
      dataType: 'json',
      cache: false,
      success: function(data) {
        this.setState({polls: data, loading: false});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(url, status, err.toString());
      }.bind(this)
    });
  },

  componentDidMount: function(){
    this.loadPollsFromServer();
  },

  render: function(){

    if(!this.state.loading){

      // if a message was not returned show the poll
      if(!this.state.polls.message){

        return (
          <LivePreviewProps polls={this.state.polls} loadPollsFromServer={this.loadPollsFromServer}
          header={this.state.header} classContext={this.classContext} />
          );

      }else{

        return (
            <div className="center">
              <h1 className="red-text">Poll not found</h1>
              <p>The poll may have closed, or you don't have the right link</p>
            </div>
          );

      }
    } else {
        return (
          <div className="center">
            <div className="preloader-wrapper small active">
              <div className="spinner-layer spinner-green-only">
                <div className="circle-clipper left">
                  <div className="circle"></div>
                </div><div className="gap-patch">
                  <div className="circle"></div>
                </div><div className="circle-clipper right">
                  <div className="circle"></div>
                </div>
              </div>
            </div>
          </div>
        );
      }
    }
  });

ReactDOM.render((
  <Router history={browserHistory}>
    <Route path="/" component={AllPolls} />
    <Route path="/polls" component={PollForm} />
    <Route path="/polls/:pollName" component={AllPolls} />
  </Router>
  ),
  document.getElementById('polls-container')
);
