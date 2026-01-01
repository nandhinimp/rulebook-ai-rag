import { useState, useRef } from 'react'
import axios from 'axios'
import './Upload.css'

const API_BASE = 'http://127.0.0.1:8001'

function Upload({ onUploadSuccess }) {
  const [status, setStatus] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const uploadAreaRef = useRef(null)
  const fileInputRef = useRef(null)

  const handleDragOver = (e) => {
    e.preventDefault()
    uploadAreaRef.current?.classList.add('active')
  }

  const handleDragLeave = () => {
    uploadAreaRef.current?.classList.remove('active')
  }

  const handleDrop = (e) => {
    e.preventDefault()
    uploadAreaRef.current?.classList.remove('active')
    processFiles(e.dataTransfer.files)
  }

  const handleFileSelect = (e) => {
    processFiles(e.target.files)
  }

  const processFiles = async (files) => {
    for (let file of files) {
      if (file.type === 'application/pdf') {
        await uploadFile(file)
      } else {
        setStatus({ type: 'error', message: 'Only PDF files are allowed' })
      }
    }
  }

  const uploadFile = async (file) => {
    const formData = new FormData()
    formData.append('file', file)

    try {
      setIsLoading(true)
      setStatus({ type: 'loading', message: `Uploading ${file.name}...` })

      const response = await axios.post(`${API_BASE}/pdf/upload`, formData)

      if (response.status === 200) {
        const { filename, chunks_added } = response.data
        onUploadSuccess(filename)
        setStatus({
          type: 'success',
          message: `✓ ${filename} uploaded successfully (${chunks_added} chunks indexed)`
        })
      }
    } catch (error) {
      setStatus({
        type: 'error',
        message: `Upload error: ${error.message}`
      })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div>
      <div
        ref={uploadAreaRef}
        className="upload-area"
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
      >
        <div className="icon">📄</div>
        <p><strong>Click to upload</strong> or drag and drop</p>
        <p style={{ fontSize: '0.9em', color: '#999' }}>PDF files only</p>
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf"
          onChange={handleFileSelect}
          className="file-input"
        />
      </div>

      {status && (
        <div className={`status ${status.type}`}>
          {status.type === 'loading' && <div className="spinner"></div>}
          <span>{status.message}</span>
        </div>
      )}
    </div>
  )
}

export default Upload
