# -*- coding: utf8 -*-
from django.core.management.base import BaseCommand, CommandError
from strongs.api.models import BibleBook
from os import path
from xml.etree import ElementTree as ElementTree
import re
import string


class Command(BaseCommand):
    args = "<bible_books_file>"
    help = 'Initializes the database with the bible books.'


    def add_arguments(self, parser):
        parser.add_argument('bible_books_file', nargs=1, type=str)


    def handle(self, *args, **options):
        try:
            self.init_bible_books(args)
        except:
            raise CommandError('Bible book file "%s" does not exist, or another error occured while inserting the bible books.' % args)


    def init_bible_books(self, path):
        s = ''
        f = open(path, 'r')
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
