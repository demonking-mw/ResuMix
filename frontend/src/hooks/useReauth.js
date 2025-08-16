// src/hooks/useReauth.js
import { useAuth } from '../context/AuthContext';
import api from '../api/connection';

export const useReauth = () => {
  const { user, reauthToken, login } = useAuth();

  const makeReauthRequest = async (url, data = {}, method = 'GET') => {
    console.log('Making reauth request to:', url, 'with data:', data, 'and method:', method);
    if (!reauthToken || !user?.id) {
      throw new Error('No reauth token or user ID available');
    }

    const requestData = {
      ...data,
      type: 're',
      uid: user.id,
      reauth_jwt: reauthToken
    };

    try {
      let response;
      if (method.toLowerCase() === 'post') {
        response = await api.post(url, requestData);
      } else if (method.toLowerCase() === 'get') {
        response = await api.get(url, { params: requestData });
      } else {
        response = await api.request({
          method: method,
          url: url,
          data: requestData
        });
      }

      // If the response contains a new JWT, update it in the auth context
      if (response.data?.jwt) {
        login(response.data.jwt, user, response.data.jwt);
      }

      return response;
    } catch (error) {
      console.error('Error making reauth request:', error);
      throw error;
    }
  };

  return { makeReauthRequest };
};
