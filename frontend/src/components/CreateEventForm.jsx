// frontend/src/components/CreateEventForm.jsx (FINAL & COMPLETE)

import React, { useState, useEffect } from 'react';
import { createEvent, updateEvent } from '../api/eventApi'; 

const initialFormData = {
    title: '',
    description: '',
    event_date: '',         // Date part (YYYY-MM-DD)
    event_time: '',         // Time part (HH:MM)
    location: '',
    capacity: 10,
    registration_deadline: '', // Datetime part (YYYY-MM-DDTHH:MM)
    image_url: '',
};

const CreateEventForm = ({ eventToEdit, isEditMode, onSuccess }) => {
    const [formData, setFormData] = useState(initialFormData);
    const [statusMessage, setStatusMessage] = useState(null); 
    const [isSubmitting, setIsSubmitting] = useState(false);

    // --- EFFECT: Pre-fill form data if in Edit Mode ---
    useEffect(() => {
        if (isEditMode && eventToEdit) {
            // Helper function to format ISO date/time string for input fields
            const formatForInput = (isoDateString) => {
                if (!isoDateString) return '';
                // The input type="datetime-local" expects 'YYYY-MM-DDTHH:MM'
                return isoDateString.substring(0, 16); 
            };

            // Event Date/Time requires splitting the event_date field from the response
            // The response event_date is a full datetime string from Pydantic/SQLAlchemy
            // We use the simpler event_date column (which is Date object in the DB but datetime string in Pydantic response)
            
            // 1. Get Date Part
            const fullEventDate = new Date(eventToEdit.event_date);
            // This grabs the YYYY-MM-DD part based on the date component
            const datePart = fullEventDate.toISOString().substring(0, 10); 
            
            // 2. Get Time Part
            // Use the event_time field from the response, which should be HH:MM:SS
            const timePart = eventToEdit.event_time ? eventToEdit.event_time.substring(0, 5) : ''; 

            setFormData({
                title: eventToEdit.title || '',
                description: eventToEdit.description || '',
                
                event_date: datePart,  
                event_time: timePart, 
                
                location: eventToEdit.location || '',
                capacity: eventToEdit.capacity || 10,
                
                // Registration Deadline uses the full datetime string
                registration_deadline: formatForInput(eventToEdit.registration_deadline), 
                
                image_url: eventToEdit.image_url || '',
            });
            setStatusMessage(null); 
        } else if (!isEditMode) {
            setFormData(initialFormData);
        }
    }, [isEditMode, eventToEdit]); 

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: type === 'checkbox' ? checked : (name === 'capacity' ? parseInt(value) : value),
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsSubmitting(true);
        setStatusMessage(null);

        // Combine date and time (YYYY-MM-DDT HH:MM:SS) for the event_date field
        const combinedEventDateTime = `${formData.event_date}T${formData.event_time}:00`; 
        
        // When updating, we only send the fields that should be changed, but for simplicity here,
        // we send the full set of inputs. The backend (FastAPI/Pydantic) handles this well.
        const dataToSend = {
            title: formData.title,
            description: formData.description,
            // The combined datetime string goes into the 'event_date' API field
            event_date: combinedEventDateTime, 
            location: formData.location,
            capacity: formData.capacity,
            registration_deadline: formData.registration_deadline, 
            image_url: formData.image_url || null,
        };
        
        // Basic Validation
        if (!dataToSend.title || !dataToSend.description || formData.event_date === '' || formData.event_time === '' || !dataToSend.registration_deadline) {
             setStatusMessage({ type: 'error', text: "Please fill in all required fields (Title, Description, Event Date, Event Time, Registration Deadline)." });
             setIsSubmitting(false);
             return;
        }

        try {
            let result;
            if (isEditMode) {
                // EDIT MODE: Use PUT request
                result = await updateEvent(eventToEdit.id, dataToSend); 
                setStatusMessage({ type: 'success', text: `Event '${result.title}' updated successfully!` });
            } else {
                // CREATE MODE: Use POST request
                result = await createEvent(dataToSend); 
                setStatusMessage({ type: 'success', text: `Event '${result.title}' created successfully!` });
                setFormData(initialFormData); // Clear the form only on successful creation
            }


            // Let parent refresh list / exit edit mode
            if (typeof onSuccess === 'function') {
                await onSuccess(result);
            }
            
        } catch (error) {
            let errorMessage = 'Failed to process event. Check your inputs.';
            if (error.response?.data?.detail) {
                errorMessage = typeof error.response.data.detail === 'string' 
                    ? error.response.data.detail
                    : Array.isArray(error.response.data.detail) 
                        ? error.response.data.detail.map(err => `${err.loc.join('.')}: ${err.msg}`).join(' | ')
                        : JSON.stringify(error.response.data.detail);
            } else if (error.message) {
                errorMessage = error.message;
            }
            console.error("Event error:", error);
            setStatusMessage({ type: 'error', text: errorMessage });
        } finally {
            setIsSubmitting(false);
        }
    };

    const submitButtonText = isEditMode 
        ? (isSubmitting ? 'Saving Changes...' : 'Save Changes')
        : (isSubmitting ? 'Creating...' : 'Create Event');
    
    return (
        <form onSubmit={handleSubmit} className="p-6 bg-white rounded-lg shadow-xl space-y-4">
            
            {/* Title */}
            <div>
                <label className="block text-sm font-medium text-gray-700">Title</label>
                <input 
                    type="text" 
                    name="title" 
                    value={formData.title} 
                    onChange={handleChange}
                    required
                    className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
                />
            </div>

            {/* Description */}
            <div>
                <label className="block text-sm font-medium text-gray-700">Description</label>
                <textarea 
                    name="description" 
                    value={formData.description} 
                    onChange={handleChange}
                    rows="4"
                    required
                    className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
                />
            </div>
            
            {/* --- Event Date, Time, and Location --- */}
            <div className="grid grid-cols-3 gap-4">
                {/* Event Date (YYYY-MM-DD) */}
                <div>
                    <label className="block text-sm font-medium text-gray-700">Event Date</label>
                    <input 
                        type="date" 
                        name="event_date" 
                        value={formData.event_date} 
                        onChange={handleChange}
                        required
                        className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
                    />
                </div>
                {/* Event Time (HH:MM) */}
                <div>
                    <label className="block text-sm font-medium text-gray-700">Event Time</label>
                    <input 
                        type="time" 
                        name="event_time" 
                        value={formData.event_time} 
                        onChange={handleChange}
                        required
                        className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
                    />
                </div>
                {/* Location */}
                <div>
                    <label className="block text-sm font-medium text-gray-700">Location</label>
                    <input 
                        type="text" 
                        name="location" 
                        value={formData.location} 
                        onChange={handleChange}
                        required
                        className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
                    />
                </div>
            </div>

            {/* --- Capacity and Registration Deadline --- */}
            <div className="grid grid-cols-2 gap-4">
                {/* Capacity */}
                <div>
                    <label className="block text-sm font-medium text-gray-700">Capacity</label>
                    <input 
                        type="number" 
                        name="capacity" 
                        value={formData.capacity} 
                        onChange={handleChange}
                        required
                        min="1"
                        className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
                    />
                </div>
                {/* Registration Deadline */}
                <div>
                    <label className="block text-sm font-medium text-gray-700">Registration Deadline</label>
                    <input 
                        type="datetime-local" 
                        name="registration_deadline" 
                        value={formData.registration_deadline} 
                        onChange={handleChange}
                        required
                        className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
                    />
                </div>
            </div>

             {/* Image URL */}
             <div>
                <label className="block text-sm font-medium text-gray-700">Image URL (Optional)</label>
                <input 
                    type="url" 
                    name="image_url" 
                    value={formData.image_url} 
                    onChange={handleChange}
                    className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
                />
            </div>

            {/* Status Message */}
            {statusMessage && (
                <div 
                    className={`p-3 text-sm rounded-md ${
                        statusMessage.type === 'success' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
                    }`}
                >
                    {statusMessage.text}
                </div>
            )}

            {/* Submit Button */}
            <button
                type="submit"
                disabled={isSubmitting}
                className={`w-full py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white transition duration-150 ${
                    isSubmitting
                        ? 'bg-indigo-400 cursor-not-allowed'
                        : isEditMode 
                            ? 'bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500' 
                            : 'bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500'
                }`}
            >
                {submitButtonText}
            </button>
            
            {/* Display event ID when editing for confirmation */}
            {isEditMode && <p className="text-sm text-center text-gray-500 mt-2">Editing Event ID: **{eventToEdit?.id}**</p>}
        </form>
    );
};

export default CreateEventForm;