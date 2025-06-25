import { useState } from 'react'
import Chatbot from './components/Chatbot'
import HomePage from './components/HomePage'

function App() {
  const [count, setCount] = useState(0)

  return (
    <HomePage />
  )
}

export default App
