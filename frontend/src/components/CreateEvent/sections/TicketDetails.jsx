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
      </div>)}