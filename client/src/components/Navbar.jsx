import { Link } from 'react-router-dom';
import { FaGraduationCap, FaSearch, FaUser, FaSignOutAlt } from 'react-icons/fa';
import { useAuth } from '../context/AuthContext';

export default function Navbar() {
  const { isAuthenticated, user, logout } = useAuth();

  return (
    <nav className="bg-white shadow-sm border-b border-gray-100 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2">
            <div className="bg-blue-600 p-2 rounded-lg">
              <FaGraduationCap className="text-white text-xl" />
            </div>
            <span className="text-xl font-bold text-gray-800">ProfReview</span>
          </Link>

          {/* Search Bar */}
          <div className="hidden md:flex flex-1 max-w-md mx-8">
            <div className="relative w-full">
              <FaSearch className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
              <input
                type="text"
                placeholder="Search professors, departments..."
                className="w-full pl-10 pr-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white transition"
              />
            </div>
          </div>

          {/* Nav Links */}
          <div className="flex items-center gap-4">
            <Link 
              to="/" 
              className="text-gray-600 hover:text-blue-600 font-medium transition"
            >
              Home
            </Link>
            
            {isAuthenticated ? (
              <>
                {/* Dashboard Link - Different for Student vs Professor */}
                {user?.role === 'professor' ? (
                  <Link 
                    to="/professor-dashboard" 
                    className="text-gray-600 hover:text-blue-600 font-medium transition"
                  >
                    My Dashboard
                  </Link>
                ) : (
                  <Link 
                    to="/dashboard" 
                    className="text-gray-600 hover:text-blue-600 font-medium transition"
                  >
                    My Dashboard
                  </Link>
                )}
                
                {/* User Info with Role Badge */}
                <div className="flex items-center gap-2 px-3 py-2 bg-gray-50 rounded-lg">
                  <FaUser className="text-blue-600" />
                  <div className="flex flex-col">
                    <span className="text-sm font-medium text-gray-700">
                      {user?.email?.split('@')[0]}
                    </span>
                    {user?.role === 'professor' && (
                      <span className="text-xs text-blue-600 font-medium">Professor</span>
                    )}
                  </div>
                </div>
                
                {/* Logout Button */}
                <button
                  onClick={logout}
                  className="flex items-center gap-2 px-4 py-2 text-gray-600 hover:text-red-600 hover:bg-red-50 rounded-lg transition"
                  title="Logout"
                >
                  <FaSignOutAlt />
                  <span className="hidden sm:inline">Logout</span>
                </button>
              </>
            ) : (
              <>
                <Link 
                  to="/login" 
                  className="text-gray-600 hover:text-blue-600 font-medium transition"
                >
                  Login
                </Link>
                <Link 
                  to="/signup" 
                  className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition"
                >
                  <FaUser className="text-sm" />
                  <span>Sign Up</span>
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}

