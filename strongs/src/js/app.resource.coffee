app = angular.module 'strongs.app.resource', ['strongs.api']

app.controller 'AppController', ['$scope', 'Post', ($scope, Post) ->
    $scope.posts = Post.query()
]
