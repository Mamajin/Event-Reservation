from api.views.schemas.organizer_schema import OrganizerSchema, OrganizerUpdateSchema, OrganizerResponseSchema
from api.views.schemas.other_schema import ErrorResponseSchema, FileUploadResponseSchema
from .modules import *
from .strategy.organizer_strategy import *


@api_controller('/organizers/', tags=['Organizers'])    
class OrganizerAPI:
    @http_post('/apply-organizer',response={201: OrganizerResponseSchema, 400: ErrorResponseSchema}, auth=JWTAuth())    
    def apply_organizer(self, request: HttpRequest, form: OrganizerSchema = Form(...)):
        """Apply an authenticated user to be an organizer"""
        strategy : ApplyOrganizerStrategy = ApplyOrganizerStrategy.get_strategy('apply_organizer')
        return strategy.execute(request, form)

    @http_delete('/delete-event/{event_id}', response={204: None, 403: ErrorResponseSchema, 404: ErrorResponseSchema}, auth=JWTAuth())
    def delete_event(self, request: HttpRequest, event_id: int):
        """Delete event by event id."""
        strategy : DeleteEventStrategy = DeleteEventStrategy.get_strategy('delete_event')
        return strategy.execute(request, event_id=event_id)

    @http_patch('/update-organizer', response={200: OrganizerUpdateSchema, 401: ErrorResponseSchema, 404: ErrorResponseSchema}, auth=JWTAuth())
    def update_organizer(self, request: HttpRequest, data: OrganizerUpdateSchema):
        """Update the profile information of the authenticated organizer."""
        strategy : UpdateOrganizerStrategy = UpdateOrganizerStrategy.get_strategy('update_organizer')
        return strategy.execute(request, data=data)
            
    @http_delete('/revoke-organizer', response={204: None, 403: ErrorResponseSchema, 404: ErrorResponseSchema}, auth=JWTAuth())
    def revoke_organizer(self, request: HttpRequest):
        """Revoke the organizer role of the authenticated user."""
        strategy : RevokeOrganizerStrategy = RevokeOrganizerStrategy.get_strategy('revoke_organizer')
        return strategy.execute(request)
        
    @http_get('/view-organizer', response={200: OrganizerResponseSchema, 401: ErrorResponseSchema, 404: ErrorResponseSchema}, auth=JWTAuth())
    def view_organizer(self, request: HttpRequest):
        """View the organizer profile."""
        strategy : ViewOrganizerStrategy = ViewOrganizerStrategy.get_strategy('view_organizer')
        return strategy.execute(request)
        
    @http_post('/{organizer_id}/upload/logo/', response={200: FileUploadResponseSchema, 400: ErrorResponseSchema}, auth=JWTAuth())
    def upload_profile_picture(self, request: HttpRequest, organizer_id: int, logo: UploadedFile = File(...)):
        """Upload a logo for a organzier's profile."""
        strategy : UploadLogoStrategy = UploadLogoStrategy.get_strategy('upload_logo')        
        return strategy.execute(request, organizer_id=organizer_id, logo=logo)               
