import { Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import TravelerList from './components/TravelerList'
import TravelerDetail from './components/TravelerDetail'

export default function App() {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<TravelerList />} />
        <Route path="/travelers/:id" element={<TravelerDetail />} />
      </Routes>
    </>
  )
}
