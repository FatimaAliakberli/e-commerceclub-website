import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

function Navbar() {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 50);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <nav
      className={`fixed top-0 w-full z-50 transition-all duration-300 ${
        scrolled ? 'bg-white/70 shadow-md backdrop-blur' : 'bg-white'
      } border-b border-green-900`}
    >
      <div className="max-w-7xl mx-auto px-6 py-3 flex justify-between items-center">
        <img
          src="https://github.com/zasgar17/preFinalWebsite/blob/main/preFinal-Website/logoecom-removebg-preview.png?raw=true"
          alt="Logo"
          className="h-14"
        />
        <div className="space-x-6 text-lg">
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
              className="hover:underline hover:text-gray-900 transition"
            >
              {item}
            </Link>
          ))}
        </div>
      </div>
    </nav>
  );
}

export default Navbar;