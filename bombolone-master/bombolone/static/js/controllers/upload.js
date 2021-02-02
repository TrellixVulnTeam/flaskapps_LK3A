'use strict';

/* Upload v4 */
angular.module('bombolone.controllers.upload', [])
.controller('UploadCtrl', [
  "$scope", 
  "$resource", 
  "$rootScope",
    function($scope, $resource, $rootScope) {
      var match_settings, match_users, up, __abort_upload, __format_size, __init_upload, __load_file, __show_message_error, __start_upload, __upload_supported;
      $scope.upload_allowed = true;
      match_users = path.match(/^\/admin\/users\/([^\/]+)\/?$/i);
      match_settings = path.match(/^\/settings\/profile\/?$/i);
      if (match_users || match_settings) {
        up = {
          multiple: false,
          module: 'avatars',
          action: $rootScope.API + "/account/upload_avatar.json",
          recipe: false
        };
      }
      $scope.setFile = function(element) {
        return $scope.$apply(function($scope) {
          $scope.files = element.files;
          return __init_upload();
        });
      };
      $scope.file = [];
      $scope.number_upload = 0;
      __upload_supported = function() {
        var input;
        input = d.createElement("input");
        input.type = "file";
        return "multiple" in input && typeof File !== "undefined" && typeof (new XMLHttpRequest()).upload !== "undefined";
      };
      if (__upload_supported() === false) {
        $scope.upload_allowed = false;
        alert("I'm sorry but your browser is old!      \nIt's not possible upload images by Ajax, please use one of the version is green in this page http://caniuse.com/xhr2");
      }
      __init_upload = function() {
        var file_data, files_list, index, item, position, _i, _ref, _results;
        console.log("Files ===> ", $scope.files);
        files_list = $scope.files;
        _results = [];
        for (index = _i = 0, _ref = files_list.length; 0 <= _ref ? _i < _ref : _i > _ref; index = 0 <= _ref ? ++_i : --_i) {
          item = files_list[index];
          if (!up.multiple && $scope.number_upload) {
            _results.push(__show_message_error("Attento stai gia caricando un altro file"));
          } else {
            file_data = {
              "index": index,
              "progress": 0,
              "file": item,
              "size": item.fileSize != null ? item.fileSize : item.size,
              "name": item.fileName != null ? item.fileName : item.name
            };
            if (file_data.file_size > 16000000) {
              _results.push(__show_message_error("Attento il file è più grande di 16Mb"));
            } else {
              $scope.file.push(file_data);
              position = $scope.file.length;
              $scope.number_upload += 1;
              _results.push(__load_file($scope.file[position - 1]));
            }
          }
        }
        return _results;
      };
      $scope.stop_upload = function(index) {
        var item, _results;
        if (index) {
          $scope.file[index].xhr.abort();
          return $scope.file[index].xhr = null;
        } else {
          _results = [];
          for (item in $scope.file[index]) {
            _results.push(__abort_upload(item));
          }
          return _results;
        }
      };
      __abort_upload = function(upload) {
        var item;
        if ((upload != null) === false) {
          item.abort();
          return item = null;
        }
      };
      __load_file = function(upload) {
        upload.xhr = new XMLHttpRequest();
        upload.text = upload.name + "  " + __format_size(upload.size);
        upload.info_show = true;
        if (up.recipe) {
          $scope.$parent.recipe.images.push(upload);
          upload.len = $scope.$parent.recipe.images.length - 1;
          upload.show = "/static/default/recipe.jpg";
          upload.description = {
            it: "",
            en: ""
          };
          upload = $scope.$parent.recipe.images[upload.len];
        }
        return __start_upload(upload);
      };
      __start_upload = function(file) {
        file.xhr.upload.onprogress = (function(file) {
          return function(e) {
            return $scope.$apply(function() {
              var percentCompleted;
              percentCompleted = Math.round(e.loaded / e.total * 100);
              if (percentCompleted < 1) {
                file.progress_value = "Uploading...";
              } else if (percentCompleted === 100) {
                file.progress_value = "Saving...";
              } else {
                file.progress_value = percentCompleted + "%";
              }
              return file.progress = percentCompleted + "%";
            });
          };
        })(file);
        file.xhr.onload = (function(file, index) {
          return function(e) {
            return $scope.$apply(function() {
              var data, image;
              file.progress_value = "Uploaded!";
              data = JSON.parse(e.target.responseText);
              if (data.success) {
                image = data.message;
                if (up.recipe) {
                  file.progress_value = "Completato  " + __format_size(file.size);
                  $scope.$parent.recipe.images[file.len].uploaded = image;
                  $scope.$parent.recipe.images[file.len].show = "/static/" + up.module + "/tmp/" + image;
                  $scope.number_upload -= 1;
                } else {
                  file.progress_value = "Completato  " + __format_size(file.size);
                  $scope.$parent.user.image_uploaded = image;
                  $scope.$parent.user.image_show = "/static/" + up.module + "/tmp/" + image;
                  $scope.number_upload -= 1;
                }
                return file.info_show = false;
              } else {
                console.log("loose");
                return __upload_failed(evt);
              }
            });
          };
        })(file, file.index);
        file.xhr.open("POST", up.action, true);
        file.xhr.setRequestHeader("X-User-Id", app["user_id"]);
        file.xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
        file.xhr.setRequestHeader("X-File-Name", file.name);
        file.xhr.setRequestHeader("Content-Type", "application/octet-stream");
        return file.xhr.send(file.file);
      };

      $scope.remove_image = function(index, callback) {
        if (up.recipe) {
          $scope.$parent.recipe.images.splice(index, 1);
          callback(index);
        }
      };

      __format_size = function(bytes) {
        var i;
        i = -1;
        while (true) {
          bytes = bytes / 1024;
          i++;
          if (!(bytes > 99)) {
            break;
          }
        }
        return Math.max(bytes, 0.1).toFixed(1) + ["kB", "MB", "GB", "TB", "PB", "EB"][i];
      };

      __show_message_error = function(message) {
        console.log(message);
        return false;
      };
    }
  ]
);
