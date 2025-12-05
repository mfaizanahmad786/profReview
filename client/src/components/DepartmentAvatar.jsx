import { 
  FaCode, 
  FaLaptopCode, 
  FaDatabase,
  FaCalculator, 
  FaSuperscript,
  FaAtom, 
  FaFlask,
  FaMicroscope,
  FaBook,
  FaGraduationCap,
  FaPencilAlt,
  FaChartLine,
  FaDna,
  FaGlobe,
  FaBalanceScale,
  FaMusic,
  FaPalette,
  FaHeart,
  FaBrain
} from 'react-icons/fa';

// Department configuration with colors and icons
const DEPARTMENT_CONFIG = {
  'computer': {
    colors: ['#3b82f6', '#06b6d4'], // blue to cyan
    icons: [FaCode, FaLaptopCode, FaDatabase],
  },
  'math': {
    colors: ['#a855f7', '#ec4899'], // purple to pink
    icons: [FaCalculator, FaSuperscript],
  },
  'physics': {
    colors: ['#f97316', '#ef4444'], // orange to red
    icons: [FaAtom, FaFlask],
  },
  'chemistry': {
    colors: ['#22c55e', '#14b8a6'], // green to teal
    icons: [FaFlask, FaMicroscope],
  },
  'biology': {
    colors: ['#10b981', '#16a34a'], // emerald to green
    icons: [FaDna, FaMicroscope],
  },
  'economics': {
    colors: ['#f59e0b', '#eab308'], // amber to yellow
    icons: [FaChartLine, FaBalanceScale],
  },
  'literature': {
    colors: ['#f43f5e', '#ec4899'], // rose to pink
    icons: [FaBook, FaPencilAlt],
  },
  'psychology': {
    colors: ['#8b5cf6', '#7c3aed'], // violet to purple
    icons: [FaBrain, FaHeart],
  },
  'geography': {
    colors: ['#0ea5e9', '#2563eb'], // sky to blue
    icons: [FaGlobe],
  },
  'music': {
    colors: ['#d946ef', '#a855f7'], // fuchsia to purple
    icons: [FaMusic],
  },
  'art': {
    colors: ['#ec4899', '#f43f5e'], // pink to rose
    icons: [FaPalette],
  },
  'default': {
    colors: ['#6b7280', '#475569'], // gray to slate
    icons: [FaGraduationCap],
  }
};

// Get config key for department
const getDepartmentKey = (department) => {
  if (!department) return 'default';
  
  const deptLower = department.toLowerCase();
  
  if (deptLower.includes('computer') || deptLower.includes('software') || deptLower.includes(' cs') || deptLower === 'cs') {
    return 'computer';
  }
  if (deptLower.includes('math') || deptLower.includes('statistic')) {
    return 'math';
  }
  if (deptLower.includes('physic')) {
    return 'physics';
  }
  if (deptLower.includes('chem')) {
    return 'chemistry';
  }
  if (deptLower.includes('bio')) {
    return 'biology';
  }
  if (deptLower.includes('econ') || deptLower.includes('business') || deptLower.includes('finance')) {
    return 'economics';
  }
  if (deptLower.includes('english') || deptLower.includes('literature') || deptLower.includes('writing')) {
    return 'literature';
  }
  if (deptLower.includes('psych')) {
    return 'psychology';
  }
  if (deptLower.includes('geo')) {
    return 'geography';
  }
  if (deptLower.includes('music')) {
    return 'music';
  }
  if (deptLower.includes('art') || deptLower.includes('design')) {
    return 'art';
  }
  
  return 'default';
};

export default function DepartmentAvatar({ department, name, size = 'md' }) {
  const key = getDepartmentKey(department);
  const config = DEPARTMENT_CONFIG[key];
  const Icon1 = config.icons[0];
  const Icon2 = config.icons[1] || config.icons[0];
  
  // Size configurations
  const sizes = {
    sm: { container: 40, icon: 14, iconSmall: 10 },
    md: { container: 48, icon: 18, iconSmall: 12 },
    lg: { container: 80, icon: 28, iconSmall: 14 },
    xl: { container: 96, icon: 36, iconSmall: 16 }
  };
  
  const sizeConfig = sizes[size] || sizes.md;
  
  // Gradient style
  const gradientStyle = {
    background: `linear-gradient(135deg, ${config.colors[0]}, ${config.colors[1]})`,
    width: sizeConfig.container,
    height: sizeConfig.container,
  };

  return (
    <div 
      style={gradientStyle}
      className="rounded-2xl flex items-center justify-center shadow-lg relative overflow-hidden flex-shrink-0"
    >
      {/* Background pattern */}
      <div className="absolute inset-0 opacity-20">
        <div className="absolute -top-1 -left-1">
          <Icon1 
            className="text-white opacity-30" 
            style={{ fontSize: size === 'lg' || size === 'xl' ? 40 : 20 }} 
          />
        </div>
        <div className="absolute -bottom-1 -right-1">
          <Icon2 
            className="text-white opacity-30" 
            style={{ fontSize: size === 'lg' || size === 'xl' ? 32 : 16 }} 
          />
        </div>
      </div>
      
      {/* Main icon */}
      <div className="relative z-10 flex flex-col items-center">
        <Icon1 className="text-white" style={{ fontSize: sizeConfig.icon }} />
        {(size === 'lg' || size === 'xl') && config.icons.length > 1 && (
          <div className="flex gap-1 mt-1">
            {config.icons.slice(0, 3).map((IconItem, idx) => (
              <IconItem 
                key={idx} 
                className="text-white/70" 
                style={{ fontSize: sizeConfig.iconSmall }} 
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

// Export for use elsewhere
export { getDepartmentKey, DEPARTMENT_CONFIG };
