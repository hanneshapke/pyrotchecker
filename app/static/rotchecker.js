angular.module('rotApp', [])

  .factory('APIService', function( $http ) {
    return {
      checkWebsite: function(shift, url, keywords, tag) {
        return $http.get('/api/' + shift + '?url=' + url + '&q=' + keywords + '&t=' + tag, {cache: false}).then(function(result) {
          return result.data;
        });
      }
    }
  })

  .controller('ROTCheckerController', function(APIService) {

    var rotChecker = this;
    rotChecker.status_msg = '';
    rotChecker.status = '';

    rotChecker.checkWebsite = function() {
      // rotChecker.rotShift = rotChecker.rotShiftInt;
      APIService.checkWebsite(
          rotChecker.rotShiftInt,
          rotChecker.urlText,
          rotChecker.keywordText,
          rotChecker.tagText
        ).then(function(data) {
        rotChecker.status_msg = data['message'];
        rotChecker.status = data['status'];
        console.log(data);
      });
    };

  });