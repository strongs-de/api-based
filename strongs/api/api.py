from rest_framework import generics, permissions
from django.shortcuts import get_object_or_404, get_list_or_404

from .serializers import UserSerializer, PostSerializer, PhotoSerializer
from .models import User, Post, Photo
from .permissions import PostAuthorCanEditPermission


from .serializers import BibleTranslationSerializer, BibleBookSerializer, BibleVersSerializer, BibleTextSerializer
from .models import BibleTranslation, BibleBook, BibleVers, BibleText


class UserList(generics.ListAPIView):
    model = User
    serializer_class = UserSerializer
    permission_classes = [
        permissions.AllowAny
    ]


class UserDetail(generics.RetrieveAPIView):
    model = User
    serializer_class = UserSerializer
    lookup_field = 'username'


class PostMixin(object):
    model = Post
    serializer_class = PostSerializer
    permission_classes = [
        PostAuthorCanEditPermission
    ]

    def pre_save(self, obj):
        """Force author to the current user on save"""
        obj.author = self.request.user
        return super(PostMixin, self).pre_save(obj)


class PostList(PostMixin, generics.ListCreateAPIView):
    pass


class PostDetail(PostMixin, generics.RetrieveUpdateDestroyAPIView):
    pass


class UserPostList(generics.ListAPIView):
    model = Post
    serializer_class = PostSerializer

    def get_queryset(self):
        queryset = super(UserPostList, self).get_queryset()
        return queryset.filter(author__username=self.kwargs.get('username'))


class PhotoList(generics.ListCreateAPIView):
    model = Photo
    serializer_class = PhotoSerializer
    permission_classes = [
        permissions.AllowAny
    ]


class PhotoDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Photo
    serializer_class = PhotoSerializer
    permission_classes = [
        permissions.AllowAny
    ]


class PostPhotoList(generics.ListAPIView):
    model = Photo
    serializer_class = PhotoSerializer

    def get_queryset(self):
        queryset = super(PostPhotoList, self).get_queryset()
        return queryset.filter(post__pk=self.kwargs.get('pk'))


####################################################################################

class MultipleFieldRetrieveMixin(object):
    """
    Apply this mixin to any view or viewset to get multiple field filtering
    based on a `lookup_fields` attribute, instead of the default single field filtering.
    """
    def get_object(self):
        queryset = self.get_queryset()             # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]
        return get_object_or_404(queryset, **filter)  # Lookup the object


class MultipleFieldLookupMixin(object):
    def get_filter_object(self):
        filter = {}
        for i in range(0, len(self.lookup_fields)):
            urlparam = self.lookup_fields[i]
            if hasattr(self, 'url_fields') and len(self.lookup_fields) == len(self.url_fields):
                urlparam = self.url_fields[i]
            if self.kwargs.get(urlparam):
                filter[self.lookup_fields[i]] = self.kwargs[urlparam]
        return filter


class BibleTranslationList(generics.ListAPIView):
    model = BibleTranslation
    serializer_class = BibleTranslationSerializer


class BibleTranslationDetail(generics.RetrieveAPIView):
    model = BibleTranslation
    serializer_class = BibleTranslationSerializer
    lookup_field = 'identifier'


class BibleBookList(generics.ListAPIView):
    model = BibleBook
    serializer_class = BibleBookSerializer

    def get_queryset(self):
        queryset = super(BibleBookList, self).get_queryset()
        if not self.kwargs.get('language'):
            return queryset
        return queryset.filter(language=self.kwargs.get('language'))


class BibleBookDetail(MultipleFieldRetrieveMixin, generics.RetrieveAPIView):
    model = BibleBook
    serializer_class = BibleBookSerializer
    lookup_fields = ('language', 'nr')


class BibleVersList(MultipleFieldLookupMixin, generics.ListAPIView):
    model = BibleVers
    serializer_class = BibleVersSerializer
    lookup_fields = ('bookNr__language', 'bookNr__nr', 'chapterNr')

    def get_queryset(self):
        queryset = super(BibleVersList, self).get_queryset()
        filtr = self.get_filter_object()
        return queryset.filter(**filtr)


class BibleVersDetail(generics.RetrieveAPIView):
    model = BibleVers
    serializer_class = BibleVersSerializer
    lookup_field = 'pk'



class BibleTextChapterList(MultipleFieldLookupMixin, generics.ListAPIView):
    model = BibleText
    serializer_class = BibleTextSerializer
    lookup_fields = ('translationIdentifier__identifier', 'vers__bookNr__nr', 'vers__chapterNr')
    url_fields = ('translation', 'bookNr', 'chapterNr')

    def get_queryset(self):
        queryset = super(BibleTextChapterList, self).get_queryset()
        filtr = self.get_filter_object()
        return queryset.filter(**filtr)
