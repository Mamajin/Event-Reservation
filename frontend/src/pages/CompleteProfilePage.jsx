import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";
import { ACCESS_TOKEN, USER_ID } from "../constants";

function CompleteProfile() {
    const [phoneNumber, setPhoneNumber] = useState("");
    const [birthDate, setBirthDate] = useState("");
    const [address, setAddress] = useState("");
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
        } finally {
            setIsLoading(false);
        }
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