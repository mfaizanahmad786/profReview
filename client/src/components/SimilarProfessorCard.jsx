import { Link } from 'react-router-dom';
import { FaStar } from 'react-icons/fa';
import DepartmentAvatar from './DepartmentAvatar';

export default function SimilarProfessorCard({ professor }) {
  return (
    <Link to={`/professor/${professor.id}`}>
      <div className="flex items-center gap-3 p-3 rounded-lg hover:bg-gray-50 transition cursor-pointer">
        <DepartmentAvatar 
          department={professor.department}
          name={professor.name}
          size="sm"
        />
        <div className="flex-1">
          <h4 className="font-medium text-gray-800 text-sm">{professor.name}</h4>
          <p className="text-xs text-gray-500">{professor.department}</p>
        </div>
        <div className="flex items-center gap-1 text-yellow-500">
          <span className="font-semibold text-gray-700">{professor.avg_rating.toFixed(1)}</span>
          <FaStar className="text-sm" />
        </div>
      </div>
    </Link>
  );
}
