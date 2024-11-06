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
  const handleFileChange = (file) => {
    if (file.type !== 'image/jpeg' && file.type !== 'image/png') {
      alert('Only JPEG and PNG files are allowed.');
      return;
    }
    if (file.size > 5 * 1024 * 1024) {
      alert('File size exceeds the limit of 5 MB.');
      return;
    }

    setValue('event_image', file);
    setEventImage(file);
  };
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
      <div className="grid gap-4">
      <div className="form-control">
        <label className="label font-medium text-dark-purple">Short Description</label>
        <textarea
          className="textarea textarea-bordered h-24 bg-white"
          placeholder="Brief overview of your event"
          {...form.register('description', { required: true })}
        />
      </div>

      <div className="form-control">
        <label className="label font-medium text-dark-purple">Detailed Description</label>
        <textarea
          className="textarea textarea-bordered h-32 bg-white"
          placeholder="Provide detailed information about your event"
          {...form.register('detailed_description', { required: true })}
        />
      </div>
    </div>
    <div className="grid gap-4">
      <div className="grid grid-cols-2 gap-4">
        <div className="form-control">
          <label className="label font-medium text-dark-purple">Tags</label>
          <input
            type="text"
            className="input input-bordered bg-white"
            placeholder="Enter tags (comma-separated)"
            {...form.register('tags')}
          />
        </div>

        <div className="form-control">
          <label className="label font-medium text-dark-purple">Minimum Age Requirement</label>
          <input
            type="number"
            className="input input-bordered bg-white"
            placeholder="Enter minimum age"
            {...form.register('min_age_requirement', { valueAsNumber: true })}
          />
        </div>
      </div>
    </div>
    <div className="mt-6 w-full">
      <FileInput label="Event Banner" name="event_file" onChange={handleFileChange} accept=".jpg,.jpeg,.png,.pdf" />
    </div>
    </div>
    
  );
}
