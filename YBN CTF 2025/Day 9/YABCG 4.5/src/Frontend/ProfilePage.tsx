import { useEffect, useState } from "react";
import { supabase } from "../lib/supabase";
import { BusinessCardList } from './BusinessCardList';

export function ProfilePage() {
  const params = new URLSearchParams(window.location.search);
  const token = params.get("token");
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!token) {
      setError("No profile token found in URL");
      setLoading(false);
      return;
    }

    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        
        const { data: profileData, error: fetchError } = await supabase.functions.invoke('view_profile', {
          body: { token }
        });

        if (fetchError) throw fetchError;
        setData(Array.isArray(profileData) ? profileData : [profileData]);
      } catch (err: any) {
        setError(err.message || 'Failed to load profile');
        console.error('Profile fetch error:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [token]);

  // Handle missing token case
  if (!token) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 p-4">
        <div className="text-center p-8 bg-white rounded-xl shadow-md max-w-md w-full">
          <div className="text-6xl mb-4">📎</div>
          <h1 className="text-2xl font-bold text-gray-800 mb-2">Missing Profile Token</h1>
          <p className="text-gray-600 mb-4">
            This profile link appears to be incomplete. Please check the URL or contact the profile owner.
          </p>
          <div className="text-sm text-gray-500 mt-4">
            Expected format: ?token=your_token_here
          </div>
        </div>
      </div>
    );
  }

  // Loading state
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-16 w-16 border-b-2 border-indigo-600 mb-4"></div>
          <p className="text-gray-600">Loading profile...</p>
        </div>
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 p-4">
        <div className="text-center p-8 bg-white rounded-xl shadow-md max-w-md w-full">
          <div className="text-6xl mb-4">⚠️</div>
          <h1 className="text-2xl font-bold text-gray-800 mb-2">Profile Error</h1>
          <p className="text-red-600 mb-4">{error}</p>
          <button 
            onClick={() => window.location.reload()}
            className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition"
          >
            Retry Loading
          </button>
        </div>
      </div>
    );
  }

  // Empty data state
  if (data.length === 0) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 p-4">
        <div className="text-center p-8 bg-white rounded-xl shadow-md max-w-md w-full">
          <div className="text-6xl mb-4">📁</div>
          <h1 className="text-2xl font-bold text-gray-800 mb-2">No Profile Data</h1>
          <p className="text-gray-600">
            The profile exists but contains no business card information.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-10">
          <div className="inline-block p-3 bg-indigo-100 rounded-full mb-4">
            <div className="text-3xl">🆔</div>
          </div>
          <h1 className="text-3xl font-extrabold text-gray-900 sm:text-4xl">
            Profile Information
          </h1>
          <p className="mt-4 text-xl text-gray-600 max-w-2xl mx-auto">
            Viewing profile associated with token: <span className="font-mono text-indigo-600">{token.slice(0, 8)}...</span>
          </p>
        </div>

        <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
          <div className="border-b border-gray-200 bg-indigo-50 px-6 py-4">
            <h2 className="text-lg font-semibold text-indigo-900 flex items-center">
              <span className="w-2 h-2 bg-indigo-500 rounded-full mr-2"></span>
              Business Cards ({data.length})
            </h2>
          </div>
          <div className="p-6">
            <BusinessCardList cards={data} viewOnly />
          </div>
        </div>

        <div className="mt-8 text-center text-sm text-gray-500">
          <p>Profile data loaded successfully • {new Date().toLocaleString()}</p>
        </div>
      </div>
    </div>
  );
}

// Add global styles for the component
const style = document.createElement('style');
style.textContent = `
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
  .animate-spin {
    animation: spin 1s linear infinite;
  }
  
  /* Business card list enhancements */
  .business-card {
    transition: all 0.3s ease;
    border: 1px solid #e5e7eb;
  }
  .business-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    border-color: #8b5cf6;
  }
  
  .card-header {
    background: linear-gradient(to right, #8b5cf6, #6d28d9);
    color: white;
  }
  
  .contact-badge {
    background: #ede9fe;
    color: #5b21b6;
  }
`;
document.head.appendChild(style);
