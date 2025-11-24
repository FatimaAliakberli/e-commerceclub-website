import { Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Home from './pages/Home';
import AboutUs from './pages/AboutUs';
import EventCourses from './pages/EventCourses';

function App() {
  return (
    <div className="bg-gradient-to-b from-white/80 via-white/90 to-white text-gray-800">
      {/* Navbar */}
      <Navbar />

      {/* Main content wrapper with top margin equal to navbar height */}
      <main className="pt-[80px]"> {/* 80px = approx navbar height */}
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<AboutUs />} />
          <Route path="/events-courses" element={<EventCourses />} />
        </Routes>
      </main>

      {/* Footer */}
      <Footer />
    </div>
  );
}

export default App;
