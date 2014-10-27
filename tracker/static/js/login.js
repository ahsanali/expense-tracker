(function(){
	var app = angular.module('AuthDirectives',['ui.bootstrap']);

	app.directive("loginModal",['$rootScope','$http', '$modal', '$log','UserService',function($rootScope,$http,$modal, $log,UserService){
			return{
				restrict: 'E',
				templateUrl: '/static/partials/login-modal.html',
				controller: function(){

					
					$http.get('/api/v1/session').success(function(data){
							UserService.isLoggedIn = true;
							$rootScope.$broadcast('populateExpenses');
						}).
					error(function(data){
						var modalInstance = $modal.open({
					      templateUrl: 'myModalContent.html',
					      controller: 'loginController',
					      size: 'lg',
					      keyboard:false,
					      backdrop:'static',
					      controllerAs: 'loginCtrl'
					    });
					});
				}
			};
		}]);


	angular.module('ui.bootstrap').controller('loginController', function ($scope,$rootScope, $modalInstance, $log, $http,UserService) {

		$scope.credentials = {};
		$scope.login_panel = true;
		$scope.new_user = {}
		var modal =  $modalInstance;



		$scope.create_account = function(){
			 var user = {};
			 user.name = $scope.new_user.name;
			 user.email = $scope.new_user.email;
			 user.sex_code = $scope.new_user.sex;
			 user.password = $scope.new_user.password;

			 $http.post('/api/v1/user',user).success(function(data){
					UserService.isLoggedIn = true;
					$rootScope.$broadcast('populateExpenses');
					modal.close();
			 })

		};

		$scope.login = function(){
			$http.post('/api/v1/session',
				{
				 'email':$scope.credentials.email,
				 'password':$scope.credentials.password
				}
				).success(function(data){
					modal.close();
					UserService.isLoggedIn = true;
					$rootScope.$broadcast('populateExpenses');
			});
		};

		$scope.password_donot_match = function(){
			return $scope.new_user.confirm_password != $scope.new_user.password;
		}

	//   $scope.ok = function () {
	//     $modalInstance.close();
	//   };

	//   $scope.cancel = function () {
	//     $modalInstance.dismiss('cancel');
	//   };
	});


})();