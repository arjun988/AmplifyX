import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../contexts/authContext';
import ActivityLog from './ActivityLog';

const Dashboard = () => {
  const { logout, preferences } = useAuth();
  const navigate = useNavigate();
  const [sessionData, setSessionData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [paginationInfo, setPaginationInfo] = useState(null);

  const fetchSessionData = async (page = 1) => {
    try {
      const response = await axios.get(
        `http://localhost:5000/api/session?page=${page}`,
        { withCredentials: true }
      );
      setSessionData(response.data);
      setPaginationInfo(response.data.pagination);
    } catch (error) {
      setError('Error fetching session data');
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const logPageVisit = async () => {
      try {
        await axios.post('http://localhost:5000/api/session/page', 
          { page: 'dashboard' },
          { withCredentials: true }
        );
      } catch (error) {
        console.error('Error logging page visit:', error);
      }
    };

    logPageVisit();
    fetchSessionData(currentPage);
  }, [currentPage]);

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  const formatDuration = (seconds) => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}m ${remainingSeconds}s`;
  };

  const handlePageChange = (newPage) => {
    setCurrentPage(newPage);
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-bold">Squid Dashboard</h1>
            </div>
            <div className="flex items-center space-x-4">
              <Link 
                to="/preferences" 
                className="text-gray-700 hover:text-gray-900"
              >
                Preferences
              </Link>
              <button
                onClick={handleLogout}
                className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        {error && (
          <div className="mb-4 p-4 bg-red-100 text-red-700 rounded-md">
            {error}
          </div>
        )}

        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-2xl font-bold mb-4">Current Session</h2>
          {sessionData && (
            <div className="space-y-4">
              <div>
                <h3 className="text-lg font-medium">Session Duration</h3>
                <p>{formatDuration(sessionData.duration_seconds)}</p>
              </div>

              <div>
                <h3 className="text-lg font-medium">Current Preferences</h3>
                <ul className="mt-2 space-y-2">
                  <li>Theme: {preferences?.theme}</li>
                  <li>Notifications: {preferences?.notifications}</li>
                  <li>Language: {preferences?.language}</li>
                </ul>
              </div>

              <div>
                <h3 className="text-lg font-medium">Pages Visited</h3>
                <div className="mt-2 max-h-60 overflow-y-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Page
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Time
                        </th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {sessionData.pages_visited.map((visit, index) => (
                        <tr key={index}>
                          <td className="px-6 py-4 whitespace-nowrap">
                            {visit.page}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            {new Date(visit.timestamp).toLocaleTimeString()}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
                {paginationInfo && paginationInfo.total_pages > 1 && (
                  <div className="mt-4 flex justify-center space-x-2">
                    <button
                      onClick={() => handlePageChange(currentPage - 1)}
                      disabled={currentPage === 1}
                      className="px-3 py-1 rounded bg-gray-200 hover:bg-gray-300 disabled:opacity-50"
                    >
                      Previous
                    </button>
                    {Array.from({ length: paginationInfo.total_pages }, (_, i) => (
                      <button
                        key={i + 1}
                        onClick={() => handlePageChange(i + 1)}
                        className={`px-3 py-1 rounded ${
                          currentPage === i + 1
                            ? 'bg-blue-500 text-white'
                            : 'bg-gray-200 hover:bg-gray-300'
                        }`}
                      >
                        {i + 1}
                      </button>
                    ))}
                    <button
                      onClick={() => handlePageChange(currentPage + 1)}
                      disabled={currentPage === paginationInfo.total_pages}
                      className="px-3 py-1 rounded bg-gray-200 hover:bg-gray-300 disabled:opacity-50"
                    >
                      Next
                    </button>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>

        <div className="bg-white shadow rounded-lg p-6 mt-6">
          <ActivityLog />
        </div>
      </main>
    </div>
  );
};

export default Dashboard;