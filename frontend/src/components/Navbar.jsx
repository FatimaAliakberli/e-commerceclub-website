// import { useState, useEffect } from 'react';
// import { Link } from 'react-router-dom';

// function Navbar() {
//   const [scrolled, setScrolled] = useState(false);

//   useEffect(() => {
//     const handleScroll = () => {
//       setScrolled(window.scrollY > 50);
//     };
//     window.addEventListener('scroll', handleScroll);
//     return () => window.removeEventListener('scroll', handleScroll);
//   }, []);

//   return (
//     <nav
//       className={`fixed top-0 w-full z-50 transition-all duration-300 ${
//         scrolled ? 'bg-white/70 shadow-md backdrop-blur' : 'bg-white'
//       } border-b border-green-900`}
//     >
//       <div className="max-w-7xl mx-auto px-6 py-3 flex justify-between items-center">
//         <img
//           src="https://github.com/zasgar17/preFinalWebsite/blob/main/preFinal-Website/logoecom-removebg-preview.png?raw=true"
//           alt="Logo"
//           className="h-14"
//         />
//         <div className="space-x-6 text-lg">
//           {['Home', 'Events & Courses', 'About'].map((item, i) => (
//             <Link
//               key={i}
//               to={
//                 item === 'Home'
//                   ? '/'
//                   : item === 'About'
//                   ? '/about'
//                   : '/events-courses'
//               }
//               className="hover:underline hover:text-gray-900 transition"
//             >
//               {item}
//             </Link>
//           ))}
//         </div>
//       </div>
//     </nav>
//   );
// }

// export default Navbar;


import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom'; // 1. Import useNavigate
import { useAuth } from '../context/AuthContext'; // 2. Import useAuth hook

function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  
  // 3. Destructure auth state and functions
  const { isAuthenticated, isAdmin, user, logout } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 50);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // 4. Handle Logout Click
  const handleLogout = () => {
    logout();
    // Optional: Redirect to home page after logging out
    navigate('/'); 
  }

  return (
    <nav
      className={`fixed top-0 w-full z-50 transition-all duration-300 ${
        scrolled ? 'bg-white/70 shadow-md backdrop-blur' : 'bg-white'
      } border-b border-green-900`}
    >
      <div className="max-w-7xl mx-auto px-6 py-3 flex justify-between items-center">
        {/* Logo Section */}
        <img
          src="https://github.com/zasgar17/preFinalWebsite/blob/main/preFinal-Website/logoecom-removebg-preview.png?raw=true"
          alt="Logo"
          className="h-14"
        />
        
        {/* Navigation and Auth Section Combined */}
        <div className="flex items-center space-x-6 text-lg">
          {/* Main Links */}
          {['Home', 'Events & Courses', 'About'].map((item, i) => (
            <Link
              key={i}
              to={
                item === 'Home'
                  ? '/'
                  : item === 'About'
                  ? '/about'
                  : '/events-courses'
              }
              className="hover:underline hover:text-gray-900 transition font-medium"
            >
              {item}
            </Link>
          ))}
          

          {/* Admin button (admins only) */}
          {isAuthenticated && isAdmin && (
            <Link
              to="/admin"
              className="hover:underline hover:text-gray-900 transition font-medium"
            >
              Admin
            </Link>
          )}

          {/* 5. Conditional Authentication Button/Info */}
          {isAuthenticated ? (
            // Display if logged in
            <div className="flex items-center space-x-3 ml-6">
              <span className="text-sm font-semibold text-green-800">
                Hello, {user?.email || 'Member'}
              </span>
              <button
                onClick={handleLogout}
                className="px-4 py-2 text-sm font-semibold text-white bg-red-600 rounded-lg hover:bg-red-700 transition duration-150 shadow-md"
              >
                Logout
              </button>
            </div>
          ) : (
            // Display if logged out
            <Link 
              to="/login"
              className="ml-6 px-4 py-2 text-sm font-semibold text-white bg-green-700 rounded-lg hover:bg-green-800 transition duration-150 shadow-md"
            >
              Login
            </Link>
          )}
        </div>
      </div>
    </nav>
  );
}

export default Navbar;