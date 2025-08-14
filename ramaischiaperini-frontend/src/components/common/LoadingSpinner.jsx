function LoadingSpinner({ message = 'Carregando...' }) {
  return (
    <div className="loading">
      <div className="spinner"></div>
      {message}
    </div>
  )
}

export default LoadingSpinner