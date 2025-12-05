import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import ProfessorProfile from './pages/ProfessorProfile';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/professor/:id" element={<ProfessorProfile />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
