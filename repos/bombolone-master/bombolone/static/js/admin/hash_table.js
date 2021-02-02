'use strict';

/* Hash Table v6 */
angular.module('bombolone.controllers.hashTable', [])
.controller('HashTableCtrl', [
  "$scope", 
  "$resource", 
  "$rootScope", 
  "$location", 
  "api",
  function($scope, $resource, $rootScope, $location, api) {
    var counter, hash_table_index, hash_table_new, hash_table_overview, hash_table_update, 
    params, __get_value, _init_hash_table;

    $rootScope.admin_module = "hash_table";
    hash_table_overview = path.match(/^\/admin\/hash-table\/overview\/?$/i);
    hash_table_index = path.match(/^\/admin\/hash-table\/?$/i);
    hash_table_new = path.match(/^\/admin\/hash-table\/new\/?$/i);
    hash_table_update = path.match(/^\/admin\/hash-table\/update\/([^\/]+)\/?$/i);
    $scope.menu_language = false;
    $scope.show_hash_map_list = false;
    $scope.hash_map_id = "";
    $scope.hash_map = {
      name: "",
      value: {}
    };

    _init_hash_table = function() {
      $scope.hash_table = {
        language: $rootScope.language,
        lan: $rootScope.lan
      };
    };

    if (hash_table_index || hash_table_overview) {
      $rootScope.loader = true;
      api.hashTableList.get(params, function(resource) {
        $rootScope.loader = false;
        $rootScope.items_list = resource.hash_map_list;
        $scope.show_hash_map_list = true;
      });
    } else if (hash_table_new) {
      $scope.title = "New Hash Table";
      $scope.update = false;
      _init_hash_table();
    }
    
    if (hash_table_update) {
      $scope.title = "Update";
      $scope.update = true;
      _init_hash_table();
      $scope.hash_map_id = hash_table_update[1];
      params = {
        _id: $scope.hash_map_id
      };
      api.hashTableGet.get(params, function(resource) {
        var key, value, _ref, _results;
        $scope.hash_map = resource.hash_map;
        _ref = $scope.hash_map.value;
        _results = [];
        for (key in _ref) {
          value = _ref[key];
          _results.push($scope.hash_map.value[key]["key"] = key);
        }
        return _results;
      });
    }

    $scope.change_language = function(code, language) {
      $scope.hash_table.lan = code;
      $scope.hash_table.language = language;
      $scope.menu_language = false;
    };

    $scope.change_name_label = function(name_label) {
      $scope.name_label = name_label;
    };

    $scope.remove_label = function(key) {
      delete $scope.hash_map.value[key];
    };

    counter = 0;
    $scope.add_label = function() {
      var key, value;
      key = "aaa_key_" + counter;
      counter += 1;
      value = {
        key: ""
      };
      for (var i = 0; i < app.all_the_languages.length; i++) {
        value[app.all_the_languages[i][0]] = "";
      }
      $scope.hash_map.value[key] = value;
    };

    $scope.menu_reveal = function() {
      $scope.menu_language = !$scope.menu_language;
    };

    $scope["new"] = function() {
      var paramas;
      $rootScope.message_show = false;
      paramas = {
        "name": $scope.hash_map.name
      };
      paramas = __get_value(paramas);
      api.hashTableNew.post(paramas, function(resource) {
        $scope.show_message(resource);
      });
    };

    $scope.save = function() {
      var paramas;
      $rootScope.message_show = false;
      paramas = {
        "_id": $scope.hash_map_id,
        "name": $scope.hash_map.name
      };
      paramas = __get_value(paramas);
      api.hashTableUpdate.post(paramas, function(resource) {
        $scope.show_message(resource);
      });
    };

    __get_value = function(hash_map) {
      var code, key, value, _ref1;
      for (var i = 0; i < app.all_the_languages.length; i++) {
        code = app.all_the_languages[i][0];
        counter = 0;
        _ref1 = $scope.hash_map.value;
        for (key in _ref1) {
          value = _ref1[key];
          hash_map["label-name-" + counter] = value["key"];
          hash_map["label-" + code + "-" + counter] = value[code];
          counter += 1;
        }
        hash_map["len"] = counter;
      }
      return hash_map;
    };
  }
]);
