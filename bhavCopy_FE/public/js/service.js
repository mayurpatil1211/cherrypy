'use strict';

angular.module('app')

.factory('appService',['$http', '$timeout', function ($http,  $timeout) {
    var service = {};

    service.getStocks = function (callback) {

      $http.post('http://0.0.0.0:5000/')
      .success(function (response) {
        callback(response);
      })
      .error(function(response){
        console.log(response)
      });

    };

    service.saveData = function (callback) {

      $http.post('http://0.0.0.0:5000/insertData')
      .success(function (response) {
        callback(response);
      })
      .error(function(response){
        console.log(response)
      });

    };

    service.searchData = function (search_query, callback) {
      $http.post('http://0.0.0.0:5000/search/'+search_query)
      .success(function (response) {
        callback(response);
      })
      .error(function(response){
        console.log(response)
      });

    };

    return service;
  }]);

