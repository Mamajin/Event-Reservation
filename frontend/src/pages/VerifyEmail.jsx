// import React, { useEffect, useState } from 'react';
// import PageLayout from '../components/PageLayout';
// import { useNavigate } from 'react-router-dom';
// import EventCard from '../components/EventCard';
// import { ACCESS_TOKEN } from "../constants";
// import useUserProfile from '../hooks/useUserProfile';
// import api from '../api';

// function VerifyEmail() {
//     const [loading, setLoading] = useState(true);
//     const [error, setError] = useState(null);
//     const navigate = useNavigate();
//     const { userId, loading: userLoading, error: userError } = useUserProfile(navigate);

//     useEffect(() => {
//         const fetchUserData = async () => {
//             try {
//                 console.log('Fetching bookmarked events...');
//                 const token = localStorage.getItem(ACCESS_TOKEN);
//                 if (!token || !userId) {
//                     throw new Error('No access token or user ID found');
//                 }
//             } catch (err) {
//                 console.error('Error fetching bookmarked events:', err);
//                 setError(err);
//             } finally {
//                 setLoading(false);
//             }
//         };

//     }, [navigate, userId, userLoading]);

//     if (loading || userLoading) {
//         return (
//             <PageLayout>
//             <div className="text-center mt-8">Loading your Vef...</div>
//             <div className="flex justify-center items-center h-screen -mt-24">
//                 <span className="loading loading-spinner loading-lg"></span>
//             </div>
//           </PageLayout>
//         );
//     }

//     if (error || userError) {
//         return (
//             <PageLayout>
//                 <div className="flex justify-center items-start min-h-screen p-4">
//                     <div className="w-full max-w-[1400px] max-w-lg bg-white rounded-lg shadow-lg p-6 space-y-4">
//                         <h2 className="text-2xl font-bold mb-4 text-center text-dark-purple">Error</h2>
//                         <div className="text-center">
//                             <div>Error fetching bookmarked events: {error?.message || userError?.message}</div>
//                         </div>
//                     </div>
//                 </div>
//             </PageLayout>
//         );
//     }

//     if (events.length === 0) {
//         return (
//             <PageLayout>
//                 <div className="flex justify-center items-start min-h-screen p-4">
//                     <div className="w-full max-w-[1400px] max-w-lg bg-white rounded-lg shadow-lg p-6 space-y-4">
//                         <h2 className="text-2xl font-bold mb-4 text-center text-dark-purple">Bookmarked Events</h2>
//                         <div className="grid grid-cols-1 gap-4">
//                             <div>No bookmarked events available</div>
//                         </div>
//                     </div>
//                 </div>
//             </PageLayout>
//         );
//     }

//     return (
//         <PageLayout>
//             <div className="flex justify-center items-start min-h-screen p-4">
//                 <div className="w-full max-w-[1400px] bg-white rounded-lg shadow-lg p-6 space-y-4">
//                     <h1 className="text-2xl font-bold mb-6 text-center text-dark-purple">Bookmarked Events</h1>
//                     <div className="grid grid-cols-1 gap-4">
//                         {events.map((event) => (
//                             <EventCard key={event.id} event={event} />
//                         ))}
//                     </div>
//                 </div>
//             </div>
//         </PageLayout>
//     );
// }

// export default VerifyEmail;


import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import api from '../api';

const EmailVerification = () => {
    const { user_id, token } = useParams();
    const [status, setStatus] = useState('loading');

    useEffect(() => {
        const verifyEmail = async () => {
            try {
                const response = api.get(`/users/verify-email/${user_id}/${token}/`);
                
                if (response.ok) {
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

    if (status === 'loading') {
        return <p>Verifying your email...</p>;
    }
    if (status === 'success') {
        return <p>Your email has been verified successfully! <a href="/login">Login here</a>.</p>;
    }
    return <p>Verification failed. The link may have expired. <a href="/resend-verification">Resend verification email</a>.</p>;
};

export default EmailVerification;