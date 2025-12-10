import { useState } from 'react';
import { FaThumbsUp, FaFlag } from 'react-icons/fa';
import { voteReview, unvoteReview } from '../services/api';
import { useAuth } from '../context/AuthContext';

export default function ReviewCard({ review: initialReview }) {
  const { user } = useAuth();
  const [review, setReview] = useState(initialReview);
  const [isVoting, setIsVoting] = useState(false);

  const tags = ['Clear Grading', 'Helpful']; // Mock tags for now

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const handleVoteToggle = async () => {
    if (!user) {
      alert('Please log in to vote on reviews');
      return;
    }

    if (isVoting) return;
    
    setIsVoting(true);
    try {
      if (review.user_voted) {
        // Unvote
        const response = await unvoteReview(review.id);
        setReview({ 
          ...review, 
          helpful_count: response.data.helpful_count,
          user_voted: false 
        });
      } else {
        // Vote
        const response = await voteReview(review.id);
        setReview({ 
          ...review, 
          helpful_count: response.data.helpful_count,
          user_voted: true 
        });
      }
    } catch (error) {
      console.error('Error voting:', error);
      if (error.response?.status === 401) {
        alert('Please log in to vote on reviews');
      } else {
        alert(error.response?.data?.detail || 'Failed to vote');
      }
    } finally {
      setIsVoting(false);
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gray-100 rounded-full flex items-center justify-center text-gray-600 font-medium text-sm">
            {review.course_code ? review.course_code.substring(0, 2) : 'CS'}
          </div>
          <div>
            <h4 className="font-semibold text-gray-800">
              {review.course_code || 'Course'}: {review.semester}
            </h4>
            <p className="text-sm text-gray-500">{formatDate(review.created_at)}</p>
          </div>
        </div>
        <div className="text-right">
          <div className="text-sm text-gray-500">QUALITY</div>
          <div className="text-2xl font-bold text-gray-800">{review.rating_quality}.0</div>
        </div>
      </div>

      {/* Tags */}
      <div className="flex flex-wrap gap-2 mb-4">
        {tags.map((tag, idx) => (
          <span 
            key={idx}
            className="px-3 py-1 bg-blue-50 text-blue-600 text-sm rounded-full"
          >
            {tag}
          </span>
        ))}
      </div>

      {/* Comment */}
      {review.comment && (
        <p className="text-gray-700 leading-relaxed mb-4">
          {review.comment}
        </p>
      )}

      {/* Footer */}
      <div className="flex items-center justify-between pt-4 border-t border-gray-100">
        <div className="flex items-center gap-2">
          <span className="text-sm text-gray-500">Grade Received:</span>
          <span className="font-semibold text-green-600">{review.grade_received}</span>
        </div>
        <div className="flex items-center gap-4">
          <button 
            onClick={handleVoteToggle}
            disabled={isVoting}
            className={`flex items-center gap-1 transition text-sm ${
              review.user_voted 
                ? 'text-blue-600 hover:text-blue-700' 
                : 'text-gray-400 hover:text-blue-600'
            } ${isVoting ? 'opacity-50 cursor-not-allowed' : ''}`}
          >
            <FaThumbsUp className={review.user_voted ? 'fill-current' : ''} />
            <span>Helpful ({review.helpful_count || 0})</span>
          </button>
          <button className="flex items-center gap-1 text-gray-400 hover:text-red-500 transition text-sm">
            <FaFlag />
            <span>Flag</span>
          </button>
        </div>
      </div>
    </div>
  );
}

