import React, { useState } from "react";

const upcomingEvents = [
  {
    name: "E-Commerce Innovation Summit",
    date: "August 15, 2025",
    time: "2:00 PM – 5:30 PM (GMT+4)",
    location: "Main Auditorium & Zoom",
    keynote: `"The Future of E-Commerce: AI, AR & Automation"`,
    panel: `"Sustainable Supply Chains in E-Commerce"`,
  },
  {
    name: "Digital Marketing Masterclass",
    date: "September 10, 2025",
    time: "3:00 PM – 6:00 PM (GMT+4)",
    location: "Room 202, Tech Building & Zoom",
    keynote: `"Maximizing Conversions in 2025"`,
    panel: `"Emerging Tools for Student Entrepreneurs"`,
  },
];

const pastEvents = [
  {
    name: "E-Commerce Networking Meetup",
    date: "June 12, 2025",
    time: "1:00 PM – 4:00 PM (GMT+4)",
    location: "Main Auditorium & Zoom",
    keynote: `"Building Student-Led E-Commerce Platforms"`,
    panel: `"Tech Meets Business: Success Stories"`,
  },
  {
    name: "Startup Pitch Night",
    date: "May 25, 2025",
    time: "5:00 PM – 8:00 PM (GMT+4)",
    location: "Room 101, Innovation Hub",
    keynote: `"Pitch Perfect: Tips for Students"`,
    panel: `"Investor Feedback & Networking"`,
  },
];

function EventCourses() {
  const [activeTab, setActiveTab] = useState("upcoming");
  const eventsToShow = activeTab === "upcoming" ? upcomingEvents : pastEvents;

  return (
    <div className="pt-10 pb-20 min-h-screen bg-[#0000] text-white">
      <div className="px-6 md:px-20 py-8">
        <h1 className="text-4xl md:text-5xl font-bold text-green-900 mb-6">
          Events & Courses
        </h1>

        {/* Tabs */}
        <div className="flex gap-4 mb-8 border-b border-green-800">
          <button
            onClick={() => setActiveTab("upcoming")}
            className={`py-2 px-4 font-semibold rounded-t-lg transition ${
              activeTab === "upcoming"
                ? "bg-green-800 text-white"
                : "text-green-900 hover:bg-green-900 hover:bg-opacity-20"
            }`}
          >
            Upcoming Events
          </button>
          <button
            onClick={() => setActiveTab("past")}
            className={`py-2 px-4 font-semibold rounded-t-lg transition ${
              activeTab === "past"
                ? "bg-green-800 text-white"
                : "text-green-900 hover:bg-green-900 hover:bg-opacity-20"
            }`}
          >
            Past Events
          </button>
        </div>

        {/* Event Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {eventsToShow.map((event, idx) => (
            <div
              key={idx}
              className="relative bg-[#0000] border border-red-900 rounded-lg shadow-lg p-6 hover:scale-[1.02] transition transform"
            >
              <h2 className="text-2xl md:text-3xl font-bold mb-3 text-red-800">
                {event.name}
              </h2>
              <ul className="list-disc pl-5 space-y-1 text-black">
                <li><b>Date:</b> {event.date}</li>
                <li><b>Time:</b> {event.time}</li>
                <li><b>Location:</b> {event.location}</li>
                <li><b>Keynote:</b> {event.keynote}</li>
                <li><b>Panel:</b> {event.panel}</li>
              </ul>
              <button className="mt-4 bg-red-800 text-white font-semibold py-2 px-4 rounded hover:bg-red-900 transition">
                Learn More
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default EventCourses;