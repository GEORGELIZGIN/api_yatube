from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, PostViewSet

comments_router = DefaultRouter()
posts_router = DefaultRouter()
comments_router.register(
    r'(?P<post_id>\d+)/comments', CommentViewSet,
    basename='comments')
posts_router.register('posts', PostViewSet)

urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token),
    path('', include(posts_router.urls)),
    path(r'posts/', include(comments_router.urls)),
]
