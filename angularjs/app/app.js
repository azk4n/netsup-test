'use strict';

angular.module('myApp', [
  'ngRoute',
  'myApp.pessoa'
]).
config(['$locationProvider', '$routeProvider', function($locationProvider, $routeProvider) {
  $locationProvider.hashPrefix('!');
  $routeProvider.otherwise({redirectTo: '/pessoa'});
}]);
