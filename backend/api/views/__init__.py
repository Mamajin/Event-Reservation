from api.views.user import router as user_router
from api.views.event import router as event_router
from api.views.organizer import router as organizer_router
from api.views.bookmarks import router as bookmark_router
from api.views.like import router as like_router
from api.views.comment import router as comment_router

__all__ = ['user_router', 'event_router', 
           'organizer_router', 
            'bookmark_router',
           'like_router', 'comment_router']
