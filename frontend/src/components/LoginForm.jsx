import { useState } from "react";
import api from "../api";
import { useNavigate } from "react-router-dom";
import { ACCESS_TOKEN, REFRESH_TOKEN, USER_NAME } from "../constants";
import qs from "qs";
import "../style/index.css"

function LoginForm() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        try {
            const payload = { username, password };
            const formData = qs.stringify(payload);
            const res = await api.post("/users/login", formData, {
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
            });

            localStorage.setItem(ACCESS_TOKEN, res.data.access_token);
            localStorage.setItem(REFRESH_TOKEN, res.data.refresh_token);
            localStorage.setItem(USER_NAME, res.data.username);
            navigate("/");
        } catch (error) {
            alert("An error occurred during login.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-md mx-auto p-6 bg-white shadow-md rounded-md">
            <h1 className="text-2xl font-bold mb-4 text-center">Login</h1>
            <form onSubmit={handleSubmit}>
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
                <button
                    className={`w-full p-2 rounded bg-blue-500 text-white font-semibold ${loading ? "opacity-50 cursor-not-allowed" : "hover:bg-blue-600"}`}
                    type="submit"
                    disabled={loading}
                >
                    {loading ? "Loading..." : "Login"}
                </button>
            </form>
        </div>
    );
}

export default LoginForm;