from django.contrib import admin

from .models import User, Post, Photo, BibleTranslation, BibleBook, BibleText, BibleVers, BibleVersList, BibleVersNote, BibleVersNoteComment


admin.site.register(User)
admin.site.register(Post)
admin.site.register(Photo)

admin.site.register(BibleTranslation)
admin.site.register(BibleBook)
admin.site.register(BibleText)
admin.site.register(BibleVers)
admin.site.register(BibleVersNote)
admin.site.register(BibleVersNoteComment)
admin.site.register(BibleVersList)