import { useState, useEffect } from 'react';
import { FaUserCheck, FaClock, FaCheckCircle, FaTimesCircle, FaSpinner } from 'react-icons/fa';
import { useAuth } from '../context/AuthContext';
import { submitClaimRequest, getMyClaimStatus, cancelClaimRequest } from '../services/api';

export default function ClaimProfileButton({ professorId, professorName }) {
  const { user } = useAuth();
  const [claimStatus, setClaimStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [requestMessage, setRequestMessage] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');

  // Only show for professors
  if (!user || user.role !== 'professor') {
    return null;
  }

  useEffect(() => {
    fetchClaimStatus();
  }, []);

  const fetchClaimStatus = async () => {
    try {
      const response = await getMyClaimStatus();
      setClaimStatus(response.data);
    } catch (err) {
      console.error('Error fetching claim status:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmitClaim = async () => {
    setIsSubmitting(true);
    setError('');

    try {
      await submitClaimRequest(professorId, requestMessage);
      setShowModal(false);
      setRequestMessage('');
      await fetchClaimStatus(); // Refresh status
      alert('Claim request submitted successfully! Please wait for admin approval.');
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to submit claim request');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleCancelClaim = async () => {
    if (!claimStatus?.claim_request?.id) return;

    if (!confirm('Are you sure you want to cancel your claim request?')) return;

    try {
      await cancelClaimRequest(claimStatus.claim_request.id);
      await fetchClaimStatus(); // Refresh status
      alert('Claim request cancelled successfully');
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to cancel claim request');
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center p-4">
        <FaSpinner className="animate-spin text-gray-400 text-xl" />
      </div>
    );
  }

  // If user has approved claim for this professor
  if (claimStatus?.has_approved && claimStatus?.claimed_professor_id === professorId) {
    return (
      <div className="bg-green-50 border border-green-200 rounded-lg p-4 flex items-center gap-3">
        <FaCheckCircle className="text-green-600 text-2xl" />
        <div>
          <p className="font-semibold text-green-900">Profile Claimed</p>
          <p className="text-sm text-green-700">This is your verified profile</p>
        </div>
      </div>
    );
  }

  // If user has pending claim for this professor
  if (claimStatus?.has_pending && claimStatus?.claim_request?.professor_id === professorId) {
    return (
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
        <div className="flex items-center gap-3 mb-2">
          <FaClock className="text-yellow-600 text-2xl" />
          <div>
            <p className="font-semibold text-yellow-900">Claim Pending</p>
            <p className="text-sm text-yellow-700">Waiting for admin approval</p>
          </div>
        </div>
        <button
          onClick={handleCancelClaim}
          className="mt-3 text-sm text-yellow-700 hover:text-yellow-900 underline"
        >
          Cancel Request
        </button>
      </div>
    );
  }

  // If user already has an approved claim for a different professor
  if (claimStatus?.has_approved && claimStatus?.claimed_professor_id !== professorId) {
    return (
      <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
        <p className="text-sm text-gray-600">
          You have already claimed another professor profile
        </p>
      </div>
    );
  }

  // If user has pending claim for a different professor
  if (claimStatus?.has_pending && claimStatus?.claim_request?.professor_id !== professorId) {
    return (
      <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
        <p className="text-sm text-gray-600">
          You have a pending claim request for another professor
        </p>
      </div>
    );
  }

  // Show claim button
  return (
    <>
      <button
        onClick={() => setShowModal(true)}
        className="w-full bg-blue-600 text-white py-3 px-4 rounded-lg font-semibold hover:bg-blue-700 transition flex items-center justify-center gap-2"
      >
        <FaUserCheck />
        Request to Claim This Profile
      </button>

      {/* Claim Request Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-gray-500 bg-opacity-50 flex items-center justify-center p-4 w-full h-full z-50">
          <div className="bg-white rounded-xl max-w-md w-full p-6">
            <h3 className="text-xl font-bold text-gray-900 mb-4">
              Claim Profile: {professorName}
            </h3>
            
            <p className="text-gray-600 mb-4">
              Submit a request to claim this professor profile. An administrator will review your request.
            </p>

            {error && (
              <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
                <p className="text-red-600 text-sm">{error}</p>
              </div>
            )}

            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Message (Optional)
              </label>
              <textarea
                value={requestMessage}
                onChange={(e) => setRequestMessage(e.target.value)}
                placeholder="Why are you claiming this profile? (e.g., 'I am Dr. John Smith, teaching Computer Science since 2015')"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                rows="4"
                maxLength="1000"
              />
              <p className="text-xs text-gray-500 mt-1">
                {requestMessage.length}/1000 characters
              </p>
            </div>

            <div className="flex gap-3">
              <button
                onClick={() => {
                  setShowModal(false);
                  setRequestMessage('');
                  setError('');
                }}
                className="flex-1 px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition"
                disabled={isSubmitting}
              >
                Cancel
              </button>
              <button
                onClick={handleSubmitClaim}
                disabled={isSubmitting}
                className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isSubmitting ? 'Submitting...' : 'Submit Request'}
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
