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

// Unified color for all departments
const UNIFIED_COLORS = ['#3b82f6', '#06b6d4']; // blue to cyan

// Department configuration with icons
const DEPARTMENT_CONFIG = {
  'computer': {
    colors: UNIFIED_COLORS,
    icons: [FaCode, FaLaptopCode, FaDatabase],
  },
  'math': {
    colors: UNIFIED_COLORS,
    icons: [FaCalculator, FaSuperscript],
  },
  'physics': {
    colors: UNIFIED_COLORS,
    icons: [FaAtom, FaFlask],
  },
  'chemistry': {
    colors: UNIFIED_COLORS,
    icons: [FaFlask, FaMicroscope],
  },
  'biology': {
    colors: UNIFIED_COLORS,
    icons: [FaDna, FaMicroscope],
  },
  'economics': {
    colors: UNIFIED_COLORS,
    icons: [FaChartLine, FaBalanceScale],
  },
  'literature': {
    colors: UNIFIED_COLORS,
    icons: [FaBook, FaPencilAlt],
  },
  'psychology': {
    colors: UNIFIED_COLORS,
    icons: [FaBrain, FaHeart],
  },
  'geography': {
    colors: UNIFIED_COLORS,
    icons: [FaGlobe],
  },
  'music': {
    colors: UNIFIED_COLORS,
    icons: [FaMusic],
  },
  'art': {
    colors: UNIFIED_COLORS,
    icons: [FaPalette],
  },
  'default': {
    colors: UNIFIED_COLORS,
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
