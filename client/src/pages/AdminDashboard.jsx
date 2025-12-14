import { useState, useEffect } from 'react';
import { FaFlag, FaTrash, FaCheckCircle, FaUserTie, FaTimes } from 'react-icons/fa';
import { 
  getFlaggedReviews, 
  deleteReviewAsAdmin, 
  dismissFlags,
  getPendingClaimRequests,
  approveClaimRequest,
  rejectClaimRequest 
} from '../services/api';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

export default function AdminDashboard() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('claims'); // 'claims' or 'flags'
  const [flaggedReviews, setFlaggedReviews] = useState([]);
  const [claimRequests, setClaimRequests] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [actionInProgress, setActionInProgress] = useState(null);

  useEffect(() => {
    // Check if user is admin
    if (!user || user.role !== 'admin') {
      navigate('/');
      return;
    }
    loadData();
  }, [user, navigate]);

  const loadData = async () => {
    setIsLoading(true);
    try {
      await Promise.all([
        loadClaimRequests(),
        loadFlaggedReviews()
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const loadClaimRequests = async () => {
    try {
      const response = await getPendingClaimRequests();
      setClaimRequests(response.data);
    } catch (error) {
      console.error('Error loading claim requests:', error);
      if (error.response?.status === 403) {
        alert('Access denied. Admin privileges required.');
        navigate('/');
      }
    }
  };

  const loadFlaggedReviews = async () => {
    setIsLoading(true);
    try {
      const response = await getFlaggedReviews();
      setFlaggedReviews(response.data);
    } catch (error) {
      console.error('Error loading flagged reviews:', error);
      if (error.response?.status === 403) {
        alert('Access denied. Admin privileges required.');
        navigate('/');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleApproveClaim = async (claimId) => {
    if (!confirm('Are you sure you want to approve this claim request?')) {
      return;
    }

    setActionInProgress(claimId);
    try {
      await approveClaimRequest(claimId);
      setClaimRequests(claimRequests.filter(c => c.id !== claimId));
      alert('Claim request approved successfully!');
    } catch (error) {
      console.error('Error approving claim:', error);
      alert(error.response?.data?.detail || 'Failed to approve claim');
    } finally {
      setActionInProgress(null);
    }
  };

  const handleRejectClaim = async (claimId) => {
    const reason = prompt('Enter reason for rejection (optional):');
    if (reason === null) return; // User cancelled

    setActionInProgress(claimId);
    try {
      await rejectClaimRequest(claimId, reason);
      setClaimRequests(claimRequests.filter(c => c.id !== claimId));
      alert('Claim request rejected');
    } catch (error) {
      console.error('Error rejecting claim:', error);
      alert(error.response?.data?.detail || 'Failed to reject claim');
    } finally {
      setActionInProgress(null);
    }
  };

  const handleDeleteReview = async (reviewId) => {
    if (!confirm('Are you sure you want to permanently delete this review?')) {
      return;
    }

    setActionInProgress(reviewId);
    try {
      await deleteReviewAsAdmin(reviewId);
      setFlaggedReviews(flaggedReviews.filter(r => r.id !== reviewId));
      alert('Review deleted successfully');
    } catch (error) {
      console.error('Error deleting review:', error);
      alert(error.response?.data?.detail || 'Failed to delete review');
    } finally {
      setActionInProgress(null);
    }
  };

  const handleDismissFlags = async (reviewId) => {
    if (!confirm('Are you sure you want to dismiss all flags on this review?')) {
      return;
    }

    setActionInProgress(reviewId);
    try {
      await dismissFlags(reviewId);
      setFlaggedReviews(flaggedReviews.filter(r => r.id !== reviewId));
      alert('Flags dismissed successfully');
    } catch (error) {
      console.error('Error dismissing flags:', error);
      alert(error.response?.data?.detail || 'Failed to dismiss flags');
    } finally {
      setActionInProgress(null);
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-gray-600">Loading admin dashboard...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Admin Dashboard</h1>
          <p className="text-gray-600 mt-2">Manage claim requests and moderate content</p>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center gap-3">
              <FaUserTie className="text-blue-500 text-2xl" />
              <div>
                <h2 className="text-2xl font-bold text-gray-900">{claimRequests.length}</h2>
                <p className="text-gray-600">Pending Claim Requests</p>
              </div>
            </div>
          </div>
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center gap-3">
              <FaFlag className="text-red-500 text-2xl" />
              <div>
                <h2 className="text-2xl font-bold text-gray-900">{flaggedReviews.length}</h2>
                <p className="text-gray-600">Flagged Reviews</p>
              </div>
            </div>
          </div>
        </div>

        {/* Tabs */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 mb-6">
          <div className="flex border-b border-gray-200">
            <button
              onClick={() => setActiveTab('claims')}
              className={`flex-1 px-6 py-4 text-center font-medium transition ${
                activeTab === 'claims'
                  ? 'text-blue-600 border-b-2 border-blue-600 bg-blue-50'
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
              }`}
            >
              <div className="flex items-center justify-center gap-2">
                <FaUserTie />
                <span>Claim Requests ({claimRequests.length})</span>
              </div>
            </button>
            <button
              onClick={() => setActiveTab('flags')}
              className={`flex-1 px-6 py-4 text-center font-medium transition ${
                activeTab === 'flags'
                  ? 'text-blue-600 border-b-2 border-blue-600 bg-blue-50'
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
              }`}
            >
              <div className="flex items-center justify-center gap-2">
                <FaFlag />
                <span>Flagged Reviews ({flaggedReviews.length})</span>
              </div>
            </button>
          </div>
        </div>

        {/* Claim Requests Content */}
        {activeTab === 'claims' && (
          <>
            {claimRequests.length === 0 ? (
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
                <FaCheckCircle className="text-green-500 text-5xl mx-auto mb-4" />
                <h3 className="text-xl font-semibold text-gray-900 mb-2">No Pending Claim Requests</h3>
                <p className="text-gray-600">All claim requests have been reviewed.</p>
              </div>
            ) : (
              <div className="space-y-6">
                {claimRequests.map((claim) => (
                  <div key={claim.id} className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                    {/* Claim Header */}
                    <div className="flex items-start justify-between mb-4">
                      <div>
                        <h3 className="text-lg font-bold text-gray-900">
                          {claim.professor_name}
                        </h3>
                        <p className="text-sm text-gray-500">
                          Department: {claim.professor_department}
                        </p>
                        <p className="text-sm text-gray-600 mt-2">
                          Requested by: <span className="font-medium">{claim.user_email}</span>
                        </p>
                      </div>
                      <div className="flex items-center gap-2 px-3 py-1 bg-yellow-50 text-yellow-600 rounded-full">
                        <FaUserTie />
                        <span className="font-medium">Pending</span>
                      </div>
                    </div>

                    {/* Request Message */}
                    {claim.request_message && (
                      <div className="mb-4 p-4 bg-gray-50 rounded-lg">
                        <p className="text-sm font-medium text-gray-700 mb-1">Request Message:</p>
                        <p className="text-gray-600">{claim.request_message}</p>
                      </div>
                    )}

                    {/* Metadata */}
                    <div className="mb-4 text-sm text-gray-500">
                      <p>Submitted: {formatDate(claim.requested_at)}</p>
                    </div>

                    {/* Actions - Left aligned and smaller buttons */}
                    <div className="flex gap-2">
                      <button
                        onClick={() => handleApproveClaim(claim.id)}
                        disabled={actionInProgress === claim.id}
                        className="flex items-center gap-1.5 px-3 py-1.5 text-sm bg-green-500 text-white rounded-md hover:bg-green-600 disabled:opacity-50 disabled:cursor-not-allowed font-medium transition"
                      >
                        <FaCheckCircle className="text-xs" />
                        <span>{actionInProgress === claim.id ? 'Approving...' : 'Approve'}</span>
                      </button>
                      <button
                        onClick={() => handleRejectClaim(claim.id)}
                        disabled={actionInProgress === claim.id}
                        className="flex items-center gap-1.5 px-3 py-1.5 text-sm bg-red-500 text-white rounded-md hover:bg-red-600 disabled:opacity-50 disabled:cursor-not-allowed font-medium transition"
                      >
                        <FaTimes className="text-xs" />
                        <span>{actionInProgress === claim.id ? 'Rejecting...' : 'Reject'}</span>
                      </button>
                    </div>
                  </div>
                ))}

              </div>
            )}
          </>
        )}

        {/* Flagged Reviews Content */}
        {activeTab === 'flags' && (
          <>
            {flaggedReviews.length === 0 ? (
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
            <FaCheckCircle className="text-green-500 text-5xl mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">No Flagged Reviews</h3>
            <p className="text-gray-600">All reviews are clear! Great job keeping the community safe.</p>
          </div>
        ) : (
          <div className="space-y-6">
            {flaggedReviews.map((review) => (
              <div key={review.id} className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                {/* Review Header */}
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h3 className="text-lg font-bold text-gray-900">
                      Professor: {review.professor_name}
                    </h3>
                    <p className="text-sm text-gray-500">
                      {review.course_code} • {review.semester}
                    </p>
                    <p className="text-sm text-gray-500">
                      Student: {review.student_email}
                    </p>
                  </div>
                  <div className="flex items-center gap-2 px-3 py-1 bg-red-50 text-red-600 rounded-full">
                    <FaFlag />
                    <span className="font-semibold">{review.flag_count} {review.flag_count === 1 ? 'Flag' : 'Flags'}</span>
                  </div>
                </div>

                {/* Ratings */}
                <div className="flex gap-4 mb-4">
                  <div>
                    <span className="text-sm text-gray-500">Quality:</span>
                    <span className="ml-2 font-semibold">{review.rating_quality}/5</span>
                  </div>
                  <div>
                    <span className="text-sm text-gray-500">Difficulty:</span>
                    <span className="ml-2 font-semibold">{review.rating_difficulty}/5</span>
                  </div>
                  <div>
                    <span className="text-sm text-gray-500">Grade:</span>
                    <span className="ml-2 font-semibold text-green-600">{review.grade_received}</span>
                  </div>
                </div>

                {/* Comment */}
                {review.comment && (
                  <div className="mb-4 p-4 bg-gray-50 rounded-lg">
                    <p className="text-sm font-medium text-gray-700 mb-2">Review Comment:</p>
                    <p className="text-gray-800">{review.comment}</p>
                  </div>
                )}

                {/* Flag Reasons */}
                <div className="mb-4">
                  <p className="text-sm font-medium text-gray-700 mb-2">Flag Reasons:</p>
                  <div className="space-y-2">
                    {review.flags.map((flag, idx) => (
                      <div key={idx} className="flex items-start gap-2 text-sm">
                        <FaFlag className="text-red-400 mt-1 flex-shrink-0" />
                        <div>
                          <p className="text-gray-700">
                            {flag.reason || 'No reason provided'}
                          </p>
                          <p className="text-gray-500 text-xs">
                            Flagged on {formatDate(flag.flagged_at)}
                          </p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Actions */}
                <div className="flex gap-3 pt-4 border-t border-gray-200">
                  <button
                    onClick={() => handleDeleteReview(review.id)}
                    disabled={actionInProgress === review.id}
                    className="flex items-center gap-2 px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 disabled:opacity-50 disabled:cursor-not-allowed transition font-medium"
                  >
                    <FaTrash />
                    {actionInProgress === review.id ? 'Deleting...' : 'Delete Review'}
                  </button>
                  <button
                    onClick={() => handleDismissFlags(review.id)}
                    disabled={actionInProgress === review.id}
                    className="flex items-center gap-2 px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 disabled:opacity-50 disabled:cursor-not-allowed transition font-medium"
                  >
                    <FaCheckCircle />
                    {actionInProgress === review.id ? 'Dismissing...' : 'Dismiss Flags'}
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
          </>
        )}
      </div>
    </div>
  );
}
