import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';

const GRADE_COLORS = {
  'A+': '#3b82f6',
  'A': '#3b82f6',
  'A-': '#60a5fa',
  'B+': '#3b82f6',
  'B': '#3b82f6',
  'B-': '#60a5fa',
  'C+': '#3b82f6',
  'C': '#3b82f6',
  'C-': '#60a5fa',
  'D': '#3b82f6',
  'F': '#3b82f6',
  'W': '#94a3b8'
};

export default function GradeDistributionChart({ data }) {
  if (!data || data.length === 0) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">Grade Distribution</h3>
        <p className="text-gray-500 text-center py-8">No grade data available yet.</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
      <h3 className="text-lg font-semibold text-gray-800 mb-4">Grade Distribution</h3>
      <ResponsiveContainer width="100%" height={280}>
        <BarChart data={data} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
          <XAxis 
            dataKey="grade" 
            axisLine={false}
            tickLine={false}
            tick={{ fill: '#6b7280', fontSize: 12 }}
          />
          <YAxis 
            allowDecimals={false}
            axisLine={false}
            tickLine={false}
            tick={{ fill: '#9ca3af', fontSize: 12 }}
          />
          <Tooltip 
            contentStyle={{ 
              backgroundColor: '#fff', 
              border: '1px solid #e5e7eb',
              borderRadius: '8px',
              boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
            }}
            formatter={(value) => [`${value} students`, 'Count']}
          />
          <Bar 
            dataKey="count" 
            radius={[4, 4, 0, 0]}
            maxBarSize={50}
          >
            {data.map((entry, index) => (
              <Cell 
                key={index} 
                fill={GRADE_COLORS[entry.grade] || '#3b82f6'} 
              />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

