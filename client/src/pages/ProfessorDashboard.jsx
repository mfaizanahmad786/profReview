import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { FaChartLine, FaStar, FaComments, FaThumbsUp, FaUser, FaCheckCircle, FaClock } from 'react-icons/fa';
import { useAuth } from '../context/AuthContext';
import { getMyClaimStatus, getMyClaimedProfile, getProfessorReviews } from '../services/api';

export default function ProfessorDashboard() {
  const { user } = useAuth();
  const [claimStatus, setClaimStatus] = useState(null);
  const [professor, setProfessor] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      // Get claim status
      const statusRes = await getMyClaimStatus();
      setClaimStatus(statusRes.data);

      // If approved, load professor data
      if (statusRes.data.has_approved && statusRes.data.claimed_professor_id) {
        const [profRes, reviewsRes] = await Promise.all([
          getMyClaimedProfile(),
          getProfessorReviews(statusRes.data.claimed_professor_id)
        ]);
        setProfessor(profRes.data);
        setReviews(reviewsRes.data);
      }
    } catch (err) {
      console.error('Failed to load dashboard data:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  // If claim is pending
  if (claimStatus?.has_pending && !claimStatus?.has_approved) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-4xl mx-auto px-4 py-12">
          <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-8 text-center">
            <FaClock className="text-yellow-500 text-6xl mx-auto mb-4" />
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Claim Request Pending</h2>
            <p className="text-gray-600 mb-6">
              Your profile claim request is being reviewed by an administrator. You'll be notified once it's approved.
            </p>
            <Link 
              to="/"
              className="inline-block px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
            >
              Browse Professors
            </Link>
          </div>
        </div>
      </div>
    );
  }

  // If no claim yet
  if (!claimStatus?.has_approved) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-4xl mx-auto px-4 py-12">
          <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-8 text-center">
            <FaUser className="text-gray-400 text-6xl mx-auto mb-4" />
            <h2 className="text-2xl font-bold text-gray-900 mb-2">No Profile Claimed</h2>
            <p className="text-gray-600 mb-6">
              To access your professor dashboard, you need to claim your profile first. Search for your name and submit a claim request.
            </p>
            <Link 
              to="/"
              className="inline-block px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
            >
              Search for Your Profile
            </Link>
          </div>
        </div>
      </div>
    );
  }

  // Dashboard with approved claim
  const totalHelpfulVotes = reviews.reduce((sum, review) => sum + (review.helpful_count || 0), 0);
  const averageRating = professor?.avg_rating || 0;
  const totalReviews = reviews.length;

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Professor Dashboard</h1>
              <p className="text-gray-600 mt-1">Welcome back, {professor?.name}</p>
            </div>
            <div className="flex items-center gap-2 px-4 py-2 bg-green-50 border border-green-200 rounded-lg">
              <FaCheckCircle className="text-green-600" />
              <span className="text-green-900 font-medium">Profile Verified</span>
            </div>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
            <div className="flex items-center justify-between mb-2">
              <FaComments className="text-blue-600 text-2xl" />
            </div>
            <div className="text-3xl font-bold text-gray-900">{totalReviews}</div>
            <div className="text-sm text-gray-600">Total Reviews</div>
          </div>

          <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
            <div className="flex items-center justify-between mb-2">
              <FaStar className="text-yellow-500 text-2xl" />
            </div>
            <div className="text-3xl font-bold text-gray-900">{averageRating.toFixed(1)}</div>
            <div className="text-sm text-gray-600">Average Rating</div>
          </div>

          <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
            <div className="flex items-center justify-between mb-2">
              <FaThumbsUp className="text-green-600 text-2xl" />
            </div>
            <div className="text-3xl font-bold text-gray-900">{totalHelpfulVotes}</div>
            <div className="text-sm text-gray-600">Helpful Votes</div>
          </div>

          <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
            <div className="flex items-center justify-between mb-2">
              <FaChartLine className="text-purple-600 text-2xl" />
            </div>
            <div className="text-3xl font-bold text-gray-900">{professor?.avg_difficulty?.toFixed(1) || 0}</div>
            <div className="text-sm text-gray-600">Avg Difficulty</div>
          </div>
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Recent Reviews */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
              <h2 className="text-xl font-bold text-gray-900 mb-4">Recent Reviews</h2>
              {reviews.length === 0 ? (
                <div className="text-center py-12">
                  <FaComments className="text-gray-300 text-5xl mx-auto mb-4" />
                  <p className="text-gray-500">No reviews yet</p>
                </div>
              ) : (
                <div className="space-y-4">
                  {reviews.slice(0, 5).map((review) => (
                    <div key={review.id} className="border border-gray-100 rounded-lg p-4">
                      <div className="flex items-start justify-between mb-2">
                        <div className="flex items-center gap-2">
                          <div className="flex items-center">
                            {[...Array(5)].map((_, i) => (
                              <FaStar
                                key={i}
                                className={`${
                                  i < review.rating_quality ? 'text-yellow-400' : 'text-gray-200'
                                }`}
                              />
                            ))}
                          </div>
                          <span className="text-sm text-gray-500">
                            {review.course_code} • {review.semester}
                          </span>
                        </div>
                        <div className="flex items-center gap-1 text-sm text-gray-500">
                          <FaThumbsUp className="text-xs" />
                          <span>{review.helpful_count || 0}</span>
                        </div>
                      </div>
                      {review.comment && (
                        <p className="text-gray-700 text-sm">{review.comment}</p>
                      )}
                      <div className="mt-2 text-xs text-gray-500">
                        Grade: <span className="font-semibold text-green-600">{review.grade_received}</span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Profile Info */}
          <div className="space-y-6">
            <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
              <h3 className="font-semibold text-gray-900 mb-4">Profile Information</h3>
              <div className="space-y-3">
                <div>
                  <div className="text-sm text-gray-500">Name</div>
                  <div className="font-medium text-gray-900">{professor?.name}</div>
                </div>
                <div>
                  <div className="text-sm text-gray-500">Department</div>
                  <div className="font-medium text-gray-900">{professor?.department}</div>
                </div>
                <div>
                  <div className="text-sm text-gray-500">Status</div>
                  <div className="flex items-center gap-2">
                    <span className="px-2 py-1 bg-green-100 text-green-800 rounded text-xs font-medium">
                      Verified
                    </span>
                  </div>
                </div>
              </div>
              <div className="mt-6">
                <Link
                  to={`/professor/${claimStatus.claimed_professor_id}`}
                  className="block text-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
                >
                  View Public Profile
                </Link>
              </div>
            </div>

           
          </div>
        </div>
      </div>
    </div>
  );
}
