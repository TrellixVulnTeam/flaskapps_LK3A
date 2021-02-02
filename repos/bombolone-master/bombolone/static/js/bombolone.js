'use strict';


/* Bombolone v4 */
var d, host, path, protocol, qsa;
d = document;
qsa = d.querySelectorAll.bind(d);
protocol = window.location.protocol;
host = window.location.host;
path = window.location.pathname;

bombolone.config(function($interpolateProvider) {
  /* $interpolateProvider 
   * we need replace {{ }} with  [[ ]] */
  $interpolateProvider.startSymbol("[[");
  $interpolateProvider.endSymbol("]]");
});
