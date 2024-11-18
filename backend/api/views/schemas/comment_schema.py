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
    reactions: List[Dict] = []
    replies: List['CommentResponseSchema'] = []

class CommentReaction(Schema):
    comment_id: int
    reaction_type: str
    
class CommentReactionResponseSchema(Schema):
    id: int
    comment: CommentResponseSchema
    user: UserProfileSchema
    reaction_type: str
    created_at: datetime
    