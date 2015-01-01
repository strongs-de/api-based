app = angular.module 'strongs.app', ['strongs.api', 'strongs.filters', 'LocalStorageModule', 'ngRoute']

# controllers
app.controller 'MainController', ['$scope', 'BibleTranslation', 'BibleText', 'localStorageService', ($scope, BibleTranslation, BibleText, localStorageService) ->
    # initialization
    $scope.trSwitcherVisible = []

    # translation switcher
    switchTranslation = (column, index) ->
        # store the selected index in localstorage and $scope
        $scope.translationIndices[column] = index
        localStorageService.set 'translation-index-' + column, index
        reloadTranslation(column)

    # reload translations
    reloadBibleText = (index) ->
        # should reload all translations?
        if not index?
            $scope.text = (BibleText.query(tr_id: $scope.translations[$scope.translationIndices[num]].identifier, bookNr: 44, chapterNr: 1) for num in [0, 1, 2, 3])
        else
            $scope.text[index] = BibleText.query(tr_id: $scope.translations[$scope.translationIndices[index]].identifier, bookNr: 44, chapterNr: 1)

    initializeScope = () ->
        # function scoping
        $scope.switchTranslation = switchTranslation

        # get translation indices from the local storage
        $scope.translationIndices = (localStorageService.get('translation-index-' + idx) ? idx for idx in [0, 1, 2, 3])

        # load the available translations
        $scope.translations = BibleTranslation.query()

        # load bible text after translations are loaded successful
        $scope.translations.$promise.then (results) ->
            reloadBibleText()

        # example for search object
        $scope.search = {
            actPage: 1,
            totalPages: 10,
            text: 'Johannes 1'
        }

    initializeScope()
]

# configuration
app.config ($routeProvider) ->
    $routeProvider.when("/",
        templateUrl: "index.html", controller: 'MainController'
    ).when("/about",
        template: "Über Strongs.de"
    ).otherwise redirectTo: "/"