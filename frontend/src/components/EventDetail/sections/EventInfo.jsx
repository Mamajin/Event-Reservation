import { format } from 'date-fns';

export function EventDetails({ event }) {
  return (
    <div className="container bg-white py-8">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-8">
          <div className="card bg-white">
            <div className="card-body">
              <h2 className="card-title text-2xl mb-4 text-dark-purple">About the Event</h2>
              <p className="whitespace-pre-wrap text-base-content/80 leading-relaxed">
                {event.detailed_description || event.description}
              </p>
            </div>
          </div>
        </div>
        <div className="space-y-6">
          <div className="card bg-base">
            <div className="card-body">
              <h3 className="font-semibold text-lg mb-4 text-dark-purple">Date & Time</h3>
              <div className="space-y-4">
                <div className="flex items-start gap-3">
                  <div>
                    <p className="font-medium text-dark-purple">Start</p>
                    <p className="text-sm text-base-content/70">
                      {format(new Date(event.start_date_event), 'PPP')}
                    </p>
                    <p className="text-sm text-base-content/70">
                      {format(new Date(event.start_date_event), 'p')}
                    </p>
                  </div>
                </div>
                <div className="divider my-2"></div>
                <div className="flex items-start gap-3">
                  <div>
                    <p className="font-medium text-dark-purple">End</p>
                    <p className="text-sm text-base-content/70">
                      {format(new Date(event.end_date_event), 'PPP')}
                    </p>
                    <p className="text-sm text-base-content/70">
                      {format(new Date(event.end_date_event), 'p')}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
