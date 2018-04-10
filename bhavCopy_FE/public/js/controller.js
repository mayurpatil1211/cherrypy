"use strict";

angular.module("app").controller("appCtrl", ["$scope", "appService", function ($scope, appService) {

		$scope.result_success = false
		function savingData(){
			appService.saveData(function(response){
			if(response.status==200){
				$scope.heading = "Top Ten Stock Entries"
				$scope.note = response["message"]
				appService.getStocks(function(response){
					$scope.result_success = true
					$scope.topTen = response["topTen"]

			});
			}else{
				$scope.result_success = true
				$scope.topTen = []
			}
			});
		}
		savingData();


		$scope.searchCompany = function(){
			$scope.heading = "Search Results"
			$scope.result_success = false
			appService.searchData($scope.search_query ,function(response){
				if(response.status==200){
					if(response.message.length>0){
						$scope.result_success = true
						$scope.topTen = response.message
						$scope.notFound = ""
					}else{
						$scope.result_success = true
						$scope.notFoundStatus = true
						$scope.topTen = []
						$scope.notFound = "Sorry, Not Found"
					}
				}else{
					$scope.notFoundStatus = true
					$scope.topTen = []
					$scope.notFound = "Sorry, Not Found"
				}
			});
		}

	}]);