import { LuCheckCircle2 } from "react-icons/lu";

export function OrganizerInfo({ organizer }) {
  return (
    <div className="container bg-white rounded">
      <div className="card bg-white">
        <div className="card-body">
          <div className="flex items-center gap-4">
            <div className="avatar">
              <div className="w-14 h-14 rounded-full ring ring-amber-300 ring-offset-base-100 ring-offset-2">
                <img src={organizer.logo} alt={organizer.organizer_name} />
              </div>
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-xl text-dark-purple font-semibold">{organizer.organizer_name}</h2>
                {organizer.is_verified && (
                  <LuCheckCircle2 className="h-5 w-5 text-dark-purple" />
                )}
              </div>
              <p className="text-sm text-base-content/70">{organizer.organization_type}</p>
              <a href={`mailto:${organizer.email}`} className="link link-dark-purple text-sm">
                {organizer.email}
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}