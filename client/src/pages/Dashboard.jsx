import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { FaStar, FaBook, FaChartLine, FaUsers, FaCalendar, FaGraduationCap, FaEdit, FaTrash } from 'react-icons/fa';
import { getDashboardData, deleteReview, getProfessor } from '../services/api';
import { useAuth } from '../context/AuthContext';
import EditReviewModal from '../components/EditReviewModal';

export default function Dashboard() {
  const { user } = useAuth();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [editingReview, setEditingReview] = useState(null);
  const [editProfessor, setEditProfessor] = useState(null);
  const [deleteLoading, setDeleteLoading] = useState(null);

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      setLoading(true);
      const response = await getDashboardData();
      setData(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load dashboard');
    } finally {
      setLoading(false);
    }
  };

  const handleEditClick = async (review) => {
    try {
      const profResponse = await getProfessor(review.professor_id);
      setEditProfessor(profResponse.data);
      setEditingReview(review);
    } catch (err) {
      console.error('Failed to load professor:', err);
    }
  };

  const handleDeleteClick = async (reviewId) => {
    if (!confirm('Are you sure you want to delete this review? This action cannot be undone.')) {
      return;
    }

    setDeleteLoading(reviewId);
    try {
      await deleteReview(reviewId);
      loadDashboard(); // Refresh dashboard
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Failed to delete review';
      alert(errorMsg);
    } finally {
      setDeleteLoading(null);
    }
  };

  const isSemesterEnded = (semester) => {
    try {
      const [season, yearStr] = semester.split(' ');
      const year = parseInt(yearStr);
      const now = new Date();
      const currentYear = now.getFullYear();
      const currentMonth = now.getMonth() + 1;

      const semesterEnds = {
        'Spring': 5,
        'Summer': 8,
        'Fall': 12,
        'Winter': 2
      };

      const endMonth = semesterEnds[season];
      if (!endMonth) return true;

      if (year < currentYear) return true;
      if (year === currentYear && currentMonth > endMonth) return true;
      return false;
    } catch {
      return true;
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <p className="text-red-600 mb-4">{error}</p>
          <button
            onClick={loadDashboard}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  const { stats, recent_reviews, followed_professors } = data;

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600 mt-1">Welcome back, {user?.email?.split('@')[0]}</p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <StatCard
            icon={FaBook}
            label="Total Reviews"
            value={stats.total_reviews}
            bgColor="bg-blue-50"
            iconColor="text-blue-600"
          />
          <StatCard
            icon={FaStar}
            label="Avg Rating Given"
            value={stats.avg_rating_given.toFixed(1)}
            bgColor="bg-yellow-50"
            iconColor="text-yellow-600"
          />
          <StatCard
            icon={FaUsers}
            label="Following"
            value={stats.total_professors_followed}
            bgColor="bg-green-50"
            iconColor="text-green-600"
          />
          <StatCard
            icon={FaGraduationCap}
            label="Top Department"
            value={stats.most_reviewed_department || 'N/A'}
            isText
            bgColor="bg-purple-50"
            iconColor="text-purple-600"
          />
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* My Reviews */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg border border-gray-200 shadow-sm">
              <div className="p-6 border-b border-gray-200">
                <h2 className="text-xl font-semibold text-gray-900">My Reviews</h2>
                <p className="text-sm text-gray-500 mt-1">{stats.total_reviews} total reviews</p>
              </div>
              <div className="divide-y divide-gray-100">
                {recent_reviews.length === 0 ? (
                  <div className="p-12 text-center">
                    <FaBook className="text-4xl text-gray-300 mx-auto mb-3" />
                    <p className="text-gray-500">No reviews yet</p>
                    <p className="text-sm text-gray-400 mt-1">Start reviewing professors to see them here</p>
                  </div>
                ) : (
                  recent_reviews.map((review) => (
                    <ReviewItem 
                      key={review.id} 
                      review={review} 
                      onEdit={handleEditClick}
                      onDelete={handleDeleteClick}
                      deleteLoading={deleteLoading === review.id}
                      canEdit={!isSemesterEnded(review.semester)}
                    />
                  ))
                )}
              </div>
            </div>
          </div>

          {/* Followed Professors */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg border border-gray-200 shadow-sm">
              <div className="p-6 border-b border-gray-200">
                <h2 className="text-xl font-semibold text-gray-900">Following</h2>
                <p className="text-sm text-gray-500 mt-1">{stats.total_professors_followed} professors</p>
              </div>
              <div className="divide-y divide-gray-100">
                {followed_professors.length === 0 ? (
                  <div className="p-12 text-center">
                    <FaUsers className="text-4xl text-gray-300 mx-auto mb-3" />
                    <p className="text-gray-500">Not following anyone</p>
                    <p className="text-sm text-gray-400 mt-1">Follow professors to track their ratings</p>
                  </div>
                ) : (
                  followed_professors.map((professor) => (
                    <FollowedProfessorItem key={professor.id} professor={professor} />
                  ))
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
      
      {/* Edit Review Modal */}
      {editingReview && editProfessor && (
        <EditReviewModal
          review={editingReview}
          professor={editProfessor}
          onClose={() => {
            setEditingReview(null);
            setEditProfessor(null);
          }}
          onReviewUpdated={() => {
            loadDashboard();
            setEditingReview(null);
            setEditProfessor(null);
          }}
        />
      )}
    </div>
  );
}

function StatCard({ icon: Icon, label, value, isText = false, bgColor, iconColor }) {
  return (
    <div className="bg-white rounded-lg border border-gray-200 shadow-sm p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-600 mb-1">{label}</p>
          <p className={`${isText ? 'text-xl' : 'text-3xl'} font-bold text-gray-900`}>
            {value}
          </p>
        </div>
        <div className={`${bgColor} p-3 rounded-lg`}>
          <Icon className={`text-2xl ${iconColor}`} />
        </div>
      </div>
    </div>
  );
}

function ReviewItem({ review, onEdit, onDelete, deleteLoading, canEdit }) {
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
  };

  return (
    <div className="p-6 hover:bg-gray-50 transition">
      <div className="flex items-start justify-between">
        <Link
          to={`/professor/${review.professor_id}`}
          className="flex-1"
        >
          <h3 className="font-semibold text-gray-900 mb-1 hover:text-blue-600">{review.professor_name}</h3>
          <p className="text-sm text-gray-500 mb-2">{review.professor_department}</p>
          
          <div className="flex items-center gap-4 text-sm mb-2">
            <div className="flex items-center gap-1">
              <FaStar className="text-yellow-400" />
              <span className="font-medium">{review.rating_quality}/5</span>
            </div>
            <div className="flex items-center gap-1">
              <FaChartLine className="text-gray-400" />
              <span>Difficulty: {review.rating_difficulty}/5</span>
            </div>
            <div className="flex items-center gap-1">
              <FaBook className="text-gray-400" />
              <span>Grade: {review.grade_received}</span>
            </div>
          </div>

          {review.comment && (
            <p className="text-sm text-gray-600 line-clamp-2">{review.comment}</p>
          )}
        </Link>
        
        <div className="ml-4 flex flex-col items-end gap-2">
          <div className="flex items-center gap-1 text-xs text-gray-500">
            <FaCalendar />
            <span>{formatDate(review.created_at)}</span>
          </div>
          {review.course_code && (
            <span className="inline-block px-2 py-1 bg-gray-100 text-xs font-medium text-gray-700 rounded">
              {review.course_code}
            </span>
          )}
          
          {/* Edit/Delete Buttons */}
          <div className="flex items-center gap-2 mt-2">
            {canEdit ? (
              <>
                <button
                  onClick={() => onEdit(review)}
                  className="flex items-center gap-1 px-2 py-1 text-xs text-blue-600 hover:bg-blue-50 rounded transition"
                  title="Edit review"
                >
                  <FaEdit />
                  <span>Edit</span>
                </button>
                <button
                  onClick={() => onDelete(review.id)}
                  disabled={deleteLoading}
                  className="flex items-center gap-1 px-2 py-1 text-xs text-red-600 hover:bg-red-50 rounded transition disabled:opacity-50"
                  title="Delete review"
                >
                  <FaTrash />
                  <span>{deleteLoading ? 'Deleting...' : 'Delete'}</span>
                </button>
              </>
            ) : (
              <span className="text-xs text-gray-400 italic">Semester ended - locked</span>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

function FollowedProfessorItem({ professor }) {
  return (
    <Link
      to={`/professor/${professor.id}`}
      className="block p-4 hover:bg-gray-50 transition"
    >
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <h3 className="font-medium text-gray-900">{professor.name}</h3>
          <p className="text-xs text-gray-500 mt-1">{professor.department}</p>
        </div>
        <div className="text-right">
          <div className="flex items-center gap-1 mb-1">
            <FaStar className="text-yellow-400 text-sm" />
            <span className="text-sm font-semibold text-gray-900">
              {professor.avg_rating.toFixed(1)}
            </span>
          </div>
          <p className="text-xs text-gray-500">{professor.total_reviews} reviews</p>
        </div>
      </div>
    </Link>
  );
}
