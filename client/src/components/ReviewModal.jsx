import { useState } from 'react';
import { FaTimes, FaStar } from 'react-icons/fa';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { createReview } from '../services/api';

export default function ReviewModal({ professor, onClose, onReviewSubmitted }) {
  const { isAuthenticated, user } = useAuth();
  const navigate = useNavigate();
  
  // Get current semester (e.g., "Fall 2025")
  const getCurrentSemester = () => {
    const date = new Date();
    const year = date.getFullYear();
    const month = date.getMonth();
    const season = month >= 8 ? 'Fall' : month >= 5 ? 'Summer' : month >= 1 ? 'Spring' : 'Winter';
    return `${season} ${year}`;
  };
  
  const [formData, setFormData] = useState({
    rating_quality: 0,
    rating_difficulty: 0,
    course_code: '',
    grade_received: '',
    comment: '',
    semester: getCurrentSemester(),
  });
  
  const [hoveredRating, setHoveredRating] = useState(0);
  const [hoveredDifficulty, setHoveredDifficulty] = useState(0);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');

  // Redirect to login if not authenticated
  if (!isAuthenticated) {
    navigate('/login');
    return null;
  }

  const grades = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D', 'F', 'W'];

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    // Validation
    if (formData.rating_quality === 0) {
      setError('Please select a rating');
      return;
    }
    if (formData.rating_difficulty === 0) {
      setError('Please select a difficulty level');
      return;
    }
    if (!formData.grade_received) {
      setError('Please select a grade');
      return;
    }

    setIsSubmitting(true);

    try {
      await createReview({
        professor_id: professor.id,
        rating_quality: formData.rating_quality,
        rating_difficulty: formData.rating_difficulty,
        grade_received: formData.grade_received,
        course_code: formData.course_code || null,
        comment: formData.comment || null,
        semester: formData.semester,
      });

      // Call callback to refresh reviews
      if (onReviewSubmitted) {
        onReviewSubmitted();
      }
      
      onClose();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to submit review. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const StarRating = ({ value, hovered, onChange, onHover, label }) => (
    <div className="flex flex-col gap-2">
      <label className="text-sm font-medium text-gray-700">{label}</label>
      <div className="flex gap-1">
        {[1, 2, 3, 4, 5].map((star) => (
          <button
            key={star}
            type="button"
            onClick={() => onChange(star)}
            onMouseEnter={() => onHover(star)}
            onMouseLeave={() => onHover(0)}
            className="focus:outline-none transition-transform hover:scale-110"
          >
            <FaStar
              className={`text-2xl ${
                star <= (hovered || value)
                  ? 'text-yellow-400'
                  : 'text-gray-300'
              }`}
            />
          </button>
        ))}
        <span className="ml-2 text-sm text-gray-600">
          {(hovered || value) ? `${hovered || value}/5` : 'Select rating'}
        </span>
      </div>
    </div>
  );

  return (
    <div className="fixed inset-0 bg-gray-400 bg-opacity-5 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="sticky top-0 bg-white border-b border-gray-200 p-6 flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">Write a Review</h2>
            <p className="text-gray-600 mt-1">
              {professor.name} • {professor.department}
            </p>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition"
          >
            <FaTimes className="text-xl" />
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="p-6 space-y-6">
          {error && (
            <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-red-600 text-sm">{error}</p>
            </div>
          )}

          {/* Rating */}
          <StarRating
            label="Overall Rating *"
            value={formData.rating_quality}
            hovered={hoveredRating}
            onChange={(value) => setFormData({ ...formData, rating_quality: value })}
            onHover={setHoveredRating}
          />

          {/* Difficulty */}
          <StarRating
            label="Difficulty Level *"
            value={formData.rating_difficulty}
            hovered={hoveredDifficulty}
            onChange={(value) => setFormData({ ...formData, rating_difficulty: value })}
            onHover={setHoveredDifficulty}
          />

          {/* Would Take Again - REMOVED */}

          {/* Course Taken */}
          <div>
            <label htmlFor="course" className="block text-sm font-medium text-gray-700 mb-2">
              Course Code
            </label>
            <input
              id="course"
              type="text"
              value={formData.course_code}
              onChange={(e) => setFormData({ ...formData, course_code: e.target.value })}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="e.g., CS 101"
            />
          </div>

          {/* Grade Received */}
          <div>
            <label htmlFor="grade" className="block text-sm font-medium text-gray-700 mb-2">
              Grade Received *
            </label>
            <select
              id="grade"
              value={formData.grade_received}
              onChange={(e) => setFormData({ ...formData, grade_received: e.target.value })}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            >
              <option value="">Select grade</option>
              {grades.map((grade) => (
                <option key={grade} value={grade}>
                  {grade}
                </option>
              ))}
            </select>
          </div>

          {/* Comment */}
          <div>
            <label htmlFor="comment" className="block text-sm font-medium text-gray-700 mb-2">
              Your Review
            </label>
            <textarea
              id="comment"
              value={formData.comment}
              onChange={(e) => setFormData({ ...formData, comment: e.target.value })}
              rows={5}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
              placeholder="Share your experience with this professor..."
            />
          </div>

          {/* Submit Button */}
          <div className="flex gap-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 px-6 py-3 border border-gray-300 text-gray-700 rounded-lg font-medium hover:bg-gray-50 transition"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isSubmitting}
              className="flex-1 px-6 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isSubmitting ? 'Submitting...' : 'Submit Review'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
