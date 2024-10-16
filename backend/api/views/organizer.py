from ninja import Router, Schema, Form
from django.contrib.auth import authenticate
from api.models import Organizer
from ninja.responses import Response
from rest_framework import status


router = Router()


class OrganizerSchema(Schema):
    organizer_name: str
    email: str

class OrganizerResponseSchema(Schema):
    id: int
    organizer_name: str
    email: str

@router.post('/apply-organizer', response=OrganizerResponseSchema)
def apply_organizer(request, form: OrganizerSchema = Form(...)):
    if not request.user.is_authenticated:
        return Response({'error': 'User must be logged in to apply as an organizer'}, status=status.HTTP_401_UNAUTHORIZED)
    
    if Organizer.objects.filter(user=request.user).exists():
        return Response({'error': 'User is already an organizer'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        organizer = Organizer.objects.create(
            user=request.user,
            organizer_name=form.organizer_name,
            email=form.email
        )
        return Response({
            'id': organizer.id,
            'organizer_name': organizer.organizer_name,
            'email': organizer.email
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
