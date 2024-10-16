import { useState } from "react";
import api from "../api";
import { useNavigate } from "react-router-dom";
import { ACCESS_TOKEN, REFRESH_TOKEN, USER_NAME} from "../constants";
import qs from "qs"
import "../style/Form.css";

function Form({ route, method }) {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [password2, setPassword2] = useState(""); // Second password state
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const name = method === "login" ? "Login" : "Register";

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        // Check if passwords match
        if (method === "register" && password !== password2) {
            alert("Passwords do not match!"); // Alert user if passwords don't match
            setLoading(false); // Reset loading state
            return; // Exit the function early
        }

        try {
            const payload = { username, password };
            if (method === "register") {
                payload.password2 = password2; // Include password2 only for registration
            }
            const formData = qs.stringify(payload);
            const res = await api.post(route, formData,{
               headers:{"Content-Type": "application/x-www-form-urlencoded"
               },     
            }); // Make API call
            if (method === "login") {
                localStorage.setItem(ACCESS_TOKEN, res.data.access_token); // Store access token
                localStorage.setItem(REFRESH_TOKEN, res.data.refresh_token); // Store refresh token
                localStorage.setItem(USER_NAME, res.data.username); // Store username
                navigate("/");
            } else {
                navigate("/login");
            }
        } catch (error) {
            let errorMessage;
    
            // Check if the error response exists
            if (error.response) {
                // Get the specific status and detail from the error response
                const status = error.response.status;
                const data = error.response.data;
    
                // Provide specific messages based on status codes
                switch (status) {
                    case 400: // Bad Request
                        if (data.detail) {
                            errorMessage = data.detail; // Use the specific detail message
                        } else {
                            errorMessage = "There was an issue with your registration. Please check your inputs.";
                        }
                        break;
                    case 409: // Conflict
                        if (data.detail && data.detail.includes("unique constraint")) {
                            errorMessage = "This username is already taken. Please choose a different one."; // Message for already taken username
                        } else {
                            errorMessage = "There was a conflict with your request. Please try again.";
                        }
                        break;
                    case 500: // Internal Server Error
                        errorMessage = "Server error. Please try again later.";
                        break;
                    default:
                        errorMessage = "An unexpected error occurred. Please try again.";
                        break;
                }
            } else {
                errorMessage = "Network error. Please check your connection and try again.";
            }
    
            alert(errorMessage); // Show the appropriate error message
        } finally {
            setLoading(false); // Reset loading state
        }
    }

    return (
        <form onSubmit={handleSubmit} className="form-container">
            <h1>{name}</h1>
            <input
                className="form-input"
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Username"
            />
            <input
                className="form-input"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Password"
                required
            />
            {/* Second password input for verification */}
            {method === "register" && (
                <input
                    className="form-input"
                    type="password"
                    value={password2}
                    onChange={(e) => setPassword2(e.target.value)}
                    placeholder="Confirm Password"
                    required
                />
            )}
            <button className="form-button" type="submit" disabled={loading}>
                {name}
            </button>
        </form>
    );
}

export default Form;
