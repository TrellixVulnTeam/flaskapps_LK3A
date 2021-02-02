'use strict';

/* Tables in the administration v6 */
angular.module('bombolone.directives.table', [])
.directive('tableAdmin', [
  "$rootScope", 
  function($rootScope) {
    return {
      restrict: "A",
      replace: true,
      scope: {
        "tableType": "@",
        "itemsList": "=tableList",
        "itemsFilter": "=itemsFilter",
        "remove": '=onRemove'
      },
      templateUrl: "/static/partial/table.html?" + new Date().getTime(),
      link: function(scope, element, attrs) {
        scope.admin = app.rank <= 20;

        scope.edit_url = "/admin/users/[[ item._id ]]/";

        /*
        Default values
        */
        var htmlTemplate, template;
        scope.show_url = true;
        scope.show_alias = false;

        /*
        Default table object
        */
        scope.table = {
          language_code: [],
          head: [],
          headWidth: [],
          sortBy: [],
          type: {
            hash_table: false,
            languages: false,
            ranks: false,
            users: false,
            items: true
          }
        };
        
        if (scope.tableType === "hash-table") {
          scope.table.type.hash_table = true;
          scope.table.type.items = false;
          if (app.rank < 15) {
            scope.table.admin = true;
            scope.table.headWidth = ["45", "35", "20"];
            scope.table.head = ["name", "number"];
            scope.table.sortBy = ["name", "number"];
          } else {
            scope.table.headWidth = ["55", "45"];
            scope.table.head = ["name", "number"];
            scope.table.sortBy = ["name", "number"];
          }

        } else if (scope.tableType === "languages") {
          scope.table.type.languages = true;
          scope.table.type.items = false;
          if (app.rank < 15) {
            scope.table.admin = true;
            scope.table.headWidth = ["5", "15", "35", "40"];
            scope.table.head = ["", "code", "language", "_id"];
            scope.table.sortBy = ["", "code", "language", "_id"];
          } else {
            scope.table.headWidth = ["15", "40", "40"];
            scope.table.head = ["code", "language", "_id"];
            scope.table.sortBy = ["code", "language", "_id"];
          }

        } else if (scope.tableType === "ranks") {
          scope.table.type.ranks = true;
          scope.table.type.items = false;
          scope.table.headWidth = ["60", "20", "20"];
          scope.table.head = ["Name", "Type permit", "Number user"];
          scope.table.sortBy = ["name", "rank", ""];

        } else if (scope.tableType === "users") {
          scope.table.type.users = true;
          scope.table.type.items = false;
          if (app.rank < 15) {
            scope.table.admin = true;
            scope.table.headWidth = ["4", "34", "42", "10"];
            scope.table.head = ["img", "username", "email", "created"];
            scope.table.sortBy = ["", "username", "email", "created"];
          } else {
            scope.table.headWidth = ["4", "76", "10"];
            scope.table.head = ["img", "username", "created"];
            scope.table.sortBy = ["", "username", "created"];
          }
          scope.sortTable = '-created';
        }

        scope.sort_by = function(index) {
          if (scope.sortTable == scope.table.sortBy[index]) {
            scope.sortTable = '-' + scope.table.sortBy[index];
          } else {
            scope.sortTable = scope.table.sortBy[index];
          }
          scope.table.active = index;
        };
      }
    }
  }
]);
