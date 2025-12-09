import { useState, useEffect } from 'react';
import { FaSearch, FaGraduationCap, FaChartLine, FaStar, FaUsers } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';
import ProfessorCard from '../components/ProfessorCard';
import { getProfessors } from '../services/api';

export default function Home() {
  const [professors, setProfessors] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    loadProfessors();
  }, []);

  const loadProfessors = async (search = '') => {
    try {
      setLoading(true);
      const response = await getProfessors(search);
      
      // Sort by rating (highest first)
      const sorted = response.data.sort((a, b) => b.avg_rating - a.avg_rating);
      
      // If no search query, show only top 3 rated professors
      if (!search) {
        setProfessors(sorted.slice(0, 3));
      } else {
        setProfessors(sorted);
      }
    } catch (error) {
      console.error('Failed to load professors:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e) => {
    e.preventDefault();
    loadProfessors(searchQuery);
  };

  const stats = [
    { icon: <FaUsers />, value: '1000+', label: 'Active Students' },
    { icon: <FaStar />, value: '2500+', label: 'Reviews Posted' },
    { icon: <FaGraduationCap />, value: '100+', label: 'Professors Listed' },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white">
      {/* Hero Section */}
      <section className="relative overflow-hidden">
        {/* Background Pattern */}
        <div className="absolute inset-0 bg-gradient-to-br from-blue-600 via-blue-700 to-indigo-800" />
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-20 left-10 w-72 h-72 bg-white rounded-full blur-3xl" />
          <div className="absolute bottom-20 right-10 w-96 h-96 bg-blue-300 rounded-full blur-3xl" />
        </div>

        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 lg:py-32">
          <div className="text-center">
            {/* Badge */}
            <div className="inline-flex items-center gap-2 bg-white/10 backdrop-blur-sm text-white px-4 py-2 rounded-full text-sm mb-6">
              <FaChartLine />
              <span>Data-Driven Professor Insights</span>
            </div>

            {/* Heading */}
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-white mb-6">
              Find the Right Professor<br />
              <span className="text-blue-200">Make Informed Decisions</span>
            </h1>

            {/* Subtitle */}
            <p className="text-lg text-blue-100 max-w-2xl mx-auto mb-10">
              Access real student reviews, grade distributions, and detailed analytics 
              to choose the best professors for your academic journey.
            </p>

            {/* Search Box */}
            <form onSubmit={handleSearch} className="max-w-2xl mx-auto">
              <div className="flex gap-3 bg-white p-2 rounded-2xl shadow-2xl">
                <div className="flex-1 relative">
                  <FaSearch className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400" />
                  <input
                    type="text"
                    placeholder="Search by professor name or department..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="w-full pl-12 pr-4 py-4 bg-transparent focus:outline-none text-gray-700 placeholder-gray-400"
                  />
                </div>
                <button
                  type="submit"
                  className="bg-blue-600 text-white px-8 py-4 rounded-xl font-semibold hover:bg-blue-700 transition shadow-lg hover:shadow-xl"
                >
                  Search
                </button>
              </div>
            </form>

            {/* Quick Stats */}
            {/* <div className="flex flex-wrap justify-center gap-8 mt-12">
              {stats.map((stat, idx) => (
                <div key={idx} className="flex items-center gap-3 text-white/80">
                  <div className="text-2xl text-blue-200">{stat.icon}</div>
                  <div className="text-left">
                    <div className="font-bold text-white">{stat.value}</div>
                    <div className="text-sm">{stat.label}</div>
                  </div>
                </div>
              ))}
            </div> */}
          </div>
        </div>

        {/* Wave Divider */}
        <div className="absolute bottom-0 left-0 right-0">
          <svg viewBox="0 0 1440 120" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M0 120L60 110C120 100 240 80 360 70C480 60 600 60 720 65C840 70 960 80 1080 85C1200 90 1320 90 1380 90L1440 90V120H1380C1320 120 1200 120 1080 120C960 120 840 120 720 120C600 120 480 120 360 120C240 120 120 120 60 120H0Z" fill="#f8fafc"/>
          </svg>
        </div>
      </section>

      {/* Professors Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h2 className="text-2xl font-bold text-gray-800">
              {searchQuery ? `Results for "${searchQuery}"` : ' Top Rated Professors'}
            </h2>
            <p className="text-gray-500 mt-1">
              {searchQuery ? `${professors.length} professors found` : 'Highest rated by students'}
            </p>
          </div>
        </div>

        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[1, 2, 3].map((i) => (
              <div key={i} className="bg-white rounded-xl p-6 animate-pulse">
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-12 h-12 bg-gray-200 rounded-full" />
                  <div className="flex-1">
                    <div className="h-4 bg-gray-200 rounded w-3/4 mb-2" />
                    <div className="h-3 bg-gray-200 rounded w-1/2" />
                  </div>
                </div>
                <div className="h-20 bg-gray-100 rounded" />
              </div>
            ))}
          </div>
        ) : professors.length === 0 ? (
          <div className="text-center py-16">
            <FaGraduationCap className="text-6xl text-gray-300 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-600 mb-2">No Professors Found</h3>
            <p className="text-gray-500">Try a different search term or browse all professors.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {professors.map((professor) => (
              <ProfessorCard key={professor.id} professor={professor} />
            ))}
          </div>
        )}
      </section>

      {/* Features Section */}
      <section className="bg-white border-t border-gray-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-800 mb-4">
              Why Students Trust ProfReview
            </h2>
            <p className="text-gray-500 max-w-2xl mx-auto">
              Make confident academic decisions with our comprehensive professor insights
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center p-6">
              <div className="w-16 h-16 bg-blue-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <FaChartLine className="text-2xl text-blue-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-800 mb-2">Grade Distribution</h3>
              <p className="text-gray-500">
                See exactly how students perform with visual grade charts and historical data.
              </p>
            </div>

            <div className="text-center p-6">
              <div className="w-16 h-16 bg-green-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <FaStar className="text-2xl text-green-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-800 mb-2">Verified Reviews</h3>
              <p className="text-gray-500">
                Real feedback from students who have taken the course and earned their grades.
              </p>
            </div>

            <div className="text-center p-6">
              <div className="w-16 h-16 bg-purple-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <FaUsers className="text-2xl text-purple-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-800 mb-2">Community Driven</h3>
              <p className="text-gray-500">
                Join thousands of students sharing their experiences to help each other succeed.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-400">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center gap-2 mb-4 md:mb-0">
              <div className="bg-blue-600 p-2 rounded-lg">
                <FaGraduationCap className="text-white" />
              </div>
              <span className="text-xl font-bold text-white">ProfReview</span>
            </div>
            <p className="text-sm">
              © 2024 ProfReview. Built for students, by students.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}

