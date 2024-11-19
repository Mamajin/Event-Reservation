from api.views.modules import *


# Schema for Email
class EmailVerificationSchema(Schema):
    token: str

class EmailVerificationResponseSchema(Schema):
    message: str
    verified: bool

# Schema for Error
class ErrorResponseSchema(Schema):
    error: str
    
# Schema for File Upload
class FileUploadResponseSchema(Schema):
    file_url: str
    message: str = "Upload successful"
    file_name: str
    uploaded_at: datetime