import FileInput from "../../FileInput";
import SelectInput from "../../SelectInput";

export default function BasicDetails({ form }) {
  const { watch, setValue } = form;

  const CATEGORY_OPTION = [
    { value: 'CONFERENCE', label: "Conference" },
    { value: 'WORKSHOP', label: "Workshop" },
    { value: 'SEMINAR', label: "Seminar" },
    { value: 'NETWORKING', label: "Networking" },
    { value: 'CONCERT', label: "Concert" },
    { value: 'OTHER', label: "Other" },
  ];

  const DRESS_CODE = [
    { value: "CASUAL", label: "Casual" },
    { value: "SMART_CASUAL", label: "Smart Casual" },
    { value: "BUSINESS_CASUAL", label: "Business Casual" },
    { value: "SEMI_FORMAL", label: "Semi Formal" },
    { value: "FORMAL", label: "Formal" },
    { value: "BLACK_TIE", label: "Black Tie" },
    { value: "WHITE_TIE", label: "White Tie" },
    { value: "THEMED", label: "Themed" },
    { value: "OUTDOOR_BEACH_CASUAL", label: "Outdoor Beach Casual" },
  ];

  return (
    <div className="grid gap-4">
      <div className="form-control">
        <label className="label font-medium text-dark-purple">Event Name</label>
        <input
          type="text"
          className="input input-bordered bg-white"
          placeholder="Enter event name"
          {...form.register('event_name', { required: true })}
        />
      </div>
      <div className="grid grid-cols-2 gap-4">
        <div className="form-control">
          <SelectInput
            label="Category"
            name="category"
            value={watch('category')}
            onChange={e => setValue('category', e.target.value)}
            options={CATEGORY_OPTION}
          />
        </div>
        <div className="form-control">
          <SelectInput
            label="Dress Code"
            name="dress_code"
            value={watch('dress_code')}
            onChange={e => setValue('dress_code', e.target.value)}
            options={DRESS_CODE}
          />
        </div>
      </div>
    </div>
  );
}
