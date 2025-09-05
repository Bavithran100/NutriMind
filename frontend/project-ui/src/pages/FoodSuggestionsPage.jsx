import { useState, useEffect } from 'react'
import axios from 'axios'

export default function FoodSuggestionsPage() {
  const [suggestions, setSuggestions] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchSuggestions()
  }, [])

  const fetchSuggestions = async () => {
    try {
      const token = localStorage.getItem('access_token')
      const response = await axios.get('http://localhost:8000/api/food-suggestions/', {
        headers: { Authorization: `Bearer ${token}` }
      })
      setSuggestions(response.data)
    } catch {
      // Fallback to static suggestions
      setSuggestions([
        { meal: 'Breakfast', time: '8 AM', items: 'Oats + Banana', calories: 300 },
        { meal: 'Lunch', time: '1 PM', items: 'Rice + Chicken + Salad', calories: 500 },
        { meal: 'Dinner', time: '7 PM', items: 'Soup + Spinach', calories: 350 }
      ])
    } finally {
      setLoading(false)
    }
  }

  if (loading) return <div className="text-center mt-20">Loading suggestions...</div>

  return (
    <div className="max-w-4xl mx-auto mt-10 p-6">
      <h2 className="text-3xl font-bold mb-8">Food Suggestions</h2>

      <div className="space-y-6">
        {suggestions.map((suggestion, index) => (
          <div key={index} className="bg-white p-6 rounded shadow">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-xl font-semibold">{suggestion.meal}</h3>
              <span className="text-gray-600">{suggestion.time}</span>
            </div>
            <p className="text-gray-700 mb-2">{suggestion.items}</p>
            <p className="text-sm text-gray-500">Approx. {suggestion.calories} calories</p>
          </div>
        ))}
      </div>

      <div className="mt-8 text-center">
        <button
          onClick={fetchSuggestions}
          className="bg-purple-600 text-white px-6 py-2 rounded hover:bg-purple-700"
        >
          Generate New Plan
        </button>
      </div>
    </div>
  )
}
