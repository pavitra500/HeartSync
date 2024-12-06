import React, { useState } from 'react';
import axios from 'axios';
import './ProfileSearch.css'; // Make sure to update the CSS
import { useLocation, useNavigate } from 'react-router-dom';

const ProfileSearch = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [searchText, setSearchText] = useState('');
  const [profiles, setProfiles] = useState([]);
  const current_username = location.state?.username || 'default_username';

  // List of image filenames from the "images" folder
  const imageFilenames = [
    '1.jpg',
    '2.jpg',
    '3.jpg',
    '4.jpg',
    '5.jpg',
  ];

  const handleSearch = async () => {
    if (!searchText.trim()) {
      alert('Please enter some criteria for the profiles.');
      return;
    }

    try {
      const response = await axios.post(
        `http://localhost:5001/profiles_search/${current_username}`,
        { searchCriteria: searchText }
      );

      console.log('Profiles received:', response.data);

      if (response.data && response.data.profiles && response.data.profiles.length > 0) {
        setProfiles(response.data.profiles);
      } else {
        alert('No profiles found for the given criteria.');
        setProfiles([]);
      }
    } catch (error) {
      console.error('Error fetching profiles:', error);
      alert('An error occurred while fetching profiles. Please try again later.');
    }
  };

  const handleViewProfile = (username) => {
    navigate('/profile-details', { state: { username } });
  };

  return (
    <div className="profile-search-page">
      <h2>Search for Profiles</h2>
      <div className="search-container">
        <textarea
          className="search-textbox"
          placeholder="Enter what kind of profiles you want to see (e.g., 'gym enthusiasts in Houston')"
          value={searchText}
          onChange={(e) => setSearchText(e.target.value)}
        ></textarea>
        <button className="search-button" onClick={handleSearch}>
          Search
        </button>
      </div>

      <div className="results-container">
        <h3>Search Results</h3>
        {profiles.length > 0 ? (
          profiles.map((profile, index) => (
            <div className="profile-card" key={index}>
              {/* Circular Profile Picture */}
              <div className="profile-image-container">
              <img
                    className="profile-image"
                    src={`/images/${imageFilenames[index % imageFilenames.length]}`}
                    alt={`Profile of ${profile.username}`}
                    />
              </div>
              <h4>{profile.username}</h4>
              <p><strong>Age:</strong> {profile.age}</p>
              <p><strong>Score:</strong> {profile.Score}</p>
              <p><strong>Bio:</strong> {profile.essay0}</p>
              <p><strong>Score Analysis:</strong> {profile['Score Analysis']}</p>

            </div>
          ))
        ) : (
          <p>No profiles found. Try a different search.</p>
        )}
      </div>
    </div>
  );
};

export default ProfileSearch;
