import { useState } from 'react'
import axios from 'axios'
import { useNavigate } from 'react-router-dom'

export default function AddLogPage() {
  const [mood, setMood] = useState(3)
  const [sleepHours, setSleepHours] = useState('')
  const [exerciseMinutes, setExerciseMinutes] = useState('')
  const [food, setFood] = useState('')
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const token = localStorage.getItem('access_token')
      await axios.post('http://localhost:8000/api/logs/', {
        mood,
        sleep_hours: parseFloat(sleepHours),
        exercise_minutes: parseInt(exerciseMinutes),
        food
      }, {
        headers: { Authorization: `Bearer ${token}` }
      })
      setSuccess('Log added successfully!')
      setTimeout(() => navigate('/'), 2000)
    } catch {
      setError('Failed to add log')
    }
  }

  return (
    <div className="max-w-md mx-auto mt-10 p-6 bg-white rounded shadow">
      <h2 className="text-2xl font-bold mb-6">Add Daily Log</h2>
      {error && <p className="text-red-500 mb-4">{error}</p>}
      {success && <p className="text-green-500 mb-4">{success}</p>}
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label className="block mb-2">Mood (1-5)</label>
          <input
            type="range"
            min="1"
            max="5"
            value={mood}
            onChange={(e) => setMood(e.target.value)}
            className="w-full"
          />
          <div className="text-center mt-2">Current: {mood}</div>
        </div>

        <div className="mb-4">
          <label className="block mb-2">Sleep Hours</label>
          <input
            type="number"
            step="0.5"
            className="w-full p-2 border rounded"
            value={sleepHours}
            onChange={(e) => setSleepHours(e.target.value)}
            required
          />
        </div>

        <div className="mb-4">
          <label className="block mb-2">Exercise Minutes</label>
          <input
            type="number"
            className="w-full p-2 border rounded"
            value={exerciseMinutes}
            onChange={(e) => setExerciseMinutes(e.target.value)}
            required
          />
        </div>

        <div className="mb-4">
          <label className="block mb-2">Food Eaten</label>
          <textarea
            className="w-full p-2 border rounded"
            rows="3"
            value={food}
            onChange={(e) => setFood(e.target.value)}
            placeholder="e.g., Rice, Chicken, Salad"
            required
          />
        </div>

        <button type="submit" className="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700">
          Save Log
        </button>
      </form>
    </div>
  )
}
