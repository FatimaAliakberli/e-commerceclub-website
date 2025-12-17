// frontend/src/pages/AdminDashboard.jsx

import React, { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';

import CreateEventForm from '../components/CreateEventForm';
import { fetchEvents, fetchEventById, deleteEvent } from '../api/eventApi';

const AdminDashboard = () => {
    const navigate = useNavigate();
    const [searchParams] = useSearchParams();

    const editId = searchParams.get('editId'); // string or null
    const isEditMode = Boolean(editId);

    // Edit-mode state
    const [eventToEdit, setEventToEdit] = useState(null);
    const [loadingEvent, setLoadingEvent] = useState(false);
    const [fetchError, setFetchError] = useState(null);

    // List state
    const [events, setEvents] = useState([]);
    const [loadingList, setLoadingList] = useState(false);

    const loadEvents = async () => {
        setLoadingList(true);
        try {
            const data = await fetchEvents(true, true); // include_past + include_inactive
            setEvents(data?.events || []);
        } catch (err) {
            console.error('Error loading events list:', err);
        } finally {
            setLoadingList(false);
        }
    };

    const loadEventForEdit = async (id) => {
        if (!id) {
            setEventToEdit(null);
            return;
        }

        setLoadingEvent(true);
        setFetchError(null);

        try {
            const data = await fetchEventById(id);
            setEventToEdit(data);
        } catch (err) {
            console.error('Error fetching event for editing:', err);
            setFetchError(`Failed to load event ID ${id} for editing.`);
        } finally {
            setLoadingEvent(false);
        }
    };

    // Load list once
    useEffect(() => {
        loadEvents();
    }, []);

    // Load edit event when editId changes
    useEffect(() => {
        loadEventForEdit(editId);
    }, [editId]);

    const handleEdit = (id) => navigate(`/admin?editId=${id}`);

    const handleDelete = async (id) => {
        const ok = window.confirm('Delete this event? This cannot be undone.');
        if (!ok) return;

        try {
            await deleteEvent(id);
            await loadEvents();

            // If you deleted the event currently in edit mode, exit edit mode.
            if (String(editId) === String(id)) {
                navigate('/admin');
            }
        } catch (err) {
            console.error('Error deleting event:', err);
            alert('Failed to delete event. Check console for details.');
        }
    };

    const title = isEditMode ? `Edit Event (ID: ${editId})` : 'Create New Event/Course';

    if (loadingEvent) {
        return (
            <div className="max-w-4xl mx-auto py-12 px-4 text-center">
                Loading event details for modification...
            </div>
        );
    }

    if (fetchError) {
        return (
            <div className="max-w-4xl mx-auto py-12 px-4 text-center text-red-600">
                {fetchError}
            </div>
        );
    }

    return (
        <div className="max-w-4xl mx-auto py-12 px-4">
            <h1 className="text-4xl font-bold text-indigo-700 mb-8 border-b pb-2">
                Admin Dashboard
            </h1>

            <section className="mb-12">
                <h2 className="text-3xl font-semibold text-gray-800 mb-6">
                    {title}
                </h2>

                <CreateEventForm
                    eventToEdit={eventToEdit}
                    isEditMode={isEditMode}
                    onSuccess={async () => {
                        await loadEvents();
                        navigate('/admin'); // exit edit mode after save
                    }}
                />
            </section>

            <section>
                <h2 className="text-3xl font-semibold text-gray-800 mb-6">
                    Manage Existing Events
                </h2>

                {loadingList ? (
                    <p className="text-gray-600">Loading events...</p>
                ) : events.length === 0 ? (
                    <p className="text-gray-600">No events found.</p>
                ) : (
                    <div className="space-y-3">
                        {events.map((e) => (
                            <div
                                key={e.id}
                                className="p-4 bg-white rounded shadow flex justify-between items-center"
                            >
                                <div>
                                    <div className="font-semibold">{e.title}</div>
                                    <div className="text-sm text-gray-600">
                                        ID: {e.id}
                                    </div>
                                </div>

                                <div className="flex gap-2">
                                    <button
                                        onClick={() => handleEdit(e.id)}
                                        className="px-3 py-2 bg-blue-600 text-white rounded"
                                    >
                                        Edit
                                    </button>

                                    <button
                                        onClick={() => handleDelete(e.id)}
                                        className="px-3 py-2 bg-red-600 text-white rounded"
                                    >
                                        Delete
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </section>
        </div>
    );
};

export default AdminDashboard;
