(function(){
	var app = angular.module('ExpenseListDirectives',['ui.bootstrap','AuthService']);

	app.directive('expensesList',function(){
		return {
			restrict:'E',
			templateUrl:'/static/partials/expenses-list.html',
			controller: ['$http','$log',"$scope",'UserService',function($http,$log,$scope,UserService){
					var expenseList = this;
					expenseList.expenses = []
					expenseList.searchWeek = 0
					this.get_expenses = function(){
						$http.get('/api/v1/expenses/week/'+expenseList.searchWeek).success(function(data){
							expenseList.expenses = data.expenses;
							expenseList.total_amount = data.total_amount;

						})

					}
					if (UserService.isLoggedIn){
						this.get_expenses();
					}

					$scope.$on('populateExpenses', function(event, args) {
						expenseList.get_expenses();
					});
			}],
			controllerAs:'expenseListCtrl'
		}
	});
	
})();