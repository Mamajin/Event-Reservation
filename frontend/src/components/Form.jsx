import { useState } from "react";
import api from "../api";
import { useNavigate } from "react-router-dom";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants";
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

            const res = await api.post(route, payload); // Make API call
            if (method === "login") {
                localStorage.setItem(ACCESS_TOKEN, res.data.access); // Store access token
                localStorage.setItem(REFRESH_TOKEN, res.data.refresh); // Store refresh token
                navigate("/");
            } else {
                navigate("/login");
            }
        } catch (error) {
            alert(error.response?.data?.detail || "An error occurred");
        } finally {
            setLoading(false); // Reset loading state
        }
    };

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
            <button className="form-button" type="submit" disabled={loading}> // Prevents Duplicate Submissions
                {name}
            </button>
        </form>
    );
}

export default Form;
