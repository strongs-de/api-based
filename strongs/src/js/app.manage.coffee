app = angular.module 'strongs.app.manage', ['strongs.api', 'strongs.app.editor']

app.controller 'DeleteController', ['$scope', 'AuthUser', ($scope, AuthUser) ->
    $scope.canDelete = (post) ->
        return post.author.username == AuthUser.username

    $scope.delete = (post) ->
        post.$delete()
        .then ->
            # Remove it from the list on success
            idx = $scope.posts.indexOf(post)
            $scope.posts.splice(idx, 1)
]
