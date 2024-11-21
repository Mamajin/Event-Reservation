import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';

const Logout = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const handleLogout = async () => {
        try {
          await api.post('/users/logout');
          localStorage.clear();
          navigate("/login");
        } catch (error) {
          console.error("Logout failed:", error);
        }
      };

    handleLogout();
  }, [navigate]);


};

export default Logout;
