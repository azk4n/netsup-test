'use strict';

angular.module('myApp.pessoa', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/pessoa', {
    templateUrl: 'pessoa/pessoa.html',
    controller: 'PessoaCtrl'
  });
}])

.controller('PessoaCtrl', ['$scope', '$http', function($scope, $http) {
  $scope.showAlertError = false;
  $scope.showAlertModalError = false;
  $scope.showModal = false;
  $scope.pesquisa =  {
    "nome": "",
    "idade": "",
    "profissao": ""
  };
  $scope.pessoa =  {
    "id": "",
    "nome": ""
  };
  $scope.selectedPessoa = {
    "id": "",
    "nome": ""
  };
  //    Our GET request function
  $scope.getPessoa = function() {
    $http({
      method: "GET",
      url: "http://localhost:5000/pessoas/" + $scope.pessoa.id,
      headers: {"Authorization": "test"}
    }).then(
      function successCallback(response) {
        $scope.pessoa.nome = response.data.result.nome;
      },
      function errorCallback(err) {
        $scope.showAlertError = true;
        $scope.errorMsg = err.data.message;
      }
    );
  };
  $scope.search = function() {
    $http({
      method: "POST",
      data: {
        "nome": $scope.pesquisa.nome,
        "idade": $scope.pesquisa.idade,
        "profissao": $scope.pesquisa.profissao
      },
      url: "http://localhost:5000/pessoas",
      headers: {"Authorization": "test"}
    }).then(
      function successCallback(response) {
        $scope.pessoas = response.data.result;
      },
      function errorCallback(err) {
        $scope.showAlertModalError = true;
        $scope.errorMsg = err.data.message;
      }
    );
  };
  // executando search com parametros vazios
  // p/ preencher a lista inicialmente
  $scope.search();
  $scope.dblClickRowHandler = function(item) {
    $scope.pessoa.id = item.id;
    $scope.pessoa.nome = item.nome;
    $scope.selectedPessoa = {
      "id": "",
      "nome": ""
    };
    angular.element('#searchModal').trigger('click');
  };
  $scope.clickRowHandler = function(item) {
    $scope.selectedPessoa.id = item.id;
    $scope.selectedPessoa.nome = item.nome;
  };
  $scope.selectButtonHandler = function () {
    $scope.pessoa = $scope.selectedPessoa;
    $scope.selectedPessoa = {
      "id": "",
      "nome": ""
    };
    angular.element('#searchModal').trigger('click');
  };
}]);