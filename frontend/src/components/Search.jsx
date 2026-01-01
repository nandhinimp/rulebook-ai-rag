import { useState } from 'react'
import axios from 'axios'
import './Search.css'

const API_BASE = 'http://127.0.0.1:8001'

function Search({ onSearch }) {
  const [query, setQuery] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const handleSearch = async (e) => {
    e.preventDefault()
    const trimmedQuery = query.trim()

    if (!trimmedQuery) return

    try {
      setIsLoading(true)
      const response = await axios.post(`${API_BASE}/ask`, null, {
        params: { query: trimmedQuery }
      })

      onSearch(response.data)
      setQuery('')
    } catch (error) {
      console.error('Search error:', error)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div>
      <form className="search-box" onSubmit={handleSearch}>
        <input
          type="text"
          placeholder="Ask a question about your PDFs..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          disabled={isLoading}
        />
        <button
          type="submit"
          className="btn btn-primary"
          disabled={isLoading}
        >
          {isLoading ? 'Searching...' : 'Ask'}
        </button>
      </form>
    </div>
  )
}

export default Search
