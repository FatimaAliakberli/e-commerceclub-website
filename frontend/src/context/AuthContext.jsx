// import React, { createContext, useState, useContext, useEffect } from 'react';
// import axiosInstance from '../utils/axiosInstance'; // Assuming this path

// // The context object itself
// const AuthContext = createContext(null);

// // =========================================================================
// // 1. AuthProvider Component
// // =========================================================================
// export const AuthProvider = ({ children }) => {
//     // 1.1 State for user data and token
//     const [user, setUser] = useState(null);
//     const [token, setToken] = useState(null);
//     const [loading, setLoading] = useState(true); // To prevent flashing before checking token

//     // 1.2 Persist Token and User on Load (useEffect)
//     useEffect(() => {
//         const storedToken = localStorage.getItem('jwt_token');
//         const storedUser = localStorage.getItem('user');

//         if (storedToken && storedUser) {
//             try {
//                 const userData = JSON.parse(storedUser);
//                 setToken(storedToken);
//                 setUser(userData);
//                 // Set the token in Axios header for subsequent requests
//                 setAxiosAuthHeader(storedToken);
//             } catch (error) {
//                 // Handle corrupted localStorage data
//                 console.error("Error parsing user data from localStorage:", error);
//                 // Optionally call logout here to clear corrupted data
//                 localStorage.removeItem('jwt_token');
//                 localStorage.removeItem('user');
//             }
//         }
//         setLoading(false);
//     }, []);

//     // 1.3 Helper function to set the Axios Authorization Header
//     const setAxiosAuthHeader = (jwtToken) => {
//         // Set the default Authorization header for all future requests
//         axiosInstance.defaults.headers.common['Authorization'] = `Bearer ${jwtToken}`;
//     };

//     // 1.4 Login Function (Remains the same)
//     const login = (userData, jwtToken) => {
//         // 1. Store the token and user data in local storage for persistence
//         localStorage.setItem('jwt_token', jwtToken);
//         localStorage.setItem('user', JSON.stringify(userData));
        
//         // 2. Update the state
//         setToken(jwtToken);
//         setUser(userData);
        
//         // 3. Configure Axios to use the token
//         setAxiosAuthHeader(jwtToken);
//     };

//     // 1.5 Logout Function (Remains the same)
//     const logout = () => {
//         // 1. Clear storage
//         localStorage.removeItem('jwt_token');
//         localStorage.removeItem('user');

//         // 2. Clear state
//         setToken(null);
//         setUser(null);
        
//         // 3. Clear the Axios header
//         delete axiosInstance.defaults.headers.common['Authorization'];
//     };

//     // 💥 CRITICAL ADDITION: Calculate isAdmin state 💥
//     const isAdmin = user 
//         ? (user.is_admin === true || user.is_admin === 1) 
//         : false;

//     // 1.6 Context Value (Publicly exposed data and functions)
//     const contextValue = {
//         user,
//         token,
//         isAuthenticated: !!token, // True if token exists
//         loading,
//         login,
//         logout,
        
//         // 💥 EXPOSE THE isAdmin FLAG 💥
//         isAdmin,
//     };

//     // Wait for the token check to finish before rendering the app
//     if (loading) {
//         return <div>Loading authentication...</div>;
//     }

//     return (
//         <AuthContext.Provider value={contextValue}>
//             {children}
//         </AuthContext.Provider>
//     );
// };

// // =========================================================================
// // 2. Custom Hook to use the context easily (Remains the same)
// // =========================================================================
// export const useAuth = () => {
//     const context = useContext(AuthContext);
//     if (!context) {
//         throw new Error('useAuth must be used within an AuthProvider');
//     }
//     return context;
// };


import React, { createContext, useState, useContext, useEffect } from 'react';
// Re-importing axiosInstance is recommended here for the initial /users/me check
import axiosInstance from '../utils/axiosInstance'; 

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [token, setToken] = useState(null);
    const [loading, setLoading] = useState(true); // Start as true

    // Function to check token validity and fetch user details from API
    const checkAuthStatus = async (storedToken, storedUser) => {
        if (storedToken && storedUser) {
            try {
                // 1. Temporarily set token for the immediate API call
                // Note: If you rely on the Interceptor, this step might be needed there too.
                // For simplicity here, let's assume the Interceptor is configured correctly 
                // and the token is available from the state/storage when the interceptor runs.
                
                // Fetch the current user data to ensure the token is valid and data is fresh.
                const response = await axiosInstance.get('/api/users/me', {
                    headers: {
                        Authorization: `Bearer ${storedToken}`
                    }
                });
                
                // If the call succeeds, the token is valid. Update state.
                setToken(storedToken);
                setUser(response.data); // This data will contain the fresh 'is_admin' status
                localStorage.setItem('user', JSON.stringify(response.data)); // Optional: Update stored user data
                
            } catch (error) {
                // Token is expired or invalid (API returned 401/403)
                console.error("Token validation failed. Logging out.", error);
                localStorage.removeItem('jwt_token');
                localStorage.removeItem('user');
                setToken(null);
                setUser(null);
            }
        }
        // CRITICAL: Ensure loading is set to false only AFTER the async check is complete.
        setLoading(false);
    };


    useEffect(() => {
        const storedToken = localStorage.getItem('jwt_token');
        const storedUser = localStorage.getItem('user');
        
        // Start the asynchronous check
        checkAuthStatus(storedToken, storedUser);
    }, []); // Run only once on mount


    // Login Function (remains mostly the same, ensuring we store the correct user object)
    const login = (userData, jwtToken) => {
        localStorage.setItem('jwt_token', jwtToken);
        localStorage.setItem('user', JSON.stringify(userData));
        setToken(jwtToken);
        setUser(userData);
        // Loading is not affected here as the user is actively logging in
    };

    // Logout Function (remains the same)
    const logout = () => {
        localStorage.removeItem('jwt_token');
        localStorage.removeItem('user');
        setToken(null);
        setUser(null);
    };

    // Calculate isAdmin state (This logic is perfect)
    const isAdmin = user 
        ? (user.is_admin === true || user.is_admin === 1) 
        : false;

    const contextValue = {
        user,
        token,
        isAuthenticated: !!token, 
        loading,
        login,
        logout,
        isAdmin,
    };

    // Wait for the token check to finish before rendering the app (This is now reliable)
    if (loading) {
        return <div className="text-center py-20">Loading authentication...</div>;
    }

    return (
        <AuthContext.Provider value={contextValue}>
            {children}
        </AuthContext.Provider>
    );
};
// =========================================================================
// 2. Custom Hook to use the context easily (Remains the same)
// =========================================================================
export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;

};
