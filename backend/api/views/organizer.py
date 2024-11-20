from api.views.schemas.organizer_schema import OrganizerSchema, OrganizerUpdateSchema, OrganizerResponseSchema
from api.views.schemas.other_schema import ErrorResponseSchema, FileUploadResponseSchema
from .modules import *
from .strategy.organizer_strategy import OrganizerStrategy


@api_controller('/organizers/', tags=['Organizers'])    
class OrganizerAPI:
    @route.post('/apply-organizer',response={201: OrganizerResponseSchema, 400: ErrorResponseSchema}, auth=JWTAuth())    
    def apply_organizer(self, request: HttpRequest, form: OrganizerSchema = Form(...)):
        """Apply an authenticated user to be an organizer"""
        strategy : OrganizerStrategy = OrganizerStrategy.get_strategy('apply_organizer')
        return strategy.execute(request, form)

    @route.delete('/delete-event/{event_id}', response={204: dict, 403: ErrorResponseSchema, 404: ErrorResponseSchema}, auth=JWTAuth())
    def delete_event(self, request: HttpRequest, event_id: int):
        """Delete event by event id."""
        strategy : OrganizerStrategy = OrganizerStrategy.get_strategy('delete_event')
        return strategy.execute(request, event_id)

    @route.patch('/update-organizer', response={200: OrganizerResponseSchema, 401: ErrorResponseSchema, 404: ErrorResponseSchema}, auth=JWTAuth())
    def update_organizer(self, request: HttpRequest, data: OrganizerUpdateSchema):
        """Update the profile information of the authenticated organizer."""
        strategy : OrganizerStrategy = OrganizerStrategy.get_strategy('update_organizer')
        return strategy.execute(request, data)
            
    @route.delete('/revoke-organizer', response={200: None, 403: ErrorResponseSchema, 404: ErrorResponseSchema}, auth=JWTAuth())
    def revoke_organizer(self, request: HttpRequest):
        """Revoke the organizer role of the authenticated user."""
        strategy : OrganizerStrategy = OrganizerStrategy.get_strategy('revoke_organizer')
        return strategy.execute(request)
        
    @route.get('/view-organizer', response={200: OrganizerResponseSchema, 401: ErrorResponseSchema, 404: ErrorResponseSchema}, auth=JWTAuth())
    def view_organizer(self, request: HttpRequest):
        """View the organizer profile."""
        strategy : OrganizerStrategy = OrganizerStrategy.get_strategy('view_organizer')
        return strategy.execute(request)
        
    @route.post('/{organizer_id}/upload/logo/', response={200: FileUploadResponseSchema, 400: ErrorResponseSchema}, auth=JWTAuth())
    def upload_profile_picture(self, request: HttpRequest, organizer_id: int, logo: UploadedFile = File(...)):
        """Upload a logo for a organzier's profile."""
        strategy : OrganizerStrategy = OrganizerStrategy.get_strategy('upload_logo')        
        return strategy.execute(request, organizer_id, logo)               
