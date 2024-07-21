import React, { useEffect, useState } from 'react';
import { getUser, followUser, unfollowUser, acceptFollowRequest, rejectFollowRequest, setProfilePrivacy } from '../../../../services/userService';
import styles from '../../pages/UserPage/index.module.css';
import { useParams } from 'react-router-dom';

interface User {
  full_name: string;
  username: string;
  email: string;
  birth_date: string;
  phone_number: string;
  address: string;
  gender: string;
  following: string[];
  follow_requests: string[];
  followers: string[];
  is_private: boolean;
  profile_picture: string;
}

const UserProfile = () => {
  const [user, setUser] = useState<User | null>(null);
  const [followUsername, setFollowUsername] = useState('');
  const [showFollowingModal, setShowFollowingModal] = useState(false);
  const [showFollowersModal, setShowFollowersModal] = useState(false);
  const [showFollowRequestsModal, setShowFollowRequestsModal] = useState(false);
  const { userId } = useParams<{ userId: string }>();

  useEffect(() => {
    const fetchUser = async () => {
      if (!userId) {
        console.error('userId is undefined');
        return;
      }
  
      const userData = await getUser(userId);
      setUser(userData.data);
    };
  
    fetchUser();
  }, [userId]);

  const handleFollow = async () => {
    if (!followUsername) {
      console.error('Follow username is empty');
      return;
    }
  
    if (!userId) {
      console.error('User ID is undefined');
      return;
    }
  
    // Prevent the user from following themselves
    if (user && followUsername === user.username) {
      console.error('User cannot follow themselves');
      return;
    }
  
    const result = await followUser(userId, followUsername);
    if (result) {
      setUser((prevUser) => {
        if (prevUser) {
          return {
            ...prevUser,
            following: [...prevUser.following, followUsername],
          };
        } else {
          return null;
        }
      });
    }
  };

  const handleUnfollow = async (usernameToUnfollow: string) => {
    if (!userId) {
      console.error('User ID is undefined');
      return;
    }
  
    await unfollowUser(userId, usernameToUnfollow);

    // Update the state of the component
    setUser((prevUser) => {
      if (prevUser) {
        return {
          ...prevUser,
          following: prevUser.following.filter(username => username !== usernameToUnfollow),
        };
      } else {
        return null;
      }
    });
  };

  const handleAcceptFollowRequest = async (requesterUsername: string) => {
    if (!userId) {
      console.error('User ID is undefined');
      return;
    }
  
    await acceptFollowRequest(userId, requesterUsername);

    // Update the state of the component
    setUser((prevUser) => {
      if (prevUser) {
        return {
          ...prevUser,
          follow_requests: prevUser.follow_requests.filter(username => username !== requesterUsername),
          followers: [...prevUser.followers, requesterUsername],
        };
      } else {
        return null;
      }
    });
  };

  const handleRejectFollowRequest = async (requesterUsername: string) => {
    if (!userId) {
      console.error('User ID is undefined');
      return;
    }
  
    await rejectFollowRequest(userId, requesterUsername);

    // Update the state of the component
    setUser((prevUser) => {
      if (prevUser) {
        return {
          ...prevUser,
          follow_requests: prevUser.follow_requests.filter(username => username !== requesterUsername),
        };
      } else {
        return null;
      }
    });
  };

  const handleShowFollowing = () => {
    setShowFollowingModal(true);
  };

  const handleShowFollowers = () => {
    setShowFollowersModal(true);
  };

  const handleShowFollowRequests = () => {
    setShowFollowRequestsModal(true);
  };

  const handleCloseModal = () => {
    setShowFollowingModal(false);
    setShowFollowersModal(false);
    setShowFollowRequestsModal(false);
  };

  const handleSwitchMode = async () => {
    if (!userId) {
      console.error('User ID is undefined');
      return;
    }
  
    if (!user) {
      console.error('User is null');
      return;
    }
  
    const result = await setProfilePrivacy(userId, !user.is_private);
    if (result) {
      setUser((prevUser) => {
        if (prevUser) {
          return {
            ...prevUser,
            is_private: !prevUser.is_private,
          };
        } else {
          return null;
        }
      });

      // If the profile is set to public, accept all follow requests
      if (user.is_private) {
        for (const requesterUsername of user.follow_requests) {
          await acceptFollowRequest(userId, requesterUsername);
        }
      }
    }
  };
  
  if (!user) {
    return <div>Loading...</div>;
  }

  return (
    <div className={styles.profile}>
      <div className={styles.left}>
        <img src={user.profile_picture} alt="Profile" className={styles.profilePicture} />
        <div className={styles.userInitialInfo}>
          <h2>@{user.username}</h2>
          <h4>{user.full_name}</h4>
          <p>{user.email}</p>
        </div>
        <div className={styles.userInfo}>
          <p><b>Birth Date: </b><em>{user.birth_date}</em></p>
          <p><b>Phone Number:</b><em> {user.phone_number}</em></p>
          <p><b>Gender:</b><em> {user.gender}</em></p>
          <p><b>Account Mode:</b><em> {user.is_private ? 'Private' : 'Public'}</em></p>
        </div>
      </div>
      <div className={styles.right}>
        <div className={styles.follow}>
          <button onClick={handleShowFollowing}><b>{user.following.length}</b> following</button>
          <button onClick={handleShowFollowers}><b>{user.followers.length}</b> followers</button>
        </div>
        {user.is_private && <button onClick={handleShowFollowRequests}>Show Follow Requests</button>}
        <div className={styles.followUserFunc}>
          <input
            type="text"
            placeholder="Enter username to follow"
            value={followUsername}
            onChange={(e) => setFollowUsername(e.target.value)}
          />
          <button onClick={handleFollow}>Follow</button>
        </div>
        <button onClick={handleSwitchMode}>Switch Mode</button>
      </div>
      {showFollowingModal && (
        <div className={styles.modal}>
          <h2>Following</h2>
          {user.following.map((username) => (
            <div key={username}>
              <p>{username}</p>
              <button onClick={() => handleUnfollow(username)}>Unfollow</button>
            </div>
          ))}
          <button onClick={handleCloseModal}>Close</button>
        </div>
      )}
      {showFollowersModal && (
        <div className={styles.modal}>
          <h2>Followers</h2>
          {user.followers.map((username) => (
            <div key={username}>
              <p>{username}</p>
              {/* Removed the unfollow button for followers */}
            </div>
          ))}
          <button onClick={handleCloseModal}>Close</button>
        </div>
      )}
      {showFollowRequestsModal && (
        <div className={styles.modal}>
          <h2>Follow Requests</h2>
          {user.follow_requests.map((username) => (
            <div key={username}>
              <p>{username}</p>
              <button onClick={() => handleAcceptFollowRequest(username)}>Accept</button>
              <button onClick={() => handleRejectFollowRequest(username)}>Reject</button>
            </div>
          ))}
          <button onClick={handleCloseModal}>Close</button>
        </div>
      )}
    </div>
  );
};

export default UserProfile;
