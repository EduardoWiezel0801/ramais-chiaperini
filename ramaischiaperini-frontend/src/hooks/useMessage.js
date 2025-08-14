import { useState } from 'react'

export function useMessage() {
  const [message, setMessage] = useState({ type: '', text: '' })

  const showMessage = (type, text) => {
    setMessage({ type, text })
    setTimeout(() => setMessage({ type: '', text: '' }), 5000)
  }

  const clearMessage = () => {
    setMessage({ type: '', text: '' })
  }

  return {
    message,
    showMessage,
    clearMessage
  }
}