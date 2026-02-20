import { useState } from 'react'
import { createTrip } from '../api/client'

const TRAVEL_TYPES = ['business', 'leisure', 'adventure', 'family', 'solo', 'couple']
const ACCOMMODATION_TYPES = ['hotel', 'airbnb', 'hostel', 'resort', 'camping', 'other']

const EMPTY = {
  country: '',
  city: '',
  region: '',
  start_date: '',
  end_date: '',
  travel_type: '',
  accommodation_type: '',
  notes: '',
}

export default function AddTripModal({ travelerId, onClose, onCreated }) {
  const [form, setForm] = useState(EMPTY)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const set = (k) => (e) => setForm((f) => ({ ...f, [k]: e.target.value }))

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')

    if (form.end_date && form.start_date && form.end_date < form.start_date) {
      setError('End date must be on or after start date.')
      return
    }

    setLoading(true)
    try {
      const trip = await createTrip({ ...form, traveler_id: travelerId })
      onCreated(trip)
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
          <h2 className="modal__title">Add Trip</h2>
          <button className="modal__close" onClick={onClose} aria-label="Close">&times;</button>
        </div>

        {error && <div className="error-banner">{error}</div>}

        <form onSubmit={handleSubmit}>
          {/* Destination */}
          <div className="form-group">
            <label htmlFor="country">Country *</label>
            <input
              id="country"
              className="form-control"
              placeholder="e.g. Japan"
              value={form.country}
              onChange={set('country')}
              required
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="city">City</label>
              <input
                id="city"
                className="form-control"
                placeholder="e.g. Tokyo"
                value={form.city}
                onChange={set('city')}
              />
            </div>
            <div className="form-group">
              <label htmlFor="region">Region</label>
              <input
                id="region"
                className="form-control"
                placeholder="e.g. Kanto"
                value={form.region}
                onChange={set('region')}
              />
            </div>
          </div>

          {/* Dates */}
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="start_date">Start date *</label>
              <input
                id="start_date"
                type="date"
                className="form-control"
                value={form.start_date}
                onChange={set('start_date')}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="end_date">End date *</label>
              <input
                id="end_date"
                type="date"
                className="form-control"
                value={form.end_date}
                min={form.start_date}
                onChange={set('end_date')}
                required
              />
            </div>
          </div>

          {/* Type selects */}
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="travel_type">Travel type *</label>
              <select
                id="travel_type"
                className="form-control"
                value={form.travel_type}
                onChange={set('travel_type')}
                required
              >
                <option value="">Select…</option>
                {TRAVEL_TYPES.map((t) => (
                  <option key={t} value={t}>{t.charAt(0).toUpperCase() + t.slice(1)}</option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label htmlFor="accommodation_type">Accommodation *</label>
              <select
                id="accommodation_type"
                className="form-control"
                value={form.accommodation_type}
                onChange={set('accommodation_type')}
                required
              >
                <option value="">Select…</option>
                {ACCOMMODATION_TYPES.map((a) => (
                  <option key={a} value={a}>{a.charAt(0).toUpperCase() + a.slice(1)}</option>
                ))}
              </select>
            </div>
          </div>

          {/* Notes */}
          <div className="form-group">
            <label htmlFor="notes">Notes</label>
            <textarea
              id="notes"
              className="form-control"
              placeholder="Any memorable highlights…"
              rows={3}
              value={form.notes}
              onChange={set('notes')}
              style={{ resize: 'vertical' }}
            />
          </div>

          <div className="form-actions">
            <button type="button" className="btn btn-ghost" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? 'Saving…' : 'Add Trip'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
