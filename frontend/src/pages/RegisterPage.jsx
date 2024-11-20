import { useState } from "react";
import api from "../api";
import { useNavigate } from "react-router-dom";
import qs from "qs";

export default function Register() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [password2, setPassword2] = useState("");
    const [firstName, setFirstName] = useState("");
    const [lastName, setLastName] = useState("");
    const [birthDate, setBirthDate] = useState("");
    const [phoneNumber, setPhoneNumber] = useState("");
    const [email, setEmail] = useState("");
    const [loading, setLoading] = useState(false);
    const [currentStep, setCurrentStep] = useState(1);
    const navigate = useNavigate();

    const totalSteps = 3; // Number of steps in the form

    const handleNext = () => {
        if (currentStep < totalSteps) {
            setCurrentStep(currentStep + 1);
        }
    };

    const handlePrevious = () => {
        if (currentStep > 1) {
            setCurrentStep(currentStep - 1);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        try {
            const payload = {
                username,
                password,
                password2,
                first_name: firstName,
                last_name: lastName,
                birth_date: birthDate,
                phone_number: phoneNumber,
                email,
            };

            const formData = qs.stringify(payload);
            await api.post("/users/register", formData, {
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
            });

            navigate("/login");
        } catch (error) {
            console.error("Registration error:", error);
            let errorMessage = "An error occurred during registration.";
            if (error.response) {
                errorMessage = error.response.data.error || errorMessage;
            }
            alert(errorMessage);
            setLoading(false);
        }
    };

    return (
        <div className="flex items-center justify-center min-h-screen bg-gradient-to-r from-purple-500 to-blue-600">
            <div className="max-w-md w-full bg-white shadow-lg rounded-lg p-8 space-y-6">
                <div className="mb-4">
                    <progress
                        className="progress progress-primary w-full"
                        value={(currentStep / totalSteps) * 100}
                        max="100"
                    ></progress>
                </div>

                <form onSubmit={handleSubmit}>
                    {currentStep === 1 && (
                        <div>
                            <h2 className="text-2xl font-bold mb-4 text-center text-dark-purple">Step 1: Account Info</h2>
                            <input
                                className="input bg-white input-bordered w-full mb-3"
                                type="text"
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                                placeholder="Username"
                                required
                            />
                            <input
                                className="input bg-white input-bordered w-full mb-3"
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                placeholder="Password"
                                required
                            />
                            <input
                                className="input bg-white input-bordered w-full mb-3"
                                type="password"
                                value={password2}
                                onChange={(e) => setPassword2(e.target.value)}
                                placeholder="Confirm Password"
                                required
                            />
                        </div>
                    )}

                    {currentStep === 2 && (
                        <div>
                            <h2 className="text-2xl font-bold mb-4 text-center text-dark-purple">Step 2: Personal Info</h2>
                            <input
                                className="input bg-white input-bordered w-full mb-3"
                                type="text"
                                value={firstName}
                                onChange={(e) => setFirstName(e.target.value)}
                                placeholder="First Name"
                                required
                            />
                            <input
                                className="input bg-white input-bordered w-full mb-3"
                                type="text"
                                value={lastName}
                                onChange={(e) => setLastName(e.target.value)}
                                placeholder="Last Name"
                                required
                            />
                            <input
                                className="input bg-white input-bordered w-full mb-3"
                                type="date"
                                value={birthDate}
                                onChange={(e) => setBirthDate(e.target.value)}
                                placeholder="Birth Date"
                                required
                            />
                        </div>
                    )}

                    {currentStep === 3 && (
                        <div>
                            <h2 className="text-2xl font-bold mb-4 text-center text-dark-purple">Step 3: Contact Info</h2>
                            <input
                                className="input bg-white input-bordered w-full mb-3"
                                type="text"
                                value={phoneNumber}
                                onChange={(e) => setPhoneNumber(e.target.value)}
                                placeholder="Phone Number"
                                required
                            />
                            <input
                                className="input bg-white input-bordered w-full mb-3"
                                type="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                placeholder="Email"
                                required
                            />
                        </div>
                    )}

                    <div className="flex justify-between mt-4">
                        <button
                            type="button"
                            className={`btn bg-dark-purple text-amber-300 ${currentStep === 1 ? "invisible" : ""}`}
                            onClick={handlePrevious}
                        >
                            Previous
                        </button>

                        {currentStep < totalSteps ? (
                            <button
                                type="button"
                                className="btn bg-amber-300 text-dark-purple"
                                onClick={handleNext}
                            >
                                Next
                            </button>
                        ) : (
                            <button
                                type="submit"
                                className={`btn bg-amber-300 text-dark-purple ${loading ? "loading" : ""}`}
                                disabled={loading}
                            >
                                {loading ? 'Submitting...' : 'Submit'}
                            </button>
                        )}
                    </div>
                </form>
            </div>
        </div>
    );
}
