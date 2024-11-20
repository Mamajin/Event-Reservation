from api.views.modules import * 
from .user_schema import UserProfileSchema


class CommentType(str, Enum):
    LIKE = 'LIKE'
    LOVE = 'LOVE'
    LAUGH = 'LAUGH'
    
class CommentSchema(Schema):
    parent_id: Optional[int] = None
    content: str

class CommentResponseSchema(Schema):
    id: int
    user: UserProfileSchema
    content: str
    created_at: datetime
    status: str
    replies: List['CommentResponseSchema'] = [] 

    @classmethod
    def from_comment(cls, comment: Comment) -> Dict:
        """Serialize a Comment instance, including nested fields."""
        return {
            "id": comment.id,
            "user": UserProfileSchema(
                id=comment.user.id,
                username=comment.user.username,
                profile_picture=comment.user.profile_picture,
            ).dict(),
            "content": comment.content,
            "created_at": comment.created_at,
            "status": comment.status,
            "replies": [cls.from_comment(reply) for reply in comment.replies.all()],
        }


class CommentReaction(Schema):
    comment_id: int
    reaction_type: str
    
class CommentReactionResponseSchema(Schema):
    id: int
    comment: CommentResponseSchema
    user: UserProfileSchema
    reaction_type: str
    created_at: datetime
    