import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../api";
import { ACCESS_TOKEN, REFRESH_TOKEN, USER_NAME } from "../constants";
import qs from "qs";
import "../style/index.css";

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
        <div className="flex items-center justify-center min-h-screen bg-gradient-to-r from-red-500 to-purple-600">
            <div className="max-w-md w-full bg-white shadow-lg rounded-lg p-8 space-y-6">
                <h1 className="text-3xl font-bold text-center text-gray-700">Login</h1>
                <form onSubmit={handleSubmit} className="space-y-4">
                    <input
                        className="input w-full p-4 border bg-white border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-200"
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        placeholder="Username"
                        required
                    />
                    <input
                        className="input w-full p-4 bg-white border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 transition duration-200"
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="Password"
                        required
                    />
                    <button
                        className={`btn w-full p-4 rounded-lg text-white font-semibold transition duration-200 
                        ${loading ? "bg-pink-400 cursor-not-allowed" : "bg-blue-600 hover:bg-blue-700"}`}
                        type="submit"
                        disabled={loading}
                    >
                        {loading ? "Loading..." : "Login"}
                    </button>
                </form>
                <div className="text-center">
                    <Link to="/register" className="text-blue-600 hover:underline">Don't have an account? Sign up</Link>
                </div>
            </div>
        </div>
    );
}

export default LoginForm;
