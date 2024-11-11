import DateTimeInput from "../../DateTimeInput";

export default function DateTimeDetails({ form }) {
  return (
    <div className="grid grid-cols-2 gap-6">
      <div className="space-y-4">
        <div className="form-control">
          <DateTimeInput
            label="Registration Start Date"
            name="start_date_register"
            value={form.getValues("start_date_register")}
            onChange={(e) => form.setValue("start_date_register", e.target.value)}
            required={true}
          />
        </div>
        <div className="form-control">
          <DateTimeInput
            label="Event Start Date"
            name="start_date_event"
            value={form.getValues("start_date_event")}
            onChange={(e) => form.setValue("start_date_event", e.target.value)}
            required={true}
          />
        </div>
      </div>
      <div className="space-y-4">
        <div className="form-control">
          <DateTimeInput
            label="Registration End Date"
            name="end_date_register"
            value={form.getValues("end_date_register")}
            onChange={(e) => form.setValue("end_date_register", e.target.value)}
            required={true}
          />
        </div>
        <div className="form-control">
          <DateTimeInput
            label="Event End Date"
            name="end_date_event"
            value={form.getValues("end_date_event")}
            onChange={(e) => form.setValue("end_date_event", e.target.value)}
            required={true}
          />
        </div>
      </div>
    </div>
  );
}
