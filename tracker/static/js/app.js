(function() {
	var app = angular.module('TrackerApp',['AuthDirectives','AuthService','ExpenseDirectives','ExpenseListDirectives','CommentDirectives']);
	
	app.controller('TrackerController',['$rootScope','UserService',function($rootScope,UserService){
			 // this.isLoggenIn = UserService.isLoggedIn;
			 $rootScope.userService = UserService;
		}]);



})();