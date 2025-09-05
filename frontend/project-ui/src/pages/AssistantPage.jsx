import { useState, useEffect, useRef } from 'react'
import axios from 'axios'

function AssistantPage() {
  const [messages, setMessages] = useState([])
  const [inputMessage, setInputMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const sendMessage = async (e) => {
    e.preventDefault()
    if (!inputMessage.trim() || isLoading) return

    const userMessage = inputMessage.trim()
    setInputMessage('')
    setIsLoading(true)

    // Add user message to chat
    const newUserMessage = {
      id: Date.now(),
      message: userMessage,
      response: '',
      timestamp: new Date().toISOString(),
      isUser: true
    }

    setMessages(prev => [...prev, newUserMessage])

    try {
      const token = localStorage.getItem('access_token')
      const response = await axios.post(
        'http://localhost:8000/api/chat/chat/',
        { message: userMessage },
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }
      )

      // Update message with AI response
      setMessages(prev => prev.map(msg =>
        msg.id === newUserMessage.id
          ? { ...msg, response: response.data.response }
          : msg
      ))

    } catch (error) {
      console.error('Error sending message:', error)
      // Update message with error response
      setMessages(prev => prev.map(msg =>
        msg.id === newUserMessage.id
          ? { ...msg, response: 'Sorry, I encountered an error. Please try again.' }
          : msg
      ))
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
          {/* Header */}
          <div className="bg-blue-600 text-white p-6">
            <h1 className="text-2xl font-bold">AI Nutrition Assistant</h1>
            <p className="text-blue-100 mt-2">
              Get personalized nutrition and mood advice from our AI assistant
            </p>
          </div>

          {/* Chat Messages */}
          <div className="h-96 overflow-y-auto p-6 space-y-4">
            {messages.length === 0 && (
              <div className="text-center text-gray-500 py-8">
                <div className="text-4xl mb-4">🤖</div>
                <p className="text-lg">Hello! I'm your nutrition and mood assistant.</p>
                <p className="text-sm mt-2">Ask me anything about nutrition, mood, or wellness!</p>
              </div>
            )}

            {messages.map((msg) => (
              <div key={msg.id} className="space-y-3">
                {/* User Message */}
                <div className="flex justify-end">
                  <div className="bg-blue-600 text-white rounded-lg px-4 py-2 max-w-xs">
                    <p>{msg.message}</p>
                  </div>
                </div>

                {/* AI Response */}
                {msg.response && (
                  <div className="flex justify-start">
                    <div className="bg-gray-100 text-gray-800 rounded-lg px-4 py-2 max-w-md">
                      <p>{msg.response}</p>
                    </div>
                  </div>
                )}

                {/* Loading indicator */}
                {isLoading && messages[messages.length - 1].id === msg.id && (
                  <div className="flex justify-start">
                    <div className="bg-gray-100 text-gray-800 rounded-lg px-4 py-2">
                      <div className="flex items-center space-x-2">
                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
                        <span>Thinking...</span>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Form */}
          <div className="border-t p-4">
            <form onSubmit={sendMessage} className="flex space-x-4">
              <input
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                placeholder="Ask about nutrition, mood, or wellness..."
                className="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                disabled={isLoading}
              />
              <button
                type="submit"
                disabled={isLoading || !inputMessage.trim()}
                className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isLoading ? 'Sending...' : 'Send'}
              </button>
            </form>
          </div>
        </div>

        {/* Sample Questions */}
        <div className="mt-6 bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold mb-4">Sample Questions:</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <button
              onClick={() => setInputMessage("What foods can help improve my mood?")}
              className="text-left p-3 border border-gray-200 rounded-lg hover:bg-gray-50"
            >
              What foods can help improve my mood?
            </button>
            <button
              onClick={() => setInputMessage("How much water should I drink daily?")}
              className="text-left p-3 border border-gray-200 rounded-lg hover:bg-gray-50"
            >
              How much water should I drink daily?
            </button>
            <button
              onClick={() => setInputMessage("What are good breakfast options for energy?")}
              className="text-left p-3 border border-gray-200 rounded-lg hover:bg-gray-50"
            >
              What are good breakfast options for energy?
            </button>
            <button
              onClick={() => setInputMessage("How can I maintain healthy sleep habits?")}
              className="text-left p-3 border border-gray-200 rounded-lg hover:bg-gray-50"
            >
              How can I maintain healthy sleep habits?
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default AssistantPage
