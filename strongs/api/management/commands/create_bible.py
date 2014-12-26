# -*- coding: utf8 -*-
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from strongs.api.models import BibleTranslation, BibleBook, BibleVers, BibleText, StrongNr
from os import path
from xml.etree import ElementTree as ElementTree
import re
import string


class Command(BaseCommand):
    args = '<bible_name> <identifier> <lang> <title> <needs_chapter> <osis>'
    help =  '''
                Initializes the database with the given bible found in the bibles directory.
                You have to specify a Zefanja or OSIS XML file name to a file in the bibles directory.
            '''
    option_list = BaseCommand.option_list + (
        make_option('--osis',
            action='store_true',
            dest='osis',
            default=False,
            help='Given file name is an osis xml file.'),
        ) + (
        make_option('--needs_chapter',
            action='store_true',
            dest='needs_chapter',
            default=False,
            help='If we need to parse the chapter tags.'),
        )


    def add_arguments(self, parser):
        parser.add_argument('bible_name', nargs=1, type=str)
        parser.add_argument('identifier', nargs=1, type=str)
        parser.add_argument('lang', nargs=1, type=str)
        parser.add_argument('title', nargs=1, type=str)


    def handle(self, *args, **options):
        # try:
        if options['osis']:
            if len(args) >= 4:
                # insert osis bible
                self.insert_osis_bible(args[0], args[1], args[2], args[3], options['needs_chapter'])
            else:
                raise CommandError('You must specify 4 arguments if you want to insert an OSIS XML bible.')
        else:
            if len(args) >= 1:
                # insert zefanja bible
                self.insert_zefanja_bible(args[0])
            else:
                raise CommandError('You must specify 1 arguments if you want to insert an OSIS XML bible.')
        # except:
        #     raise CommandError('XML file for bible "%s" does not exist' % args[0])

        # self.init_bible_books()
        # if path.exists('bibles/osis.NGU.xml'):
        #   self.insert_osis_bibles()
        # self.insert_bible_vers()
        # self.init_strong_grammar()


    def element_to_string(self, element, until_child_is=None):
        s = element.text or ""
        for sub_element in element:
            if until_child_is != None and sub_element.tag in until_child_is:
                break
            s += ElementTree.tostring(sub_element)
        s += element.tail
        return s

    def insert_osis_bible(self, path, identifier, lang, title, needs_chapter):
        self.stdout.write('Start parsing ' + identifier + ' ...')

        BOOKS = ['Gen', 'Exod', 'Lev', 'Num', 'Deut', 'Josh', 'Judg', 'Ruth', '1Sam', '2Sam', '1Kgs', '2Kgs', '1Chr', '2Chr', 'Ezra', 'Neh', 'Esth', 'Job', 'Ps', 'Prov', 'Eccl', 'Song', 'Isa', 'Jer', 'Lam', 'Ezek', 'Dan', 'Hos', 'Joel', 'Amos', 'Obad', 'Jonah', 'Mic', 'Nah', 'Hab', 'Zeph', 'Hag', 'Zech', 'Mal', 'Matt', 'Mark', 'Luke', 'John', 'Acts', 'Rom', '1Cor', '2Cor', 'Gal', 'Eph', 'Phil', 'Col', '1Thess', '2Thess', '1Tim', '2Tim', 'Titus', 'Phlm', 'Heb', 'Jas', '1Pet', '2Pet', '1John', '2John', '3John', 'Jude', 'Rev']

        tree = ElementTree.parse(path)
        root = tree.getroot()
        # work = root.find('{http://www.bibletechnologies.net/2003/OSIS/namespace}osisText/{http://www.bibletechnologies.net/2003/OSIS/namespace}header/{http://www.bibletechnologies.net/2003/OSIS/namespace}work')
        if title is not None and path is not None and identifier is not None and lang is not None:
            # Ask if this translation does already exist
            tr = BibleTranslation.objects.filter(identifier=identifier)
            if tr.count() <= 0:
                tr = BibleTranslation(identifier=identifier, name=title, language=lang)
                tr.save()
                self.stdout.write(' -> created new translation ' + identifier + '.')
            else:
                tr = tr[0]

            # iterate over all verses
            if needs_chapter:
                chapters = root.findall('.//{http://www.bibletechnologies.net/2003/OSIS/namespace}chapter')
            else:
                chapters = root.getchildren()
            actbook = ''
            actchapter = 0
            tb = None
            for chapter in chapters:
                versesinchapter = chapter.findall('.//{http://www.bibletechnologies.net/2003/OSIS/namespace}verse')
                for vers in versesinchapter:
                    parts = vers.attrib.get('osisID').split('.')
                    bookname = parts[0]
                    cnumber = int(parts[1])
                    vnumber = int(parts[2])
                    text = self.element_to_string(vers)

                    if bookname != actbook:
                        # Does this book already exist?
                        bindex = BOOKS.index(bookname)
                        tb = BibleBook.objects.filter(nr=bindex+1)
                        if tb.count() <= 0:
                            tb = BibleBook(nr=bindex+1, name='', alternativeNames='')
                            tb.save()
                        else:
                            tb = tb[0]

                    # check for existance of the first vers in this chapter,
                    # cause in Schlachter 2000 the first vers isn't encapsulated
                    # in a verse-tag!
                    if cnumber != actchapter:
                        if vnumber > 1:
                            # The first verse can be found in the parent chapter tag-text
                            # __insert(tr, tb, cnumber, 1, chapter.text)
                            self.__insert(tr, tb, cnumber, 1, self.element_to_string(chapter, ['{http://www.bibletechnologies.net/2003/OSIS/namespace}div', '{http://www.bibletechnologies.net/2003/OSIS/namespace}verse']))
                        actchapter = cnumber

                    self.__insert(tr, tb, cnumber, vnumber, text)
                    # s += bookname + str(cnumber) + ',' + str(vnumber) + ': ' + text
                    # break


    def __insert(self, translation, book, chapter, vers, text):
        '''
            Insert the bible text into the database. Create the BibleVers
            and the BibleText if it does not exist.
                @translation is a BibleTranslation instance
                @book is a BibleBook instance
                @chapter and @vers are integers
                @text is a string
        '''


        # vnumber can contain multiple verses. In NGUE it is seperated by a 8209 (e.g. 16-17 is defined
        # as 16820917. So we have to check if this is the case, then separate the verse numbers, insert the
        # first one and every following as an empty verse.
        numverses = 1
        if str(vers).__contains__('8209'):
            vers, lastvers = int(str(vers).split('8209')[0]), int(str(vers).split('8209')[1])
            numverses = lastvers - vers + 1

        # Does this vers already exist?
        v = BibleVers.objects.filter(bookNr=book, chapterNr=chapter, versNr=vers)
        if v.count() <= 0:
            v = BibleVers(bookNr=book, chapterNr=chapter, versNr=vers)
            v.save()
        else:
            v = v[0]

        # Insert text if it does not already exist
        t = BibleText.objects.filter(vers=v, translationIdentifier=translation)
        if t.count() <= 0:
            t = BibleText(vers=v, translationIdentifier=translation, versText=text)
            t.save()

            if numverses > 1:
                for i in range(1, numverses):
                    self.__insert(translation, book, chapter, vers+i, '')


    def insert_zefanja_bible(self, path):
        self.stdout.write('Start parsing ...')

        ####################################################
        # Insert bibles from zefanja xml
        baum = ElementTree.parse(path)
        root = baum.getroot()
        identifier = root.findtext('INFORMATION/identifier')
        language = root.findtext('INFORMATION/language')
        title = root.findtext('INFORMATION/title')

        self.stdout.write(identifier + ':')

        # Ask if this translation does already exist
        tr = BibleTranslation.objects.filter(identifier=identifier)
        # self.stdout.write('1')
        if tr.count() <= 0:
            # self.stdout.write('2')
            tr = BibleTranslation(identifier=identifier, name=title, language=language)
            # self.stdout.write('3')
            tr.save()
            # self.stdout.write('4')
            self.stdout.write(' -> created new translation ' + identifier + '.')
            # self.stdout.write('5')
        else:
            # self.stdout.write('-2')
            tr = tr[0]
        # self.stdout.write('6')

        # Insert verses
        for book in root.findall('BIBLEBOOK'):
            # self.stdout.write('a')
            chapterCount = 0

            # Does this book already exist
            # self.stdout.write('b')
            tb = BibleBook.objects.filter(nr=book.get('bnumber'))
            # self.stdout.write('c')
            if tb.count() <= 0:
                # self.stdout.write('d')
                tb = BibleBook(nr=int(book.get('bnumber')), name='', alternativeNames='')
                # self.stdout.write('e')
                tb.save()
            else:
                # self.stdout.write('-d')
                tb = tb[0]
            # self.stdout.write('f')

            versCount = 0
            # self.stdout.write('g')
            for chapter in book.findall('CHAPTER'):
                chapterCount += 1
                for vers in chapter.findall("VERS"):
                    versCount += 1

                    # Does this vers and chapter already exist?
                    v = BibleVers.objects.filter(bookNr=tb, chapterNr=chapter.get('cnumber'), versNr=vers.get('vnumber'))
                    if v.count() <= 0:
                        v = BibleVers(bookNr=tb, chapterNr=chapter.get('cnumber'), versNr=vers.get('vnumber'))
                        v.save()
                    else:
                        v = v[0]

                    # Insert text if it does not already exist
                    dbVers = BibleText.objects.filter(translationIdentifier=tr, vers=v)
                    if dbVers.count() <= 0:
                        dbVers = BibleText(translationIdentifier=tr, vers=v, versText=self.element_to_string(vers))
                        dbVers.save()
            self.stdout.write(' -> inserted book nr ' + book.get('bnumber') + ' with ' + str(chapterCount)  + ' chapters and ' + str(versCount) + ' verses.')
        self.stdout.write('done parsing!')


    def init_strong_grammar(self):
        greekStrongVerses = BibleText.objects.filter(versText__icontains='<gr rmac=', translationIdentifier=BibleTranslation.objects.filter(identifier='GNTTR'))
        s = 'initStrongGrammar: ' + str(greekStrongVerses.count()) + ' verses found!'
        sgreek = ElementTree.parse("./strongsgreek.xml").getroot()
        entries = sgreek.findall(".//entries/entry")
        for vers in greekStrongVerses:
            # get the vers in another translation
            # trWord = BibleTranslation.objects.filter(identifier='ELB1905STR')
            # trVers = BibleVers.objects.filter(versNr=vers.versNr, chapterNr=vers.chapterNr, bookNr=vers.bookNr, translationIdentifier=trWord)
            regex = re.compile("^.*rmac=\"([^\"]*)\" str=\"([^\"]*)\">([^<]*)<", re.MULTILINE)
            if regex is not None:
                found = regex.findall(vers.versText)
                for one in found:
                    # find vers in translation
                    # regex2 = re.compile("^.*str=\"" + one[1] + "\".*>(.*)<.*", re.MULTILINE)
                    # word = ''
                    # if regex2 is not None:
                        # found2 = regex2.findall(trVers[0].versText)
                        # Todo: Handle multiple strong numbers in one verse
                        # if len(found2) > 1:
                            # word = ' oder '.join(found2)
                        # elif len(found2) > 0:
                            # word = found2[0]
                    bvers = BibleVers.objects.filter(bookNr=vers.vers.bookNr, versNr=vers.vers.versNr, chapterNr=vers.vers.chapterNr)
                    if bvers.count() > 0:
                        # search for pronounciation in strongsgreek.xml
                        for onegreek in entries:
                            if int(onegreek.get("strongs")) == int(one[1]):
                                translit = onegreek.find("./greek").get("translit")
                                break
                        strong = StrongNr(pronounciation=translit, strongNr=int(one[1]), grammar=one[0], translationIdentifier=vers.translationIdentifier, greek=one[2], vers=bvers[0])
                        strong.save()
        return s


    def init_bible_books(self):
        s = ''
        f = open('./bibleBooks_de.txt', 'r')
        bookNr = 0
        for line in f:
            bookNr += 1
            ele = line.split(',')
            if len(ele) >= 2:
                ele = [x.strip() for x in ele]
                bookNames = BibleBook.objects.filter(nr=bookNr, language='de')
                if bookNames.count() > 0:
                    bookNames = bookNames[0]
                else:
                    bookNames = BibleBook()
                bookNames.nr = bookNr
                bookNames.language = 'de'
                bookNames.name = ele[0]
                self.stdout.write(ele[0] + ' (', ending='')
                if len(ele) > 1:
                    bookNames.short_name = ele[1]
                    self.stdout.write(ele[1], ending='')
                self.stdout.write(')', ending='')
                if len(ele) > 2:
                    bookNames.alternativeNames = ',' + string.join(ele[2:], ',') + ','
                    # self.stdout.write(' [' + bookNames.alternativeNames.encode('ascii') + ']', ending='')
                self.stdout.write('')
                bookNames.save()
        return s