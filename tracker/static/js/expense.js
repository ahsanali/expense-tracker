(function(){
	var app = angular.module('ExpenseDirectives',['ui.bootstrap']);

	app.directive("expenseCreation",function(){
			return{
				restrict: 'E',
				templateUrl: '/static/partials/expense-creation.html',
				controller: ['$scope','$log','$http',function($scope,$log,$http){

									$scope.expense = {};

									$scope.create = function(){
										var expense = {};
										expense.amount = $scope.expense.amount;
										expense.description = $scope.expense.description;
										expense.expense_time = $scope.expense.date;
										expense.expense_time.setHours($scope.tm.getHours());
										expense.expense_time.setMinutes($scope.tm.getMinutes());
										expense.expense_time = expense.expense_time.valueOf() ;
										// expense.expense_time = expense.expense_time.toISOString();

										$http.post('/api/v1/expense',expense).success(
											function(data){
												$log.info('expense created');
												$scope.$emit('populateExpenses');
											})
									}

									//Date Picker Controls
									  $scope.open = function($event) {
									    $event.preventDefault();
									    $event.stopPropagation();

									    $scope.opened = true;
									  };

									// Time Picker Controls
									$scope.tm = new Date();
									$scope.hstep = 1;
									$scope.mstep = 15;
									$scope.ismeridian = true;

								}],
				controllerAs: 'expenseCreateCtrl'
			};
		});

	app.directive("editExpense",function(){
		return{
			restrict: 'E',
			templateUrl: '/static/partials/edit-expense.html',
			controller: ['$http','$log','$scope','$modal',function($http,$log,$scope,$modal){
				this.expense = {};
				this.opened = false;
				var edit_expense = this;
				this.edit_expense = function(expense){

					edit_expense.expense = expense;
					var modalInstance = $modal.open({
					      templateUrl: 'editExpense.html',
					      controller: 'editExpenseModalCtrl',
					      size: 'lg',
					      controllerAs: 'editExpenseModalCtrl',
					      resolve: {
					        selected_expense: function () {
					          return edit_expense.expense;
					        }
					      }
					    });


					modalInstance.result.then(function (selectedItem) {
				      this.opened = false;
				      this.expense = {};
				      $scope.$emit('populateExpenses');
				    }, function () {
				      this.opened = false;
				      this.expense = {};
				      $scope.$emit('populateExpenses');
				    });
					}

			}],
			controllerAs:'editExpenseCtrl'
		}
	});


	angular.module('ui.bootstrap').controller('editExpenseModalCtrl', function ($scope,$http, $modalInstance, $log, selected_expense) {
		$scope.selected_expense = selected_expense;
		$scope.selected_expense.dt = new Date(selected_expense.expense_time);
		$scope.selected_expense.tm = new Date(selected_expense.expense_time);
		
		//Time Picker
		$scope.hstep = 1;
		$scope.mstep = 15;
		$scope.ismeridian = true;

		var modal =  $modalInstance;
		$scope.edit = function(){
			var expense = {};
			expense.amount = $scope.selected_expense.amount;
			expense.description = $scope.selected_expense.description;
			expense.expense_time = $scope.selected_expense.dt;
			expense.expense_time.setHours($scope.selected_expense.tm.getHours());
			expense.expense_time.setMinutes($scope.selected_expense.tm.getMinutes());
			expense.expense_time = expense.expense_time.valueOf() ;
			$scope.selected_expense.expense_time = expense.expense_time ;
			// expense.expense_time = expense.expense_time.toISOString();

			$http.put('/api/v1/expense/'+$scope.selected_expense.id,expense).success(
				function(data){
					$log.info('expense editted');
					modal.close();
				})



		}

	  $scope.ok = function () {
	    $modalInstance.close();
	  };

	  $scope.cancel = function () {
	    $modalInstance.dismiss('cancel');
	  };
	});

})();