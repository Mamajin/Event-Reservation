from .schemas import EventInputSchema, ErrorResponseSchema, EventResponseSchema
from .modules import JWTAuth, Organizer, HttpError, timezone, Event, HttpRequest, logger, Response, Router, List, get_object_or_404, Session

router = Router()

class EventAPI:

    @router.post('/create-event', response=EventResponseSchema, auth=JWTAuth())
    def create_event(request, data: EventInputSchema):
        this_user = request.user
        try:
            organizer = Organizer.objects.get(user=this_user)
        except Organizer.DoesNotExist:
            raise HttpError(status_code=403, message="You are not an organizer.")
        
        event = Event(
            event_name=data.event_name,
            organizer=organizer,
            event_create_date=timezone.now(),
            start_date_event=data.start_date_event,
            end_date_event=data.end_date_event,
            start_date_register=data.start_date_register or timezone.now(),
            end_date_register=data.end_date_register,
            description=data.description,
            max_attendee=data.max_attendee
        )
        if event.is_valid_date():
            event.save()
            return EventResponseSchema.from_orm(event)
        else:
            return Response({'error': 'Please enter valid date'}, status=400)

    @router.get('/my-events', response=List[EventResponseSchema], auth=JWTAuth())
    def get_my_events(request: HttpRequest):
        try:
            organizer = Organizer.objects.get(user=request.user)
            events = Event.objects.filter(organizer=organizer)
            event_list = [EventInputSchema.from_orm(event) for event in events]
            logger.info(f"Organizer {organizer.organizer_name} retrieved their events.")
            return event_list
        except Organizer.DoesNotExist:
            logger.error(f"User {request.user.username} tried to access events but is not an organizer.")
            return Response({'error': 'User is not an organizer'}, status=404)
        except Exception as e:
            logger.error(f"Error while retrieving events for organizer {request.user.id}: {str(e)}")
            return Response({'error': str(e)}, status=400)

    @router.get('/events', response=List[EventResponseSchema])
    def list_all_events(request: HttpRequest):
        try:
            events = Event.objects.filter(event_create_date__lte=timezone.now()).order_by("-event_create_date")
            event_list = [EventResponseSchema.from_orm(event) for event in events]
            logger.info("Retrieved all events for the homepage.")
            return event_list
        except Exception as e:
            logger.error(f"Error while retrieving events for the homepage: {str(e)}")
            return Response({'error': str(e)}, status=400)

    @router.put('/edit-event-{event_id}', response={204: EventResponseSchema, 401: ErrorResponseSchema, 404: ErrorResponseSchema}, auth=JWTAuth())
    def edit_event(request: HttpRequest, event_id: int, data: EventInputSchema):
        try:
            event = Event.objects.get(id=event_id)
            organizer = Organizer.objects.get(user=request.user)
            if event.organizer != organizer:
                logger.warning(f"User {request.user.username} tried to edit an event they do not own.")
                return Response({'error': 'You are not allowed to edit this event.'}, status=403)
            
            Event.objects.filter(id = event_id).update(**data.dict())
                        
            event_data = EventResponseSchema.from_orm(event).dict()
            logger.info(f"Organizer {organizer.organizer_name} edited their event {event_id}.")
            return Response(event_data, status=204)
        except Event.DoesNotExist:
            logger.error(f"Event with ID {event_id} does not exist.")
            return Response({'error': 'Event not found'}, status=404)
        except Organizer.DoesNotExist:
            logger.error(f"User {request.user.username} is not an organizer.")
            return Response({'error': 'User is not an organizer'}, status=404)
        except Exception as e:
            logger.error(f"Error while editing event {event_id}: {str(e)}")
            return Response({'error': str(e)}, status=400)

    @router.get('/{event_id}', response=EventResponseSchema)
    def event_detail(request: HttpRequest, event_id: int):
        logger.info(f"Fetching details for event ID: {event_id} by user {request.user.username}.")
        event = get_object_or_404(Event, id=event_id)
        return EventResponseSchema.from_orm(event)