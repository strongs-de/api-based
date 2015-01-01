filters = angular.module 'strongs.filters', []

filters.filter 'correctverstext', ['$sce', ($sce) ->
    return (text) ->
        if not text?
            return ''
        s = '' + text
        s = s.replace("<STYLE css=", "<span style=")
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
        #return s
]