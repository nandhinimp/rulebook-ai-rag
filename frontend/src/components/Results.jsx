import './Results.css'

function Results({ data }) {
  if (!data) return null

  return (
    <div className="results">
      <div className="result-item answer">
        <div className="result-query">Q: {data.query}</div>
        <div className="result-text">{data.answer || 'No answer found'}</div>
        {data.sources && data.sources.length > 0 && (
          <div className="result-sources">
            <strong>Sources:</strong>
            <div>
              {data.sources.map((source, idx) => (
                <span key={idx} className="source-tag">
                  📄 {source.document} (Page {source.page})
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default Results
