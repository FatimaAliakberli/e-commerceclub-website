import React from 'react';
import Slider from "react-slick";
import { Link } from "react-router-dom";

function Home() {
    const events = [
    {
      name: "E-Commerce Innovation Summit",
      date: "August 15, 2025",
      time: "2:00 PM – 5:30 PM (GMT+4)",
      location: "Main Auditorium & Zoom",
      keynote: `"The Future of E-Commerce: AI, AR & Automation"`,
      panel: `"Sustainable Supply Chains in E-Commerce"`,
      link: "https://htmlcolorcodes.com/colors/dark-red/"
    },
    {
      name: "Digital Marketing Masterclass",
      date: "September 10, 2025",
      time: "3:00 PM – 6:00 PM (GMT+4)",
      location: "Room 202, Tech Building & Zoom",
      keynote: `"Maximizing Conversions in 2025"`,
      panel: `"Emerging Tools for Student Entrepreneurs"`,
      link: "/events-courses"
    },
  ];
  return (
    
    <div className="pt-0">
      <Slider
    dots={true}
    infinite={true}
    speed={600}
    slidesToShow={1}
    slidesToScroll={1}
    autoplay={true}
    autoplaySpeed={3500}
    nextArrow={<SampleNextArrow />}
    prevArrow={<SamplePrevArrow />}
  >
    {[
      "https://github.com/zasgar17/preFinalWebsite/blob/main/preFinal-Website/ecom2.jpeg?raw=true",
      "https://github.com/zasgar17/preFinalWebsite/blob/main/preFinal-Website/ecom3.jpeg?raw=true",
      "https://github.com/zasgar17/preFinalWebsite/blob/main/preFinal-Website/ecom1.jpeg?raw=true",
      "https://github.com/zasgar17/preFinalWebsite/blob/main/preFinal-Website/ecom4.jpeg?raw=true",
      "https://github.com/zasgar17/preFinalWebsite/blob/main/preFinal-Website/ecom5.jpeg?raw=true",
      "https://github.com/zasgar17/preFinalWebsite/blob/main/preFinal-Website/ecom6.jpeg?raw=true",
    ].map((src, index) => (
      <div key={index}>
        <img src={src} alt={`Slide ${index + 1}`} className="w-full h-[600px] object-cover" />
      </div>
    ))}
  </Slider>
      {/* Banner */}
      <div className="text-center bg-[#2e5941] text-white py-6 px-4">
        <h1 className="text-4xl md:text-5xl font-bold  tracking-wide">
          WELCOME TO E-COMMERCE CLUB
        </h1>
      </div>

      {/* Intro Section */}
      <div className="bg-[#b5d6c7] px-6 md:px-20 py-12 text-center text-black">
        <p className="max-w-3xl mx-auto text-lg font-medium font-serif leading-7 tracking-wide">
          YOUR GO-TO HUB FOR EXPLORING THE <br />
          DIGITAL MARKETPLACE, SPARKING <br />
          INNOVATION, AND CONNECTING STUDENT <br />
          MINDS SHAPING THE FUTURE OF ONLINE <br />
          BUSINESS.
        </p>
      </div>

      {/* New Release Marquee */}
      <div className="bg-red-700 text-white py-2 overflow-hidden whitespace-nowrap">
        <marquee behavior="scroll" direction="left" className="text-sm font-semibold tracking-widest">
          🎉 New Release: Join our upcoming Innovation Summit | Masterclass in Digital Marketing | Collaboration with ADA Tech Clubs! 🎉
        </marquee>
      </div>

      {/* Feature Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 p-6 md:px-20 bg-[#f8f8f8]">
        {[
          {
            title: 'Masterclass on Dropshipping & Digital Marketing',
            content: 'Industry experts led a hands-on workshop covering product sourcing, SEO strategies, and conversion funnels tailored for student entrepreneurs.'
          },
          {
            title: 'E-Commerce Club Kicks Off with Innovation Mixer at ADA University',
            content: 'Students from various majors gathered to pitch digital business ideas, network with peers, and meet mentors from top e-commerce startups.'
          },
          {
            title: 'Collaboration Alert: E-Commerce Club Partners with ADA Tech & Business Clubs',
            content: 'A new initiative aims to launch a campus-wide virtual marketplace built by students, for students — combining tech, design, and business talent.'
          },
        ].map((item, idx) => (
          <div key={idx} className="shadow-lg rounded-md overflow-hidden">
            <div className="bg-green-900 text-white px-4 py-3 text-base font-bold font-serif">
              {item.title}
            </div>
            <div className="bg-white px-4 py-4 text-sm font-serif text-gray-700">
              {item.content}
            </div>
          </div>
        ))}
      </div>

      {/* Upcoming Events Section */}
      <div className="px-6 md:px-20 py-12 grid grid-cols-1 md:grid-cols-2 gap-6">
        {events.map((event, idx) => (
          <div key={idx} className="relative border rounded-lg shadow-lg p-6 bg-white">
            {/* See All link */}
            <Link
              to="/events-courses"
              className="absolute top-3 right-3 text-sm font-semibold text-red-900 hover:underline"
            >
              See All
            </Link>

            {/* Event Name */}
            <h2 className="text-2xl md:text-3xl font-bold mb-4 text-[#8B0000]">{event.name}</h2>

            {/* Event Details */}
            <ul className="list-disc pl-5 space-y-1 text-gray-700">
              <li><b>Date:</b> {event.date}</li>
              <li><b>Time:</b> {event.time}</li>
              <li><b>Location:</b> {event.location}</li>
              <li><b>Keynote:</b> {event.keynote}</li>
              <li><b>Panel:</b> {event.panel}</li>
            </ul>

            {/* Optional Button */}
            <div className="mt-4">
              <Link
                to={event.link}
                className="inline-block bg-red-800 text-white py-2 px-4 rounded hover:bg-red-900 transition"
              >
                Learn More
              </Link>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

// Slider Arrows
function SampleNextArrow(props) {
  const { onClick } = props;
  return (
    <div
      onClick={onClick}
      className="absolute top-1/2 right-4 transform -translate-y-1/2 z-10 cursor-pointer transition-opacity duration-300 opacity-30 hover:opacity-100 text-white text-4xl"
    >
      ❯
    </div>
  );
}

function SamplePrevArrow(props) {
  const { onClick } = props;
  return (
    <div
      onClick={onClick}
      className="absolute top-1/2 left-4 transform -translate-y-1/2 z-10 cursor-pointer transition-opacity duration-300 opacity-30 hover:opacity-100 text-white text-4xl"
    >
      ❮
    </div>);
    
    function SampleNextArrow(props) {
  const { onClick } = props;
  return (
    <div
      onClick={onClick}
      className="absolute top-1/2 right-4 transform -translate-y-1/2 z-10 cursor-pointer transition-opacity duration-300 opacity-30 hover:opacity-100 text-white text-4xl"
    >
      ❯
    </div>
  );
}

function SamplePrevArrow(props) {
  const { onClick } = props;
  return (
    <div
      onClick={onClick}
      className="absolute top-1/2 left-4 transform -translate-y-1/2 z-10 cursor-pointer transition-opacity duration-300 opacity-30 hover:opacity-100 text-white text-4xl"
    >
      ❮
    </div>
  );
}}
export default Home;