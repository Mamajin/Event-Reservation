from api.views.modules import *


class OrganizerType(str, Enum):
    INDIVIDUAL = 'INDIVIDUAL'
    COMPANY = 'COMPANY'
    NONPROFIT = 'NONPROFIT'
    EDUCATIONAL = 'EDUCATIONAL'
    GOVERNMENT = 'GOVERNMENT'
    
class OrganizerSchema(Schema):
    organizer_name: Optional[str]
    email: Optional[EmailStr]
    organization_type: Optional[OrganizerType]

class OrganizerResponseSchema(Schema):
    id: int
    organizer_name: str
    email: EmailStr
    organization_type: OrganizerType
    logo: Optional[str]
    is_verified: bool
    
class OrganizerUpdateSchema(Schema):
    organizer_name: Optional[str] =Field(None)
    email: Optional[EmailStr]= ""
    organization_type: Optional[OrganizerType] = "INDIVIDUAL"