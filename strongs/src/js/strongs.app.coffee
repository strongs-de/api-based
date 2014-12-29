app = angular.module 'strongs.app', ['strongs.api']

app.controller 'AppController', ['$scope', '$sce', 'BibleTranslation', 'BibleText', ($scope, $sce, BibleTranslation, BibleText) ->
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

    $scope.translations = BibleTranslation.query()
    $scope.search = {
        actPage: 1,
        totalPages: 10,
        text: 'Johannes 1'
    }

    $scope.text = []
    $scope.text[0] = BibleText.query(tr_id: 'ELB1905STR', bookNr: 44, chapterNr: 1)
    $scope.text[1] = BibleText.query(tr_id: 'SCH2000', bookNr: 44, chapterNr: 1)
    $scope.text[2] = BibleText.query(tr_id: 'LUTH1912', bookNr: 44, chapterNr: 1)
    $scope.text[3] = BibleText.query(tr_id: 'NGU', bookNr: 44, chapterNr: 1)

    $scope.text[0].$promise.then (results) ->
        angular.forEach results, (vers) ->
            # correct the vers text
            vers.versText = correctverstext vers.versText


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
]
