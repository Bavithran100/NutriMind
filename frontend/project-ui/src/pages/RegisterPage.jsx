import { useState } from 'react'
import axios from 'axios'
import { useNavigate, Link } from 'react-router-dom'

export default function RegisterPage() {
  const [username, setUsername] = useState('')
  const [firstName, setFirstName] = useState('')
  const [lastName, setLastName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [password2, setPassword2] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    if (password !== password2) {
      setError('Passwords do not match')
      setLoading(false)
      return
    }

    try {
      await axios.post('http://localhost:8000/api/register/', {
        username,
        first_name: firstName,
        last_name: lastName,
        email,
        password,
        password2
      })
      navigate('/login')
    } catch (error) {
      if (error.response && error.response.data) {
        // Handle specific error messages from backend
        const errorData = error.response.data
        if (errorData.username) {
          setError(`Username: ${errorData.username[0]}`)
        } else if (errorData.email) {
          setError(`Email: ${errorData.email[0]}`)
        } else if (errorData.password) {
          setError(`Password: ${errorData.password[0]}`)
        } else {
          setError('Registration failed. Please try again.')
        }
      } else {
        setError('Registration failed. Please check your connection.')
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-md mx-auto mt-20 p-6 bg-white rounded shadow">
      <h2 className="text-2xl font-bold mb-4">Register</h2>
      {error && <p className="text-red-500 mb-4">{error}</p>}
      <form onSubmit={handleSubmit}>
        <label className="block mb-2">Username</label>
        <input
          type="text"
          className="w-full p-2 border rounded mb-4"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <label className="block mb-2">First Name</label>
        <input
          type="text"
          className="w-full p-2 border rounded mb-4"
          value={firstName}
          onChange={(e) => setFirstName(e.target.value)}
          required
        />
        <label className="block mb-2">Last Name</label>
        <input
          type="text"
          className="w-full p-2 border rounded mb-4"
          value={lastName}
          onChange={(e) => setLastName(e.target.value)}
          required
        />
        <label className="block mb-2">Email</label>
        <input
          type="email"
          className="w-full p-2 border rounded mb-4"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <label className="block mb-2">Password</label>
        <input
          type="password"
          className="w-full p-2 border rounded mb-4"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <label className="block mb-2">Confirm Password</label>
        <input
          type="password"
          className="w-full p-2 border rounded mb-4"
          value={password2}
          onChange={(e) => setPassword2(e.target.value)}
          required
        />
        <button
          type="submit"
          className="w-full bg-green-600 text-white p-2 rounded hover:bg-green-700 disabled:opacity-50"
          disabled={loading}
        >
          {loading ? 'Registering...' : 'Register'}
        </button>
      </form>
      <p className="mt-4 text-center">
        Already have an account? <Link to="/login" className="text-blue-600 hover:underline">Login</Link>
      </p>
    </div>
  )
}
