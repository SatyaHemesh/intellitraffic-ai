// frontend/src/hooks/useLiveTrafficData.js
import { useState, useEffect } from 'react';
import apiClient from '../api/client';

export const useLiveTrafficData = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await apiClient.get('/traffic/latest?limit=10');
        // Reverse the array so the oldest data is on the left of the chart
        setData(response.data.reverse());
        setError(null);
      } catch (err) {
        setError('Failed to fetch real-time traffic data.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
    // Poll the backend every 5 seconds
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, []);

  return { data, loading, error };
};