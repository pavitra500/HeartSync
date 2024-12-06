import React, { useEffect } from 'react';
import axios from 'axios';
import { useLocation, useNavigate } from 'react-router-dom';

function MainScreen() {
    const location = useLocation();
    const navigate = useNavigate();
    const username = location.state?.username; // Use optional chaining to prevent errors if state is null

    // Function to fetch from /reseti
    const resetCounter = async () => {
        try {
            const response = await axios.get(`http://localhost:5000/reseti`);
            const data = response.data; // Use response.data directly instead of response.json()
            console.log('Reset successful:', data);
        } catch (error) {
            console.error('Failed to reset counter:', error);
        }
    };

    useEffect(() => {
        resetCounter();
    }, []); // Empty dependency array to run only once

    const handleUpdatePreferences = () => {
        navigate('/preferences', { state: { username } });
    };

    const handleInbox = () => {
        navigate('/inbox', { state: { username } });
    };

    const handleShowProfiles = () => {
        navigate('/showprofiles', { state: { username } });
    };

    const handleChoice = () => {
        navigate('/choice', { state: { username } });
    };

    const handleViewProfile = () => {
        navigate('/profile', { state: { username } });
    };

    // Add navigation to ProfileSearch
    const handleSearchProfiles = () => {
        navigate('/profilesearch', { state: { username } });
    };

    return (
        <div>
            <h1>Welcome, {username}!</h1>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <button onClick={handleViewProfile} style={{ position: 'absolute', top: '50px', right: '10px' }}>
                    View Your Profile
                </button>
                <button onClick={handleUpdatePreferences}>
                    Must Haves
                </button>
                <div style={{ width: '10px', height: '20px', alignSelf: 'center' }} />
                <button onClick={handleInbox}>
                    Love Bot
                </button>
                <div style={{ width: '10px', height: '20px', alignSelf: 'center' }} />
                <button onClick={handleShowProfiles}>
                    Show Profiles
                </button>
                <div style={{ width: '10px', height: '20px', alignSelf: 'center' }} />
                <button onClick={handleChoice}>
                    Matchmaker's Choice
                </button>
                <div style={{ width: '10px', height: '20px', alignSelf: 'center' }} />
                <button onClick={handleSearchProfiles}>
                    Search Profiles
                </button>
            </div>
        </div>
    );
}

export default MainScreen;
