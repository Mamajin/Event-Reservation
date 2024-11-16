export default function TicketingDetails({ form }) {
  const isFree = form.watch('is_free');

  return (
    <div className="space-y-4">
      <div className="form-control ">
        <label className="label cursor-pointer justify-start gap-4">
          <input
            type="checkbox"
            className="toggle  bg-white"
            {...form.register('is_free')}
          />
          <span className="label-text font-medium text-dark-purple">Free Event</span>
        </label>
      </div>
      {!isFree && (
        <div className="grid grid-cols-2 gap-4">
          <div className="form-control">
            <label className="label font-medium text-dark-purple">Ticket Price</label>
            <input
              type="number"
              className="input input-bordered bg-white"
              placeholder="Enter ticket price"
              {...form.register('ticket_price', { valueAsNumber: true })}
            />
          </div>

          <div className="form-control">
            <label className="label font-medium text-dark-purple">Expected Price</label>
            <input
              type="number"
              className="input input-bordered bg-white"
              placeholder="Enter expected price"
              {...form.register('expected_price', { valueAsNumber: true })}
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
            {...form.register('max_attendee', { valueAsNumber: true })}
          />
        </div>

        <div className="form-control">
          <label className="label font-medium text-dark-purple">Allowed Email Domains</label>
          <input
            type="text"
            className="input input-bordered bg-white"
            placeholder="Enter allowed domains (comma-separated)"
            {...form.register('allowed_email_domains')}
          />
        </div>
      </div>
      <div className="form-control">
        <label className="label font-medium text-dark-purple">Terms and Conditions</label>
        <textarea
          className="textarea textarea-bordered h-24 bg-white"
          placeholder="Fill in the terms and condition for your event"
          {...form.register('terms_and_conditions')}
        />
      </div>
    </div>
  );
}