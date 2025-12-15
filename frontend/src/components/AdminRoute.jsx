// frontend/src/components/AdminRoute.jsx (Modified)
import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

// Note: Accept 'children' instead of 'element: Element'
const AdminRoute = ({ children }) => { 
    const { isAuthenticated, isAdmin, loading } = useAuth();
    
    // 💥 IMPORTANT DEBUG LOG 💥
    console.log(
        `[AdminRoute] Loading: ${loading}, Auth: ${isAuthenticated}, Admin: ${isAdmin}`
    );

    if (loading) {
        return <div className="text-center py-20">Loading authentication status...</div>;
    }

    if (isAuthenticated && isAdmin) {
        console.log("[AdminRoute] Access GRANTED.");
        // RENDER THE CHILDREN (which is <AdminDashboard />)
        return children; 
    }
    
    const redirectPath = isAuthenticated ? '/' : '/login';
    console.log(`[AdminRoute] Access DENIED. Redirecting to: ${redirectPath}`);

    return <Navigate to={redirectPath} replace />;
};

export default AdminRoute;
