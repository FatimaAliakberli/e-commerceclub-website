// frontend/src/pages/EventDetailPage.jsx (FINAL UPDATE with handleModifyEvent)

import React, { useState, useEffect, useMemo } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import axiosInstance from '../utils/axiosInstance';
import { useAuth } from '../context/AuthContext'; 

const EventDetailPage = () => {
    // 1. Destructure ID and Hooks
    const { id } = useParams(); 
    const navigate = useNavigate(); // <-- Initialized here
    const { isAuthenticated, isAdmin } = useAuth(); 

    // 2. State Management
    const [event, setEvent] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [registrationsList, setRegistrationsList] = useState(null);
    const [regListError, setRegListError] = useState(null);
    // [Removed redundant registration status states for brevity]

    // --- Core Data Fetching Logic (Event Details) ---
    useEffect(() => {
        const fetchEvent = async () => {
            try {
                const response = await axiosInstance.get(`/api/events/${id}`);
                setEvent(response.data);
            } catch (err) {
                if (err.response && err.response.status === 404) {
                    setError(`Event with ID ${id} not found.`);
                } else {
                    setError("Failed to fetch event details.");
                }
            } finally {
                setLoading(false);
            }
        };
        fetchEvent();
    }, [id]);

    // --- Admin Data Fetch Logic (Registrations List) ---
    useEffect(() => {
        if (!isAuthenticated || !isAdmin) return; 

        const fetchRegistrations = async () => {
            try {
                setRegListError(null);
                // The endpoint to fetch all participants for an event (Admin only)
                const response = await axiosInstance.get(`/api/registrations/event/${id}/registrants`);
                setRegistrationsList(response.data);
            } catch (err) {
                console.error("Failed to fetch registrants:", err);
                setRegListError(err.response?.data?.detail || "Failed to load registrants list. Check backend access.");
            }
        };
        fetchRegistrations();
    }, [id, isAuthenticated, isAdmin]);

    // --- Helper for Display Formatting (Robust Date/Time Handling) ---
    const formattedEvent = useMemo(() => {
        if (!event) return null;

        const formatDateTime = (dateTimeString) => {
            if (!dateTimeString) return 'TBD';
            const date = new Date(dateTimeString); 
            if (isNaN(date.getTime())) return 'Date Error';
            
            return date.toLocaleDateString('en-US', { 
                year: 'numeric', 
                month: 'long', 
                day: 'numeric' 
            });
        };
        
        const formatTime = (timeString) => {
            // event.event_time from backend is HH:MM:SS, we display HH:MM
            const timePart = event.event_time?.substring(0, 5) || 'TBD'; 
            return timePart === 'TBD' ? 'Time TBD' : `${timePart} (GMT+4)`;
        };
        
        const formatDeadline = (dateTimeString) => {
            if (!dateTimeString) return 'TBD';
            const date = new Date(dateTimeString);
            if (isNaN(date.getTime())) return 'Deadline Error';
            
            const datePart = date.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
            const timePart = date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
            return `${datePart} at ${timePart}`;
        };
        
        return {
            ...event,
            displayDate: formatDateTime(event.event_date),
            displayTime: formatTime(event.event_time),
            displayDeadline: formatDeadline(event.registration_deadline),
        };
    }, [event]);

    // --- 💥 FIX: Define the missing handleModifyEvent function (Around line 100) 💥
    const handleModifyEvent = () => {
        if (!isAdmin) {
            alert("Only administrators can modify events.");
            return;
        }
        // Redirects to /admin?editId={id} to launch the CreateEventForm in Edit Mode
        // This is the implementation needed to resolve the ReferenceError at the button click.
        navigate(`/admin?editId=${id}`);
    };
    // ---------------------------------------------------------------------------------


    // --- Conditional Rendering for Loading/Error States ---
    if (loading) return <div className="text-center py-20">Loading event details...</div>;
    if (error) return <div className="text-center py-20 text-red-600">{error}</div>;
    if (!formattedEvent) return <div className="text-center py-20">Event not found.</div>;


    // --- Admin Registrant Table Component ---
    const AdminRegistrantsTable = () => {
        if (regListError) {
            return <div className="p-4 text-red-600 bg-red-100 rounded border border-red-200">
                ⚠️ Error loading registrants list: {regListError}
            </div>;
        }
        // If data is still null, but no error, show loading
        if (registrationsList === null) {
            return <div className="text-gray-500 py-4">Loading registrants list...</div>;
        }

        const registeredUsersCount = registrationsList.filter(reg => !reg.is_cancelled).length;

        return (
            <div className="p-4 bg-white border border-gray-200 rounded-lg shadow-xl mt-8">
                <h3 className="text-2xl font-bold text-gray-900 mb-4">👥 Registered Users ({registeredUsersCount})</h3>
                
                {registrationsList.length === 0 ? (
                    <p className="text-gray-500">No one has registered for this event yet.</p>
                ) : (
                    <div className="overflow-x-auto">
                        <table className="min-w-full divide-y divide-gray-200">
                            <thead className="bg-gray-50">
                                <tr>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Full Name</th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Registered At</th>
                                </tr>
                            </thead>
                            <tbody className="bg-white divide-y divide-gray-200">
                                {registrationsList.map((reg) => (
                                    <tr key={reg.id} className={reg.is_cancelled ? 'bg-red-50 opacity-70' : ''}>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                                            {reg.user?.full_name || 'N/A (User Missing)'}
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-indigo-600">
                                            {reg.user?.email || 'N/A'}
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm">
                                            {reg.is_cancelled ? <span className="text-red-600 font-semibold">Cancelled</span> : <span className="text-green-600">Active</span>}
                                        </td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                            {new Date(reg.registered_at).toLocaleDateString()}
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>
        );
    };

    // --- Conditional Registration Section ---
    const registrationLinkPath = `/register/event/${formattedEvent.id}`;
    
    const registrationSection = isAdmin ? (
        <AdminRegistrantsTable />
    ) : (
        // Standard User View
        <Link 
            to={registrationLinkPath} 
            className="inline-block bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3 px-8 rounded-lg transition duration-150 shadow-md hover:shadow-lg"
        >
            Register for this Event
        </Link>
    );

    // --- Admin Action Button Section (Uses handleModifyEvent) ---
    const adminActionSection = isAdmin ? (
        <div className="mt-8 pt-6 border-t border-gray-200">
            <h3 className="text-xl font-bold text-gray-800 mb-4">Admin Actions</h3>
            <button
                // 💥 Calls the newly defined function 💥
                onClick={handleModifyEvent} 
                className="bg-purple-600 hover:bg-purple-700 text-white font-bold py-2 px-6 rounded-lg transition duration-150 shadow-md hover:shadow-lg"
            >
                ✏️ Modify This Event
            </button>
            {/* Future: Add delete button, toggle active status, etc. */}
        </div>
    ) : null;


    // --- Render the Event Detail UI ---
    return (
        <div className="max-w-4xl mx-auto py-12 px-4">
            <h1 className="text-4xl font-extrabold text-gray-900 mb-4">{formattedEvent.title}</h1>
            
            {/* Display Image if URL exists */}
            {formattedEvent.image_url && (
                <div className="mb-6 rounded-lg overflow-hidden shadow-xl">
                    <img 
                        src={formattedEvent.image_url} 
                        alt={formattedEvent.title} 
                        className="w-full h-96 object-cover"
                    />
                </div>
            )}

            <p className="text-lg text-gray-600 mb-8 whitespace-pre-line">{formattedEvent.description}</p>

            {/* Event Meta Data */}
            <div className="space-y-4 mb-8 p-6 bg-gray-50 rounded-lg shadow-sm border-l-4 border-indigo-500">
                <p className="text-xl font-bold text-gray-900">Details</p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <p className="font-semibold text-gray-700">🗓️ Event Date:</p>
                    <p className="text-indigo-600">{formattedEvent.displayDate}</p>

                    <p className="font-semibold text-gray-700">⏱️ Event Time:</p>
                    <p className="text-indigo-600">{formattedEvent.displayTime}</p>

                    <p className="font-semibold text-gray-700">📍 Location:</p>
                    <p className="text-indigo-600">{formattedEvent.location || 'Online'}</p>

                    <p className="font-semibold text-gray-700">⛔ Registration Deadline:</p>
                    <p className="text-red-500">{formattedEvent.displayDeadline}</p>
                    
                    <p className="font-semibold text-gray-700">👥 Capacity:</p>
                    <p className="text-indigo-600">{formattedEvent.current_registrations} / {formattedEvent.capacity}</p>
                </div>
            </div>
            
            {/* Registration/Admin Section */}
            <div className="mt-8">
                {registrationSection}
            </div>

            {/* Admin Modify Button Section */}
            {adminActionSection}

            {/* Back to Events Link */}
            <div className="mt-10">
                <Link to="/events-courses" className="text-indigo-600 hover:text-indigo-800 font-medium">
                    ← Back to all Events & Courses
                </Link>
            </div>
        </div>
    );
};


export default EventDetailPage;
