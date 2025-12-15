import { Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Home from './pages/Home';
import AboutUs from './pages/AboutUs';
import EventCourses from './pages/EventCourses';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import EventDetailPage from './pages/EventDetailPage';
import AdminRoute from './components/AdminRoute'; // <-- NEW Import
import AdminDashboard from './pages/AdminDashboard'; // <-- NEW Page (We'll create this next)
import EventRegistrationPage from './pages/EventRegistrationPage';

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
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/events/:id" element={<EventDetailPage />} />
          <Route path="/register/event/:id" element={<EventRegistrationPage />} />

          <Route 
            path="/admin" 
            element={
              <AdminRoute>
                <AdminDashboard />
              </AdminRoute>
            } 
          />
          
        </Routes>
      </main>

      {/* Footer */}
      <Footer />
    </div>
  );
}

export default App;


