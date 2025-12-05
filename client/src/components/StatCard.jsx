import { FaStar, FaThumbsUp } from 'react-icons/fa';

export default function StatCard({ type, value, label }) {
  const getConfig = () => {
    switch (type) {
      case 'rating':
        return {
          icon: <FaStar className="text-yellow-400" />,
          valueColor: 'text-gray-800',
          stars: Math.round(value),
        };
      case 'difficulty':
        return {
          icon: null,
          valueColor: 'text-gray-800',
          subtitle: 'out of 5',
        };
      case 'recommend':
        return {
          icon: <FaThumbsUp className="text-green-500" />,
          valueColor: 'text-gray-800',
          isPercent: true,
        };
      default:
        return {};
    }
  };

  const config = getConfig();

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 text-center">
      <div className={`text-4xl font-bold ${config.valueColor} mb-1`}>
        {config.isPercent ? `${value}%` : value.toFixed(1)}
      </div>
      
      {type === 'rating' && (
        <div className="flex justify-center gap-1 mb-2">
          {[1, 2, 3, 4, 5].map((star) => (
            <FaStar
              key={star}
              className={`text-sm ${star <= config.stars ? 'text-yellow-400' : 'text-gray-200'}`}
            />
          ))}
        </div>
      )}
      
      {type === 'difficulty' && (
        <div className="text-sm text-gray-400 mb-2">
          <span className="inline-flex items-center gap-1">
            <span className="w-2 h-2 bg-blue-500 rounded-full"></span>
            {config.subtitle}
          </span>
        </div>
      )}
      
      {type === 'recommend' && (
        <div className="flex justify-center mb-2">
          {config.icon}
        </div>
      )}
      
      <div className="text-sm font-medium text-gray-500 uppercase tracking-wide">
        {label}
      </div>
    </div>
  );
}

