import { Link } from 'react-router-dom';
import { FaStar, FaChartBar, FaArrowRight } from 'react-icons/fa';
import DepartmentAvatar from './DepartmentAvatar';

export default function ProfessorCard({ professor }) {
  const getRatingColor = (rating) => {
    if (rating >= 4) return 'text-green-600 bg-green-50';
    if (rating >= 3) return 'text-yellow-600 bg-yellow-50';
    return 'text-red-600 bg-red-50';
  };

  return (
    <Link to={`/professor/${professor.id}`}>
      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 hover:shadow-md hover:border-blue-200 transition-all duration-200 group">
        {/* Header */}
        <div className="flex items-start justify-between mb-4">
          <div className="flex items-center gap-3">
            <DepartmentAvatar 
              department={professor.department} 
              name={professor.name}
              size="md"
            />
            <div>
              <h3 className="font-semibold text-gray-800 group-hover:text-blue-600 transition">
                {professor.name}
              </h3>
              <p className="text-sm text-gray-500">{professor.department}</p>
            </div>
          </div>
          <FaArrowRight className="text-gray-300 group-hover:text-blue-500 transition" />
        </div>

        {/* Stats */}
        <div className="flex items-center gap-4">
          <div className={`flex items-center gap-1 px-3 py-1 rounded-full ${getRatingColor(professor.avg_rating)}`}>
            <FaStar className="text-sm" />
            <span className="font-semibold">{professor.avg_rating.toFixed(1)}</span>
          </div>
          <div className="flex items-center gap-1 text-gray-500 text-sm">
            <FaChartBar />
            <span>{professor.total_reviews} reviews</span>
          </div>
        </div>

        {/* Difficulty */}
        
      </div>
    </Link>
  );
}
