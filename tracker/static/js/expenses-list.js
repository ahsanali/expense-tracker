(function(){
	var app = angular.module('ExpenseListDirectives',['ui.bootstrap','AuthService']);

	app.directive('expensesList',function(){
		return {
			restrict:'E',
			templateUrl:'/static/partials/expenses-list.html',
			controller: ['$http','$log',"$scope",'UserService',function($http,$log,$scope,UserService){
					var expenseList = this;
					expenseList.expenses = [];
					expenseList.searchWeek = 0;
					expenseList.search = {};
					expenseList.search_active = false;
					this.get_expenses = function(){
						if (expenseList.search_active){
							var search = {
								'min_date':(expenseList.search.min_date)?expenseList.search.min_date.valueOf():null,
								'max_date':(expenseList.search.max_date)?expenseList.search.max_date.valueOf():null,
								'min_amount':expenseList.search.min_amount,
								'max_amount':expenseList.search.max_amount,
							}
							$http.post('/api/v1/expenses/search/',search).success(function(data){
								expenseList.expenses = data.expenses;
								expenseList.total_amount = data.total_amount;
							})

						}
						else{
							$http.get('/api/v1/expenses/week/'+expenseList.searchWeek).success(function(data){
								expenseList.expenses = data.expenses;
								expenseList.total_amount = data.total_amount;

							})
						}

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