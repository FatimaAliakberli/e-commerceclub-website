// frontend/src/api/eventApi.js (UPDATED)

import axiosInstance from '../utils/axiosInstance'; 

/**
 * Sends a POST request to the protected endpoint to create a new event.
 * @param {object} eventData - The data for the new event.
 * @returns {Promise<object>} The created event object.
 */
export const createEvent = async (eventData) => {
    const response = await axiosInstance.post('/api/events/', eventData); 
    return response.data;
};

/**
 * Sends a GET request to fetch a list of events from the API.
 * @param {boolean} includePast - Whether to include past events.
 * @param {boolean} includeInactive - Whether to include inactive events.
 * @returns {Promise<object>} The event list response object containing 'events', 'total', etc.
 */
export const fetchEvents = async (includePast = false, includeInactive = false) => {
    const response = await axiosInstance.get('/api/events/', {
        params: {
            // We set the page size to a large number to get all events in one go for simple filtering
            page_size: 100, 
            include_past: includePast,
            include_inactive: includeInactive,
        }
    });
    return response.data;
};

/**
 * Sends a PUT request to the protected endpoint to update an existing event.
 * @param {number} eventId - The ID of the event to update.
 * @param {object} eventData - The updated data for the event.
 * @returns {Promise<object>} The updated event object.
 */
// 💥 NEW FUNCTION FOR UPDATING EVENTS 💥
export const updateEvent = async (eventId, eventData) => {
    // Note: FastAPI uses PUT for full updates on the resource path
    const response = await axiosInstance.put(`/api/events/${eventId}`, eventData); 
    return response.data;
};



/**
 * Fetch a single event by ID (used for Edit mode).
 * @param {number|string} eventId
 * @returns {Promise<object>} The event object.
 */
export const fetchEventById = async (eventId) => {
    const response = await axiosInstance.get(`/api/events/${eventId}`);
    return response.data;
};

/**
 * Delete an event by ID (admin only).
 * @param {number|string} eventId
 * @returns {Promise<object>} API response (if any).
 */
export const deleteEvent = async (eventId) => {
    const response = await axiosInstance.delete(`/api/events/${eventId}`);
    return response.data;
};

// You can add other functions here later (e.g., fetchAdminEvents)
