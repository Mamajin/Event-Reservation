import { useState } from 'react';

export default function LocationDetails({ form }) {
  const isOnline = form.watch('is_online');

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
    </div>
  );
}
