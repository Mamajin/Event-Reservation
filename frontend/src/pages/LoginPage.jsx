import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import api from "../api";
import { GoogleLogin } from '@react-oauth/google';
import { ACCESS_TOKEN, REFRESH_TOKEN,USER_NAME,USER_STATUS, PROFILE_PICTURE, USER_ID} from "../constants";
import "../style/index.css";
import qs from "qs";

function Login() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const navigate = useNavigate();

    const handleGoogleSuccess = async (credentialResponse) => {
        try {
            setIsLoading(true);
            const authResponse = await api.post('users/auth/google', {
                token: credentialResponse.credential
            });

            // Store tokens in localStorage
            localStorage.setItem(PROFILE_PICTURE, authResponse.data.picture);
            localStorage.setItem(ACCESS_TOKEN, authResponse.data.access_token);
            localStorage.setItem(REFRESH_TOKEN, authResponse.data.refresh_token);
            localStorage.setItem(USER_STATUS, authResponse.data.status);
            localStorage.setItem(USER_NAME, authResponse.data.username);
            localStorage.setItem(USER_ID, authResponse.data.id);
            console.log(authResponse.data.picture)
            // Navigate to the dashboard or home after successful login
            navigate("/");
        } catch (error) {
            console.error('Authentication Error:', error);
            setError(
                error.response?.data?.detail || 
                'Authentication failed. Please try again.'
            );
        } finally {
            setIsLoading(false);
        }
    };
    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);

        try {
            const payload = { username, password };
            const formData = qs.stringify(payload);
            const res = await api.post("/users/login", formData, {
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
            });
            const token = await api.post("/token/pair", payload, {
                headers: {
                    'Content-Type': 'application/json',
                }});
            localStorage.setItem(PROFILE_PICTURE, res.data.image_url);
            localStorage.setItem(ACCESS_TOKEN, res.data.access_token);
            localStorage.setItem(REFRESH_TOKEN, res.data.refresh_token);
            localStorage.setItem(USER_NAME, res.data.username);
            localStorage.setItem(USER_STATUS, res.data.status);
            localStorage.setItem(USER_ID, res.data.id);
            navigate("/");
        } catch (error) {
            console.error("Login error:", error);
            let errorMessage = "Login failed. Please try again.";
            if (error.response) {
                errorMessage = error.response.data.error || errorMessage; // Adjust this to look for "error"
            }
    
            alert(errorMessage); // Show the alert with error message
        } finally {
            setIsLoading(false); // Reset loading state
        }
    };
    return (
        <div className="min-h-screen bg-white flex flex-col items-center justify-center p-4">
            <div className="card w-full max-w-md bg-base-100 shadow-xl relative">
                {isLoading && (
                    <div className="absolute inset-0 bg-base-100/50 backdrop-blur-sm flex items-center justify-center z-50 rounded-2xl">
                        <span className="loading loading-spinner loading-lg text-primary"></span>
                    </div>
                )}

                <div className="card-body bg-white">
                    {/* Logo Section */}
                    <div className="flex flex-col items-center gap-2 mb-4">
                        <div className="avatar">
                        </div>
                        <h2 className="card-title text-2xl text-dark-purple font-bold">Welcome Back!</h2>
                        <p className="text-base-content/90 text-center">
                            Sign in to access your account
                        </p>
                    </div>

                    {/* Error Alert */}
                    {error && (
                        <div className="alert alert-error shadow-lg mb-4">
                            <svg xmlns="http://www.w3.org/2000/svg" className="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            <span>{error}</span>
                            <button 
                                className="btn btn-ghost btn-xs"
                                onClick={() => setError('')}
                            >
                                ✕
                            </button>
                        </div>
                    )}

                    {/* Sign In Options */}
                    <div className="space-y-4">
                        {/* Email Input */}
                        <div className="form-control">
                            <input 
                                type="email" 
                                placeholder="Username" 
                                className="input bg-white input-bordered" 
                                onChange={(e) => setUsername(e.target.value)}
                                
                            />
                        </div>

                        {/* Password Input */}
                        <div className="form-control">
                            <input 
                                type="password" 
                                placeholder="Password" 
                                className="input bg-white input-bordered" 
                                onChange={(e) => setPassword(e.target.value)}
                            />
                            <label className="label">
                                <a href="#" className="label-text-alt link link-hover">
                                    Forgot password?
                                </a>
                            </label>
                        </div>

                        {/* Login Button */}
                        <button className="btn btn-dark-purple w-full" onClick={handleSubmit}>
                            Login
                        </button>

                        {/* Divider */}
                        <div className="divider">OR</div>

                        {/* Google Sign In Button */}
                        <div className="relative">
                            <GoogleLogin
                                onSuccess={handleGoogleSuccess}
                                onError={() => {
                                    setError('Google Sign In was unsuccessful. Please try again.');
                                }}
                                useOneTap
                                theme="bg-white"
                                shape="circle"
                                size="large"
                            />
                        </div>

                        {/* Sign Up Link */}
                        <p className="text-center text-sm">
                            Don't have an account?{' '}
                            <Link to="/register"  className="link link-dark-purple">
                                Sign up
                            </Link>
                        </p>
                    </div>
                </div>
            </div>

            {/* Success Toast (optional display on login success) */}
            <div id="success-toast" className="toast toast-end hidden">
                <div className="alert alert-success">
                    <span>Successfully logged in!</span>
                </div>
            </div>
        </div>
    );
}

export default Login;
