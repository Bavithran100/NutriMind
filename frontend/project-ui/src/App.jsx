import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { useState } from 'react'
import axios from 'axios'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import Dashboard from './pages/Dashboard'
import AddLogPage from './pages/AddLogPage'
import ReportPage from './pages/ReportPage'
import FoodSuggestionsPage from './pages/FoodSuggestionsPage'
import ProfilePage from './pages/ProfilePage'
import AssistantPage from './pages/AssistantPage'

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)

  // Removed automatic login check - user must explicitly login each time

  const handleLogout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    delete axios.defaults.headers.common['Authorization']
    setIsAuthenticated(false)
  }

  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Routes>
          <Route path="/login" element={<LoginPage setIsAuthenticated={setIsAuthenticated} />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/" element={<LoginPage setIsAuthenticated={setIsAuthenticated} />} />
          <Route path="/dashboard" element={isAuthenticated ? <Dashboard onLogout={handleLogout} /> : <LoginPage setIsAuthenticated={setIsAuthenticated} />} />
          <Route path="/add-log" element={isAuthenticated ? <AddLogPage /> : <LoginPage setIsAuthenticated={setIsAuthenticated} />} />
          <Route path="/report" element={isAuthenticated ? <ReportPage /> : <LoginPage setIsAuthenticated={setIsAuthenticated} />} />
          <Route path="/food-suggestions" element={isAuthenticated ? <FoodSuggestionsPage /> : <LoginPage setIsAuthenticated={setIsAuthenticated} />} />
          <Route path="/assistant" element={isAuthenticated ? <AssistantPage /> : <LoginPage setIsAuthenticated={setIsAuthenticated} />} />
          <Route path="/profile" element={isAuthenticated ? <ProfilePage /> : <LoginPage setIsAuthenticated={setIsAuthenticated} />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App
