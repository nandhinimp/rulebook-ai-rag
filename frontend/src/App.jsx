import { useState } from 'react'
import Upload from './components/Upload'
import Search from './components/Search'
import Results from './components/Results'
import './App.css'

function App() {
  const [results, setResults] = useState(null)
  const [uploadedFiles, setUploadedFiles] = useState([])

  const handleUploadSuccess = (filename) => {
    setUploadedFiles([...uploadedFiles, filename])
  }

  const handleSearch = (searchResults) => {
    setResults(searchResults)
  }

  return (
    <div className="container">
      <div className="header">
        <h1>📚 RuleBook AI</h1>
        <p>Corporate Q&A System - Get instant answers from your PDFs</p>
      </div>

      <div className="main-grid">
        <div className="card">
          <h2>📤 Upload PDF</h2>
          <Upload onUploadSuccess={handleUploadSuccess} />
          {uploadedFiles.length > 0 && (
            <div className="file-list">
              {uploadedFiles.map((file, idx) => (
                <div key={idx} className="file-item uploaded">
                  <span>✓ {file}</span>
                  <span style={{ fontSize: '0.9em' }}>Ready</span>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="card">
          <h2>❓ Ask Question</h2>
          <Search onSearch={handleSearch} />
        </div>
      </div>

      {results && (
        <div className="card">
          <h2>📋 Results</h2>
          <Results data={results} />
        </div>
      )}
    </div>
  )
}

export default App
