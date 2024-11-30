import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { LuHome, LuRefreshCw } from 'react-icons/lu';

const NotFound = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100 flex items-center justify-center p-4">
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="max-w-md w-full bg-gray-70 rounded-2xl shadow-lg p-8 text-center border-none shadow-none"
      >
        <motion.div
          animate={{ 
            rotate: [0, 10, -10, 10, 0],
            scale: [1, 1.1, 1]
          }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="text-6xl font-bold text-gray-900 mb-4"
        >
          404
        </motion.div>
        
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
        >
        <h1 className="text-2xl font-semibold text-gray-800 mb-4">Page Not Found</h1>
        <p className="text-gray-600 mb-6">
        The page might have been moved or the link was incorrect. Don't worry, you're just a click away from home.
        </p>

          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => navigate('/')}
              className="flex items-center justify-center gap-2 px-6 py-3 bg-dark-purple text-white rounded-lg font-medium transition-colors duration-200 hover:text-gray-800 hover:bg-gray-200"
            >
              <LuHome size={20} />
              Go Home
            </motion.button>
            
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => window.location.reload()}
              className="flex items-center justify-center gap-2 px-6 py-3 bg-gray-200 text-gray-800 rounded-lg font-medium transition-colors hover:bg-gray-300"
            >
              <LuRefreshCw size={20} />
              Refresh Page
            </motion.button>
          </div>
        </motion.div>
      </motion.div>
    </div>
  );
};

export default NotFound;
