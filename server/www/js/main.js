	var helloApp = angular.module("helloApp", ['colorpicker.module', 'rzModule']);
  helloApp.controller("HelloCtrl", function($scope, $http) {
    $scope.actions = ['rainbow', 'volumeBar', 'off'];
    
    $scope.max_intensity = 100;
    $scope.min_intensity = 0;
    $scope.colors = [];
    $scope.intensities = [];
    
    $scope.selected = function(ev, value) {
      rgb = value.value.match(/\d+/g);
      color = {};
      color.r = rgb[0];
      color.g = rgb[1];
      color.b = rgb[2];
      id=-1;
      $http.get('/animation.json?name=color&id='+id+'&r='+color.r+'&g='+color.g+'&b='+color.b).then(response => {
      },
      function errorCallback(response) {
        console.log(response);
      }); 
    };
    
    $scope.set_intensity = function() {
      $http.get('/intensity.json?max='+$scope.max_intensity+'&min='+$scope.min_intensity).then(response => {
      },
      function errorCallback(response) {
        console.log(response);
      }); 
    }
    
    $scope.animation = function(id,_animation) {
      $http.get('/animation.json?name='+_animation+'&id='+id).then(response => {
      },
      function errorCallback(response) {
        console.log(response);
      }); 
    }
    
    $scope.next = function() {
      $http.get('/animation.json?name=next&id=-1').then(response => {
      },
      function errorCallback(response) {
        console.log(response);
      }); 
    }
    
    //Slider config with callbacks
    $scope.slider_callbacks = {
      onStart: function () {
//           $scope.otherData.start = $scope.slider_callbacks.value * 10;
      },
      onChange: function () {
        $scope.set_intensity();
      },
      onEnd: function () {
//           $scope.otherData.end = $scope.slider_callbacks.value * 10;
      }
    };
    
    
    $scope.refresh = function() {
      self.refresh_timeout_ms = 1000;
      // fetch status
      $http.get('/status.json').then(response => {
        $scope.status = response.data;
        $scope.max_intensity = $scope.status.max_intensity*100;
        setTimeout($scope.refresh, refresh_timeout_ms);
      },function errorCallback(response) {setTimeout($scope.refresh, refresh_timeout_ms);});
    }
    
    $scope.$on('colorpicker-selected', $scope.selected)
    $scope.refresh();
  }); 
