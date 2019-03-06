describe('PessoaCtrl', function() {
  beforeEach(module('myApp.pessoa'));

  var $controller;
  const fakeItem = {
    "id": "1",
    "nome": "Alex"
  };

  beforeEach(inject(function(_$controller_){
    $controller = _$controller_;
  }));

  describe('test scope', function() {
      it('check scope', function() {
        var $scope = {};
        var controller = $controller('PessoaCtrl', { $scope: $scope });
        expect($scope.showAlertError).toEqual(false);
        expect($scope.showAlertError).toEqual(false);
        expect($scope.pessoa).toEqual({
          "id": "",
          "nome": ""
        });
        expect($scope.selectedPessoa).toEqual({
          "id": "",
          "nome": ""
        });
      });
  });
  describe('test handlers', function() {
    it('seleciona pessoa definitiva no handler de doubleclick da row', function() {
      var $scope = {};
      var controller = $controller('PessoaCtrl', { $scope: $scope });
      $scope.dblClickRowHandler(fakeItem);
      expect($scope.pessoa.id).toEqual('1');
      expect($scope.pessoa.nome).toEqual('Alex');
    });
    it('seleciona pessoa no handler de click da row', function() {
      var $scope = {};
      var controller = $controller('PessoaCtrl', { $scope: $scope });

      $scope.clickRowHandler(fakeItem);
      expect($scope.selectedPessoa.id).toEqual('1');
      expect($scope.selectedPessoa.nome).toEqual('Alex');
    });
    it('seleciona pessoa definitiva no handle de click do botao "listar"', function() {
      var $scope = {};
      var controller = $controller('PessoaCtrl', { $scope: $scope });
      $scope.clickRowHandler(fakeItem);
      $scope.selectButtonHandler(fakeItem);
      expect($scope.selectedPessoa.id).toEqual('');
      expect($scope.selectedPessoa.nome).toEqual('');
      expect($scope.pessoa.id).toEqual('1');
      expect($scope.pessoa.nome).toEqual('Alex');
    });
  });
});