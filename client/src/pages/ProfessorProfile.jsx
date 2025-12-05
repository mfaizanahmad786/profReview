import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { FaStar, FaRegClipboard, FaEdit, FaArrowLeft } from 'react-icons/fa';
import StatCard from '../components/StatCard';
import GradeDistributionChart from '../components/GradeDistributionChart';
import ReviewCard from '../components/ReviewCard';
import SimilarProfessorCard from '../components/SimilarProfessorCard';
import DepartmentAvatar from '../components/DepartmentAvatar';
import { getProfessor, getProfessorReviews, getGradeDistribution, getProfessors } from '../services/api';

export default function ProfessorProfile() {
  const { id } = useParams();
  const [professor, setProfessor] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [gradeData, setGradeData] = useState([]);
  const [similarProfessors, setSimilarProfessors] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadProfessorData();
  }, [id]);

  const loadProfessorData = async () => {
    try {
      setLoading(true);
      
      // Load all data in parallel
      const [profRes, reviewsRes, gradesRes, allProfsRes] = await Promise.all([
        getProfessor(id),
        getProfessorReviews(id),
        getGradeDistribution(id),
        getProfessors()
      ]);

      setProfessor(profRes.data);
      setReviews(reviewsRes.data);
      setGradeData(gradesRes.data);
      
      // Filter similar professors (same department, exclude current)
      const similar = allProfsRes.data
        .filter(p => p.id !== parseInt(id) && p.department === profRes.data.department)
        .slice(0, 3);
      
      // If not enough in same department, add others
      if (similar.length < 3) {
        const others = allProfsRes.data
          .filter(p => p.id !== parseInt(id) && !similar.find(s => s.id === p.id))
          .slice(0, 3 - similar.length);
        similar.push(...others);
      }
      
      setSimilarProfessors(similar);
    } catch (error) {
      console.error('Failed to load professor data:', error);
    } finally {
      setLoading(false);
    }
  };

  // Calculate "would take again" percentage (mock calculation for now)
  const wouldTakeAgain = reviews.length > 0 
    ? Math.round((reviews.filter(r => r.rating_quality >= 4).length / reviews.length) * 100)
    : 0;

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!professor) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-800 mb-2">Professor Not Found</h2>
          <Link to="/" className="text-blue-600 hover:underline">Go back home</Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Back Button */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-6">
        <Link 
          to="/" 
          className="inline-flex items-center gap-2 text-gray-600 hover:text-blue-600 transition"
        >
          <FaArrowLeft />
          <span>Back to Search</span>
        </Link>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Professor Header Card */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-4">
                  {/* Department-based Avatar */}
                  <DepartmentAvatar 
                    department={professor.department}
                    name={professor.name}
                    size="lg"
                  />
                  <div>
                    <h1 className="text-2xl font-bold text-gray-800">{professor.name}</h1>
                    <p className="text-gray-600">Department of {professor.department}</p>
                    <p className="text-gray-400 text-sm">Tech University • Since 2018</p>
                  </div>
                </div>
                <button className="flex items-center gap-2 px-4 py-2 border border-gray-200 rounded-lg hover:bg-gray-50 transition text-gray-600">
                  <FaRegClipboard />
                  <span>Claim Profile</span>
                </button>
              </div>
            </div>

            {/* Stats Row */}
            <div className="grid grid-cols-3 gap-4">
              <StatCard 
                type="rating" 
                value={professor.avg_rating} 
                label="Overall Quality" 
              />
              <StatCard 
                type="difficulty" 
                value={professor.avg_difficulty} 
                label="Difficulty Level" 
              />
              <StatCard 
                type="recommend" 
                value={wouldTakeAgain} 
                label="Would Take Again" 
              />
            </div>

            {/* Grade Distribution */}
            <GradeDistributionChart data={gradeData} />

            {/* Reviews Section */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-semibold text-gray-800">
                  Student Reviews ({reviews.length})
                </h2>
                <button className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition">
                  <FaEdit />
                  <span>Write a Review</span>
                </button>
              </div>

              {reviews.length === 0 ? (
                <div className="text-center py-12">
                  <FaStar className="text-5xl text-gray-200 mx-auto mb-4" />
                  <h3 className="text-lg font-medium text-gray-600 mb-2">No Reviews Yet</h3>
                  <p className="text-gray-500">Be the first to review this professor!</p>
                </div>
              ) : (
                <div className="space-y-4">
                  {reviews.map((review) => (
                    <ReviewCard key={review.id} review={review} />
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Similar Professors */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
              <h3 className="font-semibold text-gray-800 mb-4">Similar Professors</h3>
              {similarProfessors.length === 0 ? (
                <p className="text-gray-500 text-sm">No similar professors found.</p>
              ) : (
                <div className="space-y-2">
                  {similarProfessors.map((prof) => (
                    <SimilarProfessorCard key={prof.id} professor={prof} />
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
