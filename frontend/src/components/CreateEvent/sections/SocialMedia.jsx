export default function SocialMedia({ form }) {
  return (
    <div className="space-y-4">
      <div className="form-control">
        <label className="label font-medium text-dark-purple bg-white">Facebook URL</label>
        <input
          type="url"
          className="input input-bordered bg-white"
          placeholder="Enter Facebook URL"
          {...form.register('facebook_url')}
        />
      </div>

      <div className="form-control">
        <label className="label font-medium text-dark-purple bg-white">Twitter URL</label>
        <input
          type="url"
          className="input input-bordered bg-white"
          placeholder="Enter Twitter URL"
          {...form.register('twitter_url')}
        />
      </div>

      <div className="form-control">
        <label className="label font-medium text-dark-purple bg-white">Instagram URL</label>
        <input
          type="url"
          className="input input-bordered bg-white"
          placeholder="Enter Instagram URL"
          {...form.register('instagram_url')}
        />
      </div>
    </div>
  );
}