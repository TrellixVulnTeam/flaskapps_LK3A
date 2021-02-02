import React from 'react';
import { NavLink } from 'react-router-dom';


const NavbarBrand = () => (
  <NavLink to='/' className="nav-item nav-link" href="#">
    <span className="navbar-brand">
      <img src="img/logo_white.png" width="175px" />
    </span>
  </NavLink>
);

const Navbar = () => (
  <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
  <NavbarBrand/>
  <button className="navbar-toggler" type="button"
      data-toggle="collapse"
      data-target="#navbarNavAltMarkup"
      aria-controls="navbarNavAltMarkup"
      aria-expanded="false"
      aria-label="Toggle navigation">
    <span className="navbar-toggler-icon"></span>
  </button>
  <div className="collapse navbar-collapse" id="navbarNavAltMarkup">
    <div className="navbar-nav">

      <NavLink to='/home' className="nav-item nav-link" href="#">
        Home <span className="sr-only">(current)</span>
      </NavLink>
      <NavLink to='/models' className="nav-item nav-link">
        Models
      </NavLink>
      <NavLink to='/anomalies' className="nav-item nav-link">
        Anomalies
      </NavLink>
      <NavLink to='/cases' className="nav-item nav-link">
        Cases
      </NavLink>
      <NavLink to='/settings' className="nav-item nav-link">
        Settings
      </NavLink>

    </div>
  </div>
</nav>
);

//
// const element = <TestProp name="dev" />;


/*
@name
@description global navigator
*/
const Navigation = () => (
  <Navbar/>
);



// export the navigation component
export default Navigation;
