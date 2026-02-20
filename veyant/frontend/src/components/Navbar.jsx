import { Link } from 'react-router-dom'

export default function Navbar() {
  return (
    <nav className="navbar">
      <div className="container navbar__inner">
        <Link to="/" className="navbar__brand">
          Ve<span>y</span>ant
          <small className="navbar__sub"> &nbsp;· Travel Tracker</small>
        </Link>
      </div>
    </nav>
  )
}
