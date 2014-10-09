(function(){
	var app = angular.module('CommentDirectives',['ui.bootstrap']);

	app.directive("expenseComments",function(){
			return{
				restrict: 'E',
				templateUrl: '/static/partials/expense-comments.html',
				controller: ['$http','$log',function($http,$log){
					this.comments= []
					this.displayComments = false;
					this.show_comments = function(expense){
						this.displayComments = true;
						var commentCtrl = this;
						$http.get('/api/v1/comments/'+expense.id).success(function(data){
							commentCtrl.comments = data;
						});
					};

					this.comment_text =''
					this.create = function(expense){
						var commentCtrl = this;
						var comment = {
							text 	   : commentCtrl.comment_text
						};

						$http.post('/api/v1/comment/'+expense.id,comment).success(function(data){
							$log.info('comment created');
							commentCtrl.comments.push(data);
							commentCtrl.comment_text = '';

						});
					}

				}],
				controllerAs:'commentCtrl'

			};
		});

	app.directive("createComment",function(){
		return {
			restrict: 'E',
			templateUrl: '/static/partials/create-comment.html',
			controller:['$http','$log',function($http,$log){

				// var commentCreateCtrl = this;
				// commentCreateCtrl.comment_text =''
				// this.create(expense) = function(expense){
				// 	var comment = {
				// 		expense_id : expense.id,
				// 		text 	   : commentCreateCtrl.comment_text
				// 	};

				// 	$http.post('/api/v1/comment',comment).success(function(data){
				// 		$log.info('comment created');
				// 	});

				// }
			}],
			controller: 'commentCreateCtrl'
		};
	})

})();