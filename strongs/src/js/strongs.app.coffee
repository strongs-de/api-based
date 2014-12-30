app = angular.module 'strongs.app', ['strongs.api', 'LocalStorageModule']

app.controller 'AppController', ['$scope', '$sce', 'BibleTranslation', 'BibleText', 'localStorageService', ($scope, $sce, BibleTranslation, BibleText, localStorageService) ->
    # initialization
    $scope.trSwitcherVisible = []

    # correct vers text
    correctverstext = (value) ->
        if not value?
            return ''
        s = value.replace("<STYLE css=", "<span style=")
        s = s.replace("</STYLE>", "</span>")

        # <note n='[3]'>In den</note>
        # ==> <sup><abbr rel='tooltip' title="In den">[3]</abbr></sup>
        s = s.replace('<ns0:catchWord>', '***')
        s = s.replace('</ns0:catchWord>', '+++')
        # Replace doubled hints
        s = s.replace(/<ns0:note xmlns:ns0=['"]http:\/\/www.bibletechnologies.net\/2003\/OSIS\/namespace['"] n=['"]\[([^'"]*)\]['"]>([^<]*)<\/ns0:note><ns0:note xmlns:ns0=['"]http:\/\/www.bibletechnologies.net\/2003\/OSIS\/namespace['"] n=['"]\[([^'"]*)\]['"]>([^<]*)<\/ns0:note>/g, "<sup class='small tooltip' title='$2'>$1</sup> ")
        # Replace single hints
        s = s.replace(/<ns0:note xmlns:ns0=['"]http:\/\/www.bibletechnologies.net\/2003\/OSIS\/namespace['"] n=['"]\[([^'"]*)\]['"]>([^<]*)<\/ns0:note>/g, "<sup class=\"small tooltip\" title='$2'>$1</sup> ")
        # Replace hint in zefania xml bibles
        s = s.replace('(?i)<div><note type=[\'"]x-studynote[\'"]>([^<]*)</note></div>', "<sup class='small tooltip' title='\\1'>Hinweis</sup>")
        s = s.replace('***', '<b>')
        s = s.replace('+++', '</b>')

        # s = s.replace("<gr str=", "<span class='sb-strong' onclick='' data-strong=")
        s = s.replace(/<gr str="([^"]*)"/g, "<span class='sb-strong strong-$1' onclick='' data-strong=\"$1\"")
        s = s.replace(/\s?<\/gr>/g, "</span> ")
        s = s.replace(' </span>,', '</span>,')
        s = s.replace(' </span>.', '</span>.')
        s = s.replace(' </span>!', '</span>!')
        s = s.replace(' </span>?', '</span>?')
        s = s.replace(' </span>:', '</span>:')
        s = s.replace(' </span>;', '</span>;')
        s = s.replace(' </span>]', '</span>]')
        s = s.replace('( ', '(')
        s = s.replace(' )', ')')
        s = s.replace(' </span>)', '</span>)')
        s = s.replace('\n', ' ')
        s = s.replace(',', ', ')
        s = s.replace('.', '. ')
        s = s.replace('!', '! ')
        s = s.replace('?', '? ')
        s = s.replace(':', ': ')
        return $sce.trustAsHtml(s)

    # translation switcher
    switchTranslation = (column, index) ->
        # store the selected index in localstorage and $scope
        $scope.translationIndices[column] = index
        localStorageService.set 'translation-index-' + column, index
        reloadTranslation(column)

    # reload translations
    reloadTranslation = (index) ->
        idx = index ? 0
        $scope.text[idx] = BibleText.query(tr_id: $scope.translations[$scope.translationIndices[idx]].identifier, bookNr: 44, chapterNr: 1)


        $scope.text[idx].$promise.then (results) ->
            angular.forEach results, (vers) ->
                # correct the vers text
                vers.versText = correctverstext vers.versText

        # should reload all translations?
        if not index?
            $scope.text[1] = BibleText.query(tr_id: $scope.translations[$scope.translationIndices[1]].identifier, bookNr: 44, chapterNr: 1)
            $scope.text[2] = BibleText.query(tr_id: $scope.translations[$scope.translationIndices[2]].identifier, bookNr: 44, chapterNr: 1)
            $scope.text[3] = BibleText.query(tr_id: $scope.translations[$scope.translationIndices[3]].identifier, bookNr: 44, chapterNr: 1)


            $scope.text[1].$promise.then (results) ->
                angular.forEach results, (vers) ->
                    # correct the vers text
                    vers.versText = correctverstext vers.versText


            $scope.text[2].$promise.then (results) ->
                angular.forEach results, (vers) ->
                    # correct the vers text
                    vers.versText = correctverstext vers.versText

            $scope.text[3].$promise.then (results) ->
                angular.forEach results, (vers) ->
                    # correct the vers text
                    vers.versText = correctverstext vers.versText

    initializeScope = () ->
        $scope.switchTranslation = switchTranslation

        # get translation indices
        $scope.translationIndices = []
        $scope.translationIndices[0] = localStorageService.get('translation-index-0') ? 0
        $scope.translationIndices[1] = localStorageService.get('translation-index-1') ? 1
        $scope.translationIndices[2] = localStorageService.get('translation-index-2') ? 2
        $scope.translationIndices[3] = localStorageService.get('translation-index-3') ? 3

        $scope.translations = BibleTranslation.query()
        $scope.search = {
            actPage: 1,
            totalPages: 10,
            text: 'Johannes 1'
        }

        $scope.text = []
        $scope.translations.$promise.then (results) ->
            reloadTranslation()

    initializeScope()
]
