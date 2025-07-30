# Reauth JWT Token Implementation

This implementation adds support for storing and using the reauth JWT token that the backend provides during login. The reauth token allows you to make authenticated requests without requiring the user to log in again.

## What was changed:

### 1. AuthContext Updates (`src/context/AuthContext.jsx`)
- Added `reauthToken` state variable
- Updated `login()` function to accept and store the reauth JWT token
- Added `getReauthHeaders()` helper function for making reauth requests
- Updates localStorage to store both auth token and reauth token
- Clears both tokens on logout

### 2. Login Components Updates
- **Login.jsx**: Updated to pass the reauth JWT when calling `login()`
- **CreateProfile.jsx**: Updated to pass the reauth JWT when calling `login()`

### 3. API Connection Updates (`src/api/connection.js`)
- Added `makeReauthRequest()` helper function
- Updated response interceptor to also clear reauth token on 401 errors

### 4. Custom Hook (`src/hooks/useReauth.js`)
- Created `useReauth()` hook for easy reauth requests across the application
- Automatically updates tokens if backend provides new ones
- Handles error cases gracefully

## How to use:

### Option 1: Using the useReauth hook (Recommended)
```jsx
import { useReauth } from '../hooks/useReauth';

function MyComponent() {
  const { makeReauthRequest } = useReauth();
  
  const fetchData = async () => {
    try {
      const response = await makeReauthRequest('/user', {}, 'GET');
      console.log('User data:', response.data);
    } catch (error) {
      console.error('Error:', error);
    }
  };
  
  return <button onClick={fetchData}>Fetch User Data</button>;
}
```

### Option 2: Using the AuthContext directly
```jsx
import { useAuth } from '../context/AuthContext';
import api from '../api/connection';

function MyComponent() {
  const { user, reauthToken } = useAuth();
  
  const fetchData = async () => {
    if (!reauthToken || !user?.id) {
      console.error('No reauth token available');
      return;
    }
    
    try {
      const response = await api.get('/user', {
        params: {
          type: 're',
          uid: user.id,
          reauth_jwt: reauthToken
        }
      });
      console.log('User data:', response.data);
    } catch (error) {
      console.error('Error:', error);
    }
  };
  
  return <button onClick={fetchData}>Fetch User Data</button>;
}
```

### Option 3: Using the makeReauthRequest helper from connection.js
```jsx
import { makeReauthRequest } from '../api/connection';

function MyComponent() {
  const fetchData = async () => {
    try {
      const response = await makeReauthRequest('/user', {}, 'GET');
      console.log('User data:', response.data);
    } catch (error) {
      console.error('Error:', error);
    }
  };
  
  return <button onClick={fetchData}>Fetch User Data</button>;
}
```

## Backend API Usage

When making reauth requests, the backend expects:
```json
{
  "type": "re",
  "uid": "user_id_here",
  "reauth_jwt": "jwt_token_here",
  // ... other request data
}
```

The backend will validate the reauth token and may return a new JWT token in the response, which will be automatically stored by the useReauth hook.

## Storage

- **authToken**: Main JWT token (for Authorization header)
- **reauthToken**: Reauth JWT token (for reauth requests)

Both are stored in localStorage and will persist across browser sessions until they expire or the user logs out.

## Security Notes

- Tokens are automatically cleared on logout
- Expired tokens are removed when detected
- 401 responses automatically clear both tokens and redirect to login
- Always use HTTPS in production to protect tokens in transit

## Example Component

See `src/components/ExampleReauthUsage.jsx` for a complete working example of how to use the reauth functionality.
