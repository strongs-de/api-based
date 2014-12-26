app = angular.module 'strongs.app.translations', ['strongs.api']

app.controller 'AppController', ['$scope', 'BibleTranslation', ($scope, BibleTranslation) ->
    $scope.translations = BibleTranslation.query()
]
