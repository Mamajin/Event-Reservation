export default function TicketingDetails({ form }) {
  const { watch, setValue } = form;

  // Watch the visibility field
  const visibility = watch('visibility', 'PRIVATE'); // Default to PRIVATE

  const handleVisibilityChange = (isPublic) => {
    setValue('visibility', isPublic ? 'PUBLIC' : 'PRIVATE');
    if (isPublic) {
      setValue('allowed_email_domains', ''); // Clear email domains when switching to Public
    }
  };

  return (
    <div className="space-y-4">
      <div className="form-control">
        <label className="label justify-start gap-4">
          {/* Free or Paid Toggle */}
          <input
            type="checkbox"
            className="toggle bg-white"
            {...form.register('is_free')}
            defaultChecked
          />
          <span className="label-text font-medium text-dark-purple">
            Free Event
            </span>

          {/* Public or Private Toggle */}
          <input
            type="checkbox"
            className="toggle bg-white"
            checked={visibility === 'PUBLIC'}
            onChange={(e) => handleVisibilityChange(e.target.checked)}
          />
          <span className="label-text font-medium text-dark-purple">
            {visibility === 'PUBLIC' ? 'Public Event' : 'Private Event'}
          </span>
        </label>
      </div>

      {/* Show ticket price input if the event is not free */}
      {!watch('is_free') && (
        <div className="grid grid-cols-2 gap-4">
          <div className="form-control">
            <label className="label font-medium text-dark-purple">Ticket Price</label>
            <input
              type="number"
              className="input input-bordered bg-white"
              placeholder="Enter ticket price"
              {...form.register('ticket_price', { 
                valueAsNumber: true,
                min: 0,
              })}
              min="0"
            />
          </div>

          <div className="form-control">
            <label className="label font-medium text-dark-purple">Expected Price</label>
            <input
              type="number"
              className="input input-bordered bg-white"
              placeholder="Enter expected price"
              {...form.register('expected_price',{ 
                valueAsNumber: true,
                min: 0,
              })}
              min="0"
            />
          </div>
        </div>
      )}

      <div className="grid grid-cols-2 gap-4">
        <div className="form-control">
          <label className="label font-medium text-dark-purple">Maximum Attendees</label>
          <input
            type="number"
            className="input input-bordered bg-white"
            placeholder="Enter max attendees"
            {...form.register('max_attendee', { 
              valueAsNumber: true,
              min: 0,
            })}
            min="1"
          />
        </div>

        {/* Show allowed email domains input if event is private */}
        {visibility === 'PRIVATE' && (
          <div className="form-control">
            <label className="label font-medium text-dark-purple">Allowed Email Domains</label>
            <input
              type="text"
              className="input input-bordered bg-white"
              placeholder="Enter allowed domains (comma-separated)"
              {...form.register('allowed_email_domains')}
            />
          </div>
        )}
      </div>

      <div className="form-control">
        <label className="label font-medium text-dark-purple">Terms and Conditions</label>
        <textarea
          className="textarea textarea-bordered h-24 bg-white"
          placeholder="Fill in the terms and conditions for your event"
          {...form.register('terms_and_conditions')}
        />
      </div>
    </div>
  );
}