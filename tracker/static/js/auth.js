(function(){
	var app= angular.module('AuthService',[]);
	app.factory('UserService', [function() {
		var sdo = {
			isLoggedIn: false,
			username: ''
		};
		return sdo;
	}]);
})();