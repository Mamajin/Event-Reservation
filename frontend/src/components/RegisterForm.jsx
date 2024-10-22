import { useState } from "react";
import api from "../api";
import { useNavigate } from "react-router-dom";
import qs from "qs";

function SignupForm() {
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

        if (password !== password2) {
            alert("Passwords do not match!");
            setLoading(false);
            return;
        }

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
            alert("An error occurred during registration.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-lg mx-auto p-6 bg-white shadow-md rounded-md">
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
                        <h2 className="text-xl font-bold mb-4">Step 1: Account Info</h2>
                        <input
                            className="w-full p-2 mb-3 border border-gray-300 rounded focus:outline-none focus:border-blue-500"
                            type="text"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            placeholder="Username"
                            required
                        />
                        <input
                            className="w-full p-2 mb-3 border border-gray-300 rounded focus:outline-none focus:border-blue-500"
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            placeholder="Password"
                            required
                        />
                        <input
                            className="w-full p-2 mb-3 border border-gray-300 rounded focus:outline-none focus:border-blue-500"
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
                        <h2 className="text-xl font-bold mb-4">Step 2: Personal Info</h2>
                        <input
                            className="w-full p-2 mb-3 border border-gray-300 rounded focus:outline-none focus:border-blue-500"
                            type="text"
                            value={firstName}
                            onChange={(e) => setFirstName(e.target.value)}
                            placeholder="First Name"
                            required
                        />
                        <input
                            className="w-full p-2 mb-3 border border-gray-300 rounded focus:outline-none focus:border-blue-500"
                            type="text"
                            value={lastName}
                            onChange={(e) => setLastName(e.target.value)}
                            placeholder="Last Name"
                            required
                        />
                        <input
                            className="w-full p-2 mb-3 border border-gray-300 rounded focus:outline-none focus:border-blue-500"
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
                        <h2 className="text-xl font-bold mb-4">Step 3: Contact Info</h2>
                        <input
                            className="w-full p-2 mb-3 border border-gray-300 rounded focus:outline-none focus:border-blue-500"
                            type="text"
                            value={phoneNumber}
                            onChange={(e) => setPhoneNumber(e.target.value)}
                            placeholder="Phone Number"
                            required
                        />
                        <input
                            className="w-full p-2 mb-3 border border-gray-300 rounded focus:outline-none focus:border-blue-500"
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
                        className={`btn btn-secondary ${currentStep === 1 ? "invisible" : ""}`}
                        onClick={handlePrevious}
                    >
                        Previous
                    </button>

                    {currentStep < totalSteps ? (
                        <button
                            type="button"
                            className="btn btn-primary"
                            onClick={handleNext}
                        >
                            Next
                        </button>
                    ) : (
                        <button
                            type="submit"
                            className={`btn btn-primary ${loading ? "loading" : ""}`}
                            disabled={loading}
                        >
                            Submit
                        </button>
                    )}
                </div>
            </form>
        </div>
    );
}

export default SignupForm;
