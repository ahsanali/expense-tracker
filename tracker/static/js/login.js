(function(){
	var app = angular.module('AuthDirectives',['ui.bootstrap']);

	app.directive("loginModal",[ '$modal', '$log',function($modal, $log){
			return{
				restrict: 'E',
				templateUrl: '/static/partials/login-modal.html',
				controller: function(){
					// $log('ads')
					var modalInstance = $modal.open({
					      templateUrl: 'myModalContent.html',
					      controller: 'loginController',
					      size: 'lg',
					      keyboard:false,
					      backdrop:'static',
					      controllerAs: 'loginCtrl'
					    });
				}
			};
		}]);


	angular.module('ui.bootstrap').controller('loginController', function ($scope,$rootScope, $modalInstance, $log, $http,UserService) {

		$scope.credentials = {};
		var modal =  $modalInstance;
		$scope.login = function(){
			$http.post('/api/v1/session',
				{
				 // 'email':$scope.credentials.email,
				 // 'password':$scope.credentials.password
				 'email':'sn.ahsanali1@gmail.com',
				 'password':'test'

				}
				).success(function(data){
					modal.close()
					UserService.isLoggedIn = true
					$rootScope.$broadcast('populateExpenses');
			});
		}

	  $scope.ok = function () {
	    $modalInstance.close();
	  };

	  $scope.cancel = function () {
	    $modalInstance.dismiss('cancel');
	  };
	});


})();