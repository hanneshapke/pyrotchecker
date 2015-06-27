angular.module('rotApp', [])

  .controller('ROTCheckerController', function() {
    
    var rotChecker = this;
    rotChecker.url = '';
    rotChecker.rotShift = 13;
    rotChecker.keyword = '';
    rotChecker.status = '';

    rotChecker.checkWebsite = function() {
      rotChecker.url = rotChecker.urlText;
      rotChecker.rotShift = rotChecker.rotShiftInt;
      rotChecker.keyword = rotChecker.keywordText;
      rotChecker.status = 'alert alert-danger';
      rotChecker.status_msg = '[Invalid url] Found keyword %%%'
    };

  });