import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ActivityLog = () => {
  const [activities, setActivities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [pagination, setPagination] = useState({
    current_page: 1,
    per_page: 10,
    total_pages: 1,
    total_items: 0
  });

  const fetchActivities = async (page = 1) => {
    try {
      const response = await axios.get(`http://localhost:5000/api/activities?page=${page}`, {
        withCredentials: true
      });
      setActivities(response.data.activities);
      setPagination(response.data.pagination);
      setError('');
    } catch (err) {
      setError('Failed to load activities');
      console.error('Error fetching activities:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchActivities();
  }, []);

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleString();
  };

  const renderPagination = () => {
    const pages = [];
    for (let i = 1; i <= pagination.total_pages; i++) {
      pages.push(
        <button
          key={i}
          onClick={() => fetchActivities(i)}
          className={`px-3 py-1 mx-1 rounded ${
            pagination.current_page === i
              ? 'bg-blue-500 text-white'
              : 'bg-gray-200 hover:bg-gray-300'
          }`}
        >
          {i}
        </button>
      );
    }
    return pages;
  };

  if (loading) {
    return <div className="text-center py-4">Loading activities...</div>;
  }

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-medium">Activity Log</h3>
      {error && (
        <div className="bg-red-100 text-red-700 p-3 rounded">{error}</div>
      )}
      <div className="space-y-2">
        {activities.map((activity, index) => (
          <div
            key={index}
            className="p-3 bg-gray-50 rounded border border-gray-200"
          >
            <div className="flex justify-between">
              <span className="font-medium">{activity.action}</span>
              <span className="text-sm text-gray-500">
                {formatTimestamp(activity.timestamp)}
              </span>
            </div>
            {activity.details && (
              <div className="mt-1 text-sm text-gray-600">
                {JSON.stringify(activity.details)}
              </div>
            )}
          </div>
        ))}
      </div>
      <div className="flex justify-center mt-4">{renderPagination()}</div>
    </div>
  );
};
export default ActivityLog