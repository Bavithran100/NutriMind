import { useState, useEffect } from 'react'
import axios from 'axios'
import { Line, Bar } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
)

export default function ReportPage() {
  const [report, setReport] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchReport()
  }, [])

  const fetchReport = async () => {
    try {
      const token = localStorage.getItem('access_token')
      const response = await axios.get('http://localhost:8000/api/logs/weekly_report/', {
        headers: { Authorization: `Bearer ${token}` }
      })
      setReport(response.data)
    } catch (error) {
      console.error('Error fetching report:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) return <div className="text-center mt-20">Loading...</div>

  const moodData = {
    labels: ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7'],
    datasets: [{
      label: 'Mood',
      data: report?.mood_trend || [null, null, null, null, null, null, null],
      borderColor: 'rgb(75, 192, 192)',
      tension: 0.1,
      spanGaps: true // Connect points even with null values
    }]
  }

  const sleepExerciseData = {
    labels: ['Sleep Hours', 'Exercise Minutes'],
    datasets: [{
      label: 'Average',
      data: [report?.average_sleep || 0, report?.average_exercise || 0],
      backgroundColor: ['rgba(255, 99, 132, 0.2)', 'rgba(54, 162, 235, 0.2)'],
      borderColor: ['rgba(255, 99, 132, 1)', 'rgba(54, 162, 235, 1)'],
      borderWidth: 1
    }]
  }

  return (
    <div className="max-w-6xl mx-auto mt-10 p-6">
      <h2 className="text-3xl font-bold mb-8">Weekly Report</h2>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <div className="bg-white p-6 rounded shadow">
          <h3 className="text-xl font-semibold mb-4">Mood Trend</h3>
          <Line data={moodData} />
        </div>

        <div className="bg-white p-6 rounded shadow">
          <h3 className="text-xl font-semibold mb-4">Sleep & Exercise</h3>
          <Bar data={sleepExerciseData} />
        </div>
      </div>

      <div className="bg-white p-6 rounded shadow">
        <h3 className="text-xl font-semibold mb-4">Insights</h3>
        <div className="space-y-2">
          <p>Average Mood: {report?.average_mood?.toFixed(1) || 'N/A'}</p>
          <p>Average Sleep: {report?.average_sleep?.toFixed(1) || 'N/A'} hours</p>
          <p>Average Exercise: {report?.average_exercise?.toFixed(1) || 'N/A'} minutes</p>
          <p>Logs this week: {report?.logs_count || 0}</p>
        </div>
      </div>
    </div>
  )
}
