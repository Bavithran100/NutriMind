import { useNavigate } from 'react-router-dom'

export default function Dashboard() {
  const navigate = useNavigate()

  const handleLogout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    navigate('/login')
  }

  return (
    <div className="max-w-4xl mx-auto mt-10 p-6">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Mood & Food Wellness Dashboard</h1>
        <button
          onClick={handleLogout}
          className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
        >
          Logout
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded shadow hover:shadow-lg transition-shadow">
          <h3 className="text-xl font-semibold mb-4">Add Daily Log</h3>
          <p className="text-gray-600 mb-4">Track your mood, sleep, exercise, and food intake</p>
          <button
            onClick={() => navigate('/add-log')}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            Add Log
          </button>
        </div>

        <div className="bg-white p-6 rounded shadow hover:shadow-lg transition-shadow">
          <h3 className="text-xl font-semibold mb-4">View Reports</h3>
          <p className="text-gray-600 mb-4">See your weekly trends and insights</p>
          <button
            onClick={() => navigate('/report')}
            className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
          >
            View Report
          </button>
        </div>

        <div className="bg-white p-6 rounded shadow hover:shadow-lg transition-shadow">
          <h3 className="text-xl font-semibold mb-4">Food Suggestions</h3>
          <p className="text-gray-600 mb-4">Get personalized meal recommendations</p>
          <button
            onClick={() => navigate('/food-suggestions')}
            className="bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700"
          >
            Get Suggestions
          </button>
        </div>

        <div className="bg-white p-6 rounded shadow hover:shadow-lg transition-shadow">
          <h3 className="text-xl font-semibold mb-4">AI Assistant</h3>
          <p className="text-gray-600 mb-4">Chat with our AI for nutrition and mood advice</p>
          <button
            onClick={() => navigate('/assistant')}
            className="bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700"
          >
            Chat Now
          </button>
        </div>
      </div>
    </div>
  )
}
