export default function ContactDetails({ form }) {
  return (
    <div className="space-y-4">
      <div className="form-control">
        <label className="label font-medium text-dark-purple">Contact Email</label>
        <input
          type="email"
          className="input input-bordered bg-white"
          placeholder="Enter contact email"
          {...form.register('contact_email')}
        />
      </div>

      <div className="form-control">
        <label className="label font-medium text-dark-purple">Contact Phone</label>
        <input
          type="tel"
          className="input input-bordered bg-white"
          placeholder="Enter contact phone"
          {...form.register('contact_phone')}
        />
      </div>

      <div className="form-control">
        <label className="label font-medium text-dark-purple">Website URL</label>
        <input
          type="url"
          className="input input-bordered bg-white"
          placeholder="Enter website URL"
          {...form.register('website_url')}
        />
      </div>
    </div>
  );
}