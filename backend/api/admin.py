from django.contrib import admin
from api.models import AttendeeUser,Organizer,Event,Ticket,Comment,Bookmarks

# Register your models here.
admin.site.register(Ticket)
admin.site.register(Comment)
admin.site.register(Bookmarks)


@admin.register(AttendeeUser)
class AttendeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email')
    search_fields = ('first_name', 'last_name', 'email')
    
    
@admin.register(Organizer)
class OrganizerAdmin(admin.ModelAdmin):
    list_display = ('id', 'organizer_name', 'email', 'verification_status', 'is_verified')
    list_filter = ('verification_status',)
    search_fields = ('organizer_name', 'email')
    actions = ['approve_organizer', 'reject_organizer']

    def approve_organizer(self, request, queryset):
        """
        Verify selected organizers, setting their verification status to 'VERIFIED' and
        their is_verified flag to True.
        """
        queryset.update(verification_status='VERIFIED')
        queryset.update(is_verified = True)

    def reject_organizer(self, request, queryset):
        """
        Reject selected organizers, setting their verification status to 'REJECTED' and
        their is_verified flag to False.
        """
        queryset.update(verification_status='REJECTED')
        queryset.update(is_verified = False)

    approve_organizer.short_description = 'Verified selected organizers'
    reject_organizer.short_description = 'Reject selected organizers'
    
@admin.register(Event)
class Event(admin.ModelAdmin):
    list_display = ('id', 'event_name', 'address', 'verification_status' ,'is_verified')
    list_filter = ('verification_status',)
    search_fields = ('event_name',)
    actions = ['verified_event', 'rejected_event']

    def verified_event(self, request, queryset):
        """
        Verify selected events, setting their verification status to 'VERIFIED' and
        their is_verified flag to True.
        """
        queryset.update(is_verified = True)
        queryset.update(verification_status='VERIFIED')

    def rejected_event(self, request, queryset):
        """
        Reject selected events, setting their verification status to 'REJECTED' and
        their is_verified flag to False.
        """
        queryset.update(is_verified = False)
        queryset.update(verification_status='REJECTED')

    verified_event.short_description = 'Verify selected events'
    rejected_event.short_description = 'Reject selected events'




