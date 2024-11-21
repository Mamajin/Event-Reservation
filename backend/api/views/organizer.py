from api.views.schemas.organizer_schema import OrganizerSchema, OrganizerUpdateSchema, OrganizerResponseSchema
from api.views.schemas.other_schema import ErrorResponseSchema, FileUploadResponseSchema
from .modules import *
from .strategy.organizer_strategy import OrganizerStrategy


@api_controller('/organizers/', tags=['Organizers'])    
class OrganizerAPI:
    """
    Organizer API endpoints.
    """
    @route.post('/apply-organizer',response={201: OrganizerResponseSchema, 400: ErrorResponseSchema}, auth=JWTAuth())    
    def apply_organizer(self, request: HttpRequest, form: OrganizerSchema = Form(...)):
        """
        Apply to be an organizer

        Args:
            request (HttpRequest): The HTTP request object.
            form (OrganizerSchema): The organizer registration data.

        Returns:
            OrganizerResponseSchema: The created organizer object on successful registration.
        """
        strategy : OrganizerStrategy = OrganizerStrategy.get_strategy('apply_organizer')
        return strategy.execute(request, form)

    @route.delete('/delete-event/{event_id}', response={204: dict, 403: ErrorResponseSchema, 404: ErrorResponseSchema}, auth=JWTAuth())
    def delete_event(self, request: HttpRequest, event_id: int):
        """
        Delete an event by ID if the user is the organizer.

        Args:
            request (HttpRequest): The HTTP request object.
            event_id (int): ID of the event to delete.

        Returns:
            dict: Success message with status code 204 if the event is deleted.
            ErrorResponseSchema: Error message with status codes 403 or 404 if the user is not authorized 
            or the event does not exist.
        """
        strategy : OrganizerStrategy = OrganizerStrategy.get_strategy('delete_event')
        return strategy.execute(request, event_id)

    @route.patch('/update-organizer', response={200: OrganizerResponseSchema, 401: ErrorResponseSchema, 404: ErrorResponseSchema}, auth=JWTAuth())
    def update_organizer(self, request: HttpRequest, data: OrganizerUpdateSchema):
        """
        Update the profile information of the authenticated organizer.

        Args:
            request (HttpRequest): The HTTP request object.
            data (OrganizerUpdateSchema): The updated organizer data.

        Returns:
        """
        strategy : OrganizerStrategy = OrganizerStrategy.get_strategy('update_organizer')
        return strategy.execute(request, data)
            
    @route.delete('/revoke-organizer', response={200: None, 403: ErrorResponseSchema, 404: ErrorResponseSchema}, auth=JWTAuth())
    def revoke_organizer(self, request: HttpRequest):
        """
        Revoke the organizer role of the authenticated user.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            None: Success response with status code 200 if the organizer role is revoked.
            ErrorResponseSchema: Error message with status code 403 if the user is not authorized,
            or 404 if the user is not an organizer.
        """
        strategy : OrganizerStrategy = OrganizerStrategy.get_strategy('revoke_organizer')
        return strategy.execute(request)
        
    @route.get('/view-organizer', response={200: OrganizerResponseSchema, 401: ErrorResponseSchema, 404: ErrorResponseSchema}, auth=JWTAuth())
    def view_organizer(self, request: HttpRequest):
        """
        Retrieve the profile information of the authenticated organizer.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            OrganizerResponseSchema: Organizer profile details if successful.
            ErrorResponseSchema: Error message with status code 401 if not authorized,
            or 404 if the organizer profile does not exist.
        """
        strategy : OrganizerStrategy = OrganizerStrategy.get_strategy('view_organizer')
        return strategy.execute(request)
        
    @route.post('/{organizer_id}/upload/logo/', response={200: FileUploadResponseSchema, 400: ErrorResponseSchema}, auth=JWTAuth())
    def upload_profile_picture(self, request: HttpRequest, organizer_id: int, logo: UploadedFile = File(...)):
        """
        Upload a logo for an organizer.

        Args:
            request (HttpRequest): The HTTP request object.
            organizer_id (int): The ID of the organizer to upload a logo for.
            logo (UploadedFile): The uploaded logo file.

        Returns:
            FileUploadResponseSchema: Details of the uploaded logo, including URL, or an error response.
        """
        strategy : OrganizerStrategy = OrganizerStrategy.get_strategy('upload_logo')        
        return strategy.execute(request, organizer_id, logo)               
