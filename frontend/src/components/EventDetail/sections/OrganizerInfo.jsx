import { LuCheckCircle2 } from "react-icons/lu";

export function OrganizerInfo({ organizer }) {
  return (
    <div className="container bg-white py-8">
      <div className="card bg-white">
        <div className="card-body">
          <div className="flex items-center gap-4">
            <div className="avatar">
              <div className="w-16 h-16 rounded-full ring ring-primary ring-offset-base-100 ring-offset-2">
                <img src={organizer.logo} alt={organizer.organizer_name} />
              </div>
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-xl font-semibold">{organizer.organizer_name}</h2>
                {organizer.is_verified && (
                  <LuCheckCircle2  className="h-5 w-5 text-primary" />
                )}
              </div>
              <p className="text-sm text-base-content/70">{organizer.organization_type}</p>
              <a href={`mailto:${organizer.email}`} className="link link-primary text-sm">
                {organizer.email}
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}