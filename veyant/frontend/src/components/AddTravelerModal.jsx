import { useState } from 'react'
import { createTraveler } from '../api/client'

export default function AddTravelerModal({ onClose, onCreated }) {
  const [form, setForm] = useState({ name: '', email: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const set = (k) => (e) => setForm((f) => ({ ...f, [k]: e.target.value }))

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      const traveler = await createTraveler(form)
      onCreated(traveler)
      onClose()
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="modal-overlay" onClick={(e) => e.target === e.currentTarget && onClose()}>
      <div className="modal">
        <div className="modal__header">
          <h2 className="modal__title">Add Traveler</h2>
          <button className="modal__close" onClick={onClose} aria-label="Close">&times;</button>
        </div>

        {error && <div className="error-banner">{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="name">Full name</label>
            <input
              id="name"
              className="form-control"
              placeholder="e.g. Alex Rivera"
              value={form.name}
              onChange={set('name')}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="email">Email address</label>
            <input
              id="email"
              type="email"
              className="form-control"
              placeholder="e.g. alex@example.com"
              value={form.email}
              onChange={set('email')}
              required
            />
          </div>

          <div className="form-actions">
            <button type="button" className="btn btn-ghost" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? 'Adding…' : 'Add Traveler'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
