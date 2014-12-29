from django.conf.urls import patterns, url, include
from rest_framework.urlpatterns import format_suffix_patterns

from .api import UserList, UserDetail
from .api import PostList, PostDetail, UserPostList
from .api import PhotoList, PhotoDetail, PostPhotoList
from .api import BibleTranslationList, BibleTranslationDetail
from .api import BibleBookList, BibleBookDetail
from .api import BibleVersList, BibleVersDetail
from .api import BibleTextChapterList

user_urls = patterns('',
    url(r'^/(?P<username>[0-9a-zA-Z_-]+)/posts$', UserPostList.as_view(), name='userpost-list'),
    url(r'^/(?P<username>[0-9a-zA-Z_-]+)$', UserDetail.as_view(), name='user-detail'),
    url(r'^$', UserList.as_view(), name='user-list')
)

post_urls = patterns('',
    url(r'^/(?P<pk>\d+)/photos$', PostPhotoList.as_view(), name='postphoto-list'),
    url(r'^/(?P<pk>\d+)$', PostDetail.as_view(), name='post-detail'),
    url(r'^$', PostList.as_view(), name='post-list')
)

photo_urls = patterns('',
    url(r'^/(?P<pk>\d+)$', PhotoDetail.as_view(), name='photo-detail'),
    url(r'^$', PhotoList.as_view(), name='photo-list')
)


############################################################################################


translation_urls = patterns('',
    url(r'^$', BibleTranslationList.as_view(), name='translation-list'),
    url(r'^/(?P<identifier>.+)/?$', BibleTranslationDetail.as_view(), name='translation'),
)

book_urls = patterns('',
    url(r'^/?$', BibleBookList.as_view(), name='book-list'),
    url(r'^/(?P<language>[^/]{2,3})/?$', BibleBookList.as_view(), name='book-language-list'),
    url(r'^/(?P<language>[^/]{2,3})/(?P<nr>\d+)/?$', BibleBookDetail.as_view(), name='book'),
)

vers_urls = patterns('',
    url(r'^/(?P<bookNr__language>[^/]{2,3})/(?P<bookNr__nr>\d+)/(?P<chapterNr>\d+)/?$', BibleVersList.as_view(), name='vers-list'),
    url(r'^/(?P<pk>\d+)/?$', BibleVersDetail.as_view(), name='vers-list'),
)

# search_urls = patterns('',
#     url(r'^/(?P<translation>.+)/(?P<search>.+)$', BibleTranslationList.as_view(), name='translation-list')
# )

bible_urls = patterns('',
    url(r'^/(?P<translation>.+)/(?P<bookNr>.+)/(?P<chapterNr>\d+)/$', BibleTextChapterList.as_view(), name='bible')
)




urlpatterns = patterns('',
    url(r'^users', include(user_urls)),
    url(r'^posts', include(post_urls)),
    url(r'^photos', include(photo_urls)),
    url(r'^translations', include(translation_urls)),
    # url(r'^search', include(search_urls)),
    url(r'^bible', include(bible_urls)),
    url(r'^books', include(book_urls)),
    url(r'^verses', include(vers_urls)),
)

urlpatterns = format_suffix_patterns(urlpatterns)