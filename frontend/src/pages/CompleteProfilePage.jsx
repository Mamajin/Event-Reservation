import { useState } from "react";

function CompleteProfile() {
    const [phoneNumber, setPhoneNumber] = useState("");
    const [birthDate, setBirthDate] = useState("");
    const [address, setAddress] = useState("");

    const handleSubmit = (e) => {
        e.preventDefault();
    };

    return (
        <div className="min-h-screen bg-white flex flex-col items-center justify-center p-4">
            <div className="card w-full max-w-md bg-base-100 shadow-xl">
                <div className="card-body bg-white">
                    <h2 className="card-title text-2xl text-dark-purple font-bold text-center">
                        Complete Your Profile
                    </h2>
                    <p className="text-base-60 pb-6">
                        Please provide your additional information to complete your profile
                    </p>

                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div className="form-control">
                            <input
                                type="text"
                                placeholder="Phone Number"
                                className="input text-gray-600 bg-gray-100 input-bordered w-full"
                                value={phoneNumber}
                                onChange={(e) => setPhoneNumber(e.target.value)}
                                required
                            />
                        </div>

                        <div className="form-control">
                            <input
                                type="date"
                                placeholder="Birth Date"
                                className="input text-gray-600 bg-gray-100 input-bordered w-full"
                                value={birthDate}
                                onChange={(e) => setBirthDate(e.target.value)}
                                required
                            />
                        </div>

                        <div className="form-control">
                            <input
                                type="text"
                                placeholder="Address"
                                className="input text-gray-600 bg-gray-100 input-bordered w-full"
                                value={address}
                                onChange={(e) => setAddress(e.target.value)}
                                required
                            />
                        </div>

                        <button type="submit" className="btn btn-dark-purple w-full">
                            Save Profile
                        </button>
                    </form>
                </div>
            </div>
        </div>
    );
}

export default CompleteProfile;