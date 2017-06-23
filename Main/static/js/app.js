'use strict';

/* App Module */

var phonecatApp = angular.module('PlagiarismDetection', [
  'ngRoute',
  'PlagiarismControllers'
]);

phonecatApp.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
      when('/', {
        templateUrl: 'partials/indexData.html',
        controller: 'IndexController'
      }).
      when('/aboutus', {
        templateUrl: 'partials/aboutus.html',
        controller: 'IndexController'
      }).
      otherwise({
        redirectTo: '/'
      });
  }]);