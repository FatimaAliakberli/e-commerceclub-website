import { useState } from 'react';

// Updated team data with category and roleType
const team = [
  {
    name: 'Maryam Valiyeva',
    image: 'https://github.com/zasgar17/pics/blob/main/WhatsApp%20Image%202025-07-31%20at%2015.00.34.jpeg?raw=true',
    position: 'President',
    category: 'General Directors',
    roleType: 'head',
  },
  {
    name: 'Jeyhun Gasimzade',
    image: 'https://github.com/zasgar17/pics/blob/main/PHOTO-2025-02-27-23-28-43.jpg?raw=true',
    position: 'Founder',
    category: 'General Directors',
    roleType: 'head',
  },
  {
    name: 'Mehriban Huseyinli',
    image: 'https://github.com/zasgar17/pics/blob/main/IMG_7213_anonymous.jpg?raw=true',
    position: 'Head Manager',
    category: 'HR Group',
    roleType: 'head',
  },
  {
    name: 'Baba Alizada',
    image: 'https://github.com/zasgar17/pics/blob/main/PHOTO-2025-03-05-18-35-02.jpg?raw=true',
    position: 'Head Manager',
    category: 'HR Group',
    roleType: 'head',
  },
  {
    name: 'Jeyhana Huseyinli',
    image: 'https://github.com/zasgar17/pics/blob/main/IMG_9623_anonymous.jpg?raw=true',
    position: 'HR Manager',
    category: 'HR Group',
    roleType: 'staff',
  },
  {
    name: 'Aysel Israfilzade',
    image: 'https://github.com/zasgar17/pics/blob/main/dd89f50c-96d5-4528-ab78-a0d9ce31bcb2_anonymous.jpg?raw=true',
    position: 'HR Manager',
    category: 'HR Group',
    roleType: 'staff',
  },
  {
    name: 'Aisha Salmanova',
    image: 'https://github.com/zasgar17/pics/blob/main/ecom%20photo_anonymous.jpg?raw=true',
    position: 'Head of SMM',
    category: 'SMM Group',
    roleType: 'head',
  },
  {
    name: 'Nazrin Huseyinli',
    image: 'https://github.com/zasgar17/pics/blob/main/IMG_6022_anonymous.jpg?raw=true',
    position: 'SMM',
    category: 'SMM Group',
    roleType: 'staff',
  },
  {
    name: 'Farah Amrahova',
    image: 'https://github.com/zasgar17/pics/blob/main/IMG_5109_anonymous.jpg?raw=true',
    position: 'SMM',
    category: 'SMM Group',
    roleType: 'staff',
  },
  // ... Add the rest with category + roleType
];

function AboutUs() {
  const [hovered, setHovered] = useState(null);

  // Group members by category
  const categories = [...new Set(team.map(member => member.category))];

  return (
    <div className="pt-24 px-4 max-w-7xl mx-auto text-center">
      <h1 className="text-3xl md:text-4xl font-bold mb-10">Meet Our Team</h1>
      {categories.map(category => {
        // Get members for this category
        const categoryMembers = team.filter(m => m.category === category);
        // Heads first, then staff
        const sortedMembers = [
          ...categoryMembers.filter(m => m.roleType === 'head'),
          ...categoryMembers.filter(m => m.roleType === 'staff')
        ];

        return (
          <div key={category} className="mb-12">
            <h2 className="text-2xl font-semibold mb-6">{category}</h2>
            <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6 justify-center">
              {sortedMembers.map((member, index) => (
                <div
                  key={index}
                  onMouseEnter={() => setHovered(`${category}-${index}`)}
                  onMouseLeave={() => setHovered(null)}
                  className="relative group cursor-pointer transition-transform duration-300 transform hover:scale-105 mx-auto"
                >
                  <img
                    src={member.image}
                    alt={member.name}
                    className="w-full h-48 object-cover rounded-xl shadow-md"
                  />
                  {hovered === `${category}-${index}` && (
                    <div className="absolute inset-0 bg-black/60 text-white p-3 flex flex-col justify-center rounded-xl">
                      <h2 className="text-sm font-bold">{member.name}</h2>
                      <p className="text-xs italic">{member.position}</p>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        );
      })}
    </div>
  );
}

export default AboutUs;