from django.contrib import admin
from api.models import AttendeeUser,Organizer,Event,Ticket,Comment,Bookmarks

# Register your models here.
admin.site.register(AttendeeUser)
admin.site.register(Event)
admin.site.register(Ticket)
admin.site.register(Comment)
admin.site.register(Bookmarks)


@admin.register(Organizer)
class OrganizerAdmin(admin.ModelAdmin):
    list_display = ('id', 'organizer_name', 'email', 'verification_status')
    list_filter = ('verification_status',)
    search_fields = ('organizer_name', 'email')
    actions = ['approve_organizer', 'reject_organizer']

    def approve_organizer(self, request, queryset):
        queryset.update(verification_status='VERIFIED')
        queryset.update(is_verified = True)

    def reject_organizer(self, request, queryset):
        queryset.update(verification_status='REJECTED')
        queryset.update(is_verified = False)

    approve_organizer.short_description = 'Approve selected organizers'
    reject_organizer.short_description = 'Reject selected organizers'


