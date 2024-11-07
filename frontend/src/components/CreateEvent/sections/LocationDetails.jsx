import { useState } from 'react';
import Map from '../../Map';

export default function LocationDetails({ form }) {
  const isOnline = form.watch('is_online');
  const [error, setError] = useState('');
  const [formData, setFormData] = useState({
    address: '',
    latitude: null,
    longitude: null,
  });

  return (
    <div className="space-y-4">
      <div className="form-control">
        <label className="label cursor-pointer justify-start gap-4">
          <input
            type="checkbox"
            className="toggle"
            {...form.register('is_online')}
          />
          <span className="label-text font-medium text-dark-purple">Online Event</span>
        </label>
      </div>

      {isOnline ? (
        <div className="form-control">
          <label className="label font-medium text-dark-purple">Meeting Link</label>
          <input
            type="url"
            className="input input-bordered bg-white"
            placeholder="Enter meeting URL"
            {...form.register('meeting_link')}
          />
        </div>
      ) : (
        <>
          <div className="form-control">
            <label className="label font-medium text-dark-purple">Address</label>
            <input
              id="address-input"
              type="text"
              className="input input-bordered bg-white"
              placeholder="Enter venue address"
              {...form.register('address')}
            />
          </div>
          <Map form={form} setError={setError} />
        </>
      )}
    </div>
  );
}
