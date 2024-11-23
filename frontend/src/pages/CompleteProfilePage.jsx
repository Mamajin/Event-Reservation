import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api"; // Assuming you've configured Axios for API requests
import { ACCESS_TOKEN, USER_ID } from "../constants";
import DateInput from "../components/DateInput";

function CompleteProfile() {
    const [phoneNumber, setPhoneNumber] = useState("");
    const [birthDate, setBirthDate] = useState("");
    const [address, setAddress] = useState("");
    const [error, setError] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchProfileData = async () => {
            const token = localStorage.getItem(ACCESS_TOKEN);
            if (token) {
                try {
                    const response = await api.get("/users/profile", {
                        headers: {
                            Authorization: `Bearer ${token}`,
                        },
                    });
                    setPhoneNumber(response.data.phone_number || "");
                    setBirthDate(response.data.birth_date || "");
                    setAddress(response.data.address || "");
                } catch (error) {
                    console.error("Error fetching profile:", error);
                }
            }
        };

        fetchProfileData();
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);

        try {
            const token = localStorage.getItem(ACCESS_TOKEN);
            const userId = localStorage.getItem(USER_ID);

            const profileData = {
                phone_number: phoneNumber,
                birth_date: birthDate,
                address: address,
            };

            const response = await api.patch(`/users/edit-profile/${userId}/`, profileData, {
                headers: {
                    Authorization: `Bearer ${token}`,
                    "Content-Type": "application/json",
                },
            });

            if (response.status === 200) {
                navigate("/");
            }
        } catch (error) {
            console.error("Error updating profile:", error);
            let errorMessage = "Failed to update profile. Please try again.";
            if (error.response) {
              errorMessage = error.response.data?.error || errorMessage;
            }
            alert(errorMessage);
            setError(errorMessage);
        } finally {
            setIsLoading(false);
        }
    };
    return (
        <div className="min-h-screen bg-white flex flex-col items-center justify-center p-4">
            <div className="card w-full max-w-md bg-base-100 shadow-xl">
                {isLoading && (
                    <div className="absolute inset-0 bg-base-100/50 backdrop-blur-sm flex items-center justify-center z-50 rounded-2xl">
                        <span className="loading loading-spinner loading-lg text-primary"></span>
                    </div>
                )}

                <div className="card-body bg-white">
                    {/* Profile Completion Title */}
                    <h2 className="card-title text-2xl text-dark-purple font-bold text-center">Complete Your Profile</h2>
                    <p className="text-base-60 pb-6">
                        Please provide your additional information to complete your profile
                    </p>
                    {/* Error Alert */}
                    {error && (
                        <div className="alert alert-error shadow-lg mb-4">
                            <span>{error}</span>
                        </div>
                    )}

                    {/* Profile Form */}
                    <form onSubmit={handleSubmit} className="space-y-4">
                        {/* Phone Number Input */}
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
                        <DateInput
                            type="date"
                            label="Birth Date"
                            name="birth_date"
                            value={birthDate}
                            onChange={(e) => setBirthDate(e.target.value)}
                            required={true}
                        />
                        </div>
                        {/* Submit Button */}
                        <button type="submit" className="btn btn-dark-purple w-full" disabled={isLoading}>
                            {isLoading ? "Updating..." : "Save Profile"}
                        </button>
                    </form>
                </div>
            </div>
        </div>
    );
}

export default CompleteProfile;