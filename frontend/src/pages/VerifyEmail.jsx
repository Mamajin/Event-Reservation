import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import api from '../api'; // Replace with your API configuration

const EmailVerification = () => {
    const { user_id, token } = useParams();
    const [status, setStatus] = useState('loading');
    const [email, setEmail] = useState('');
    const [resendStatus, setResendStatus] = useState(null); // 'success', 'error', or null

    useEffect(() => {
        const verifyEmail = async () => {
            try {
                const response = await api.get(`/users/verify-email/${user_id}/${token}/`);
                if (response.status === 200) {
                    setStatus('success');
                } else {
                    setStatus('error');
                }
            } catch (error) {
                console.error('Verification failed:', error);
                setStatus('error');
            }
        };

        verifyEmail();
    }, [user_id, token]);

    const handleResendVerification = async (e) => {
        e.preventDefault();
        try {
            const response = await api.post(`/users/resend-verification/`, { email });
            if (response.status === 200) {
                setResendStatus('success');
            } else {
                setResendStatus('error');
            }
        } catch (error) {
            console.error('Resend verification failed:', error);
            setResendStatus('error');
        }
    };

    if (status === 'loading') {
        return (
            <div className="flex justify-center items-center h-screen">
                <div className="text-center">
                    <p className="text-lg font-semibold">Verifying your email...</p>
                    <progress className="progress w-56"></progress>
                </div>
            </div>
        );
    }

    if (status === 'success') {
        return (
            <div className="flex justify-center items-center h-screen">
                <div className="card shadow-lg p-8 bg-green-100 text-green-800">
                    <h1 className="text-2xl font-bold">Email Verified!</h1>
                    <p className="my-4">Your email has been successfully verified. You can now log in to your account.</p>
                    <a href="/login" className="bg-black text-white hover:bg-white hover:text-black btn btn-primary">
                        Login
                    </a>
                </div>
            </div>
        );
    }

    return (
        <div className="flex justify-center items-center h-screen">
            <div className="card shadow-lg p-8 bg-red-100 text-red-800 w-full max-w-md">
                <h1 className="text-2xl font-bold mb-4">Email Verification Failed</h1>
                <p className="mb-4">
                    The verification link may have expired. Please try resending the verification email.
                </p>
                <form onSubmit={handleResendVerification}>
                    <div className="form-control mb-4">
                        <label className="label" htmlFor="email">
                            <span className="label-text">Email Address</span>
                        </label>
                        <input
                            type="email"
                            id="email"
                            className="input input-bordered w-full"
                            placeholder="Enter your email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                        />
                    </div>
                    <button type="submit" className="bg-black text-white hover:bg-white hover:text-black btn btn-error w-full">
                        Resend Verification Email
                    </button>
                </form>
                {resendStatus === 'success' && (
                    <p className="text-green-500 mt-4">Verification email has been resent successfully.</p>
                )}
                {resendStatus === 'error' && (
                    <p className="text-red-500 mt-4">Failed to resend verification email. Please try again.</p>
                )}
            </div>
        </div>
    );
};

export default EmailVerification;
