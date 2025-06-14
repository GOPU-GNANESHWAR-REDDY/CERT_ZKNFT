import React, { useState, useEffect } from 'react'
import { useWallet } from '@txnlab/use-wallet-react'

const UNIVERSITY_ID = "A1KQ1"

const UniversityDashboard = () => {
  const { activeAddress } = useWallet()
  const [certificates, setCertificates] = useState([])

  const [formData, setFormData] = useState({
    student_name: '',
    student_pub: '',
    course: '',
    grade: '',
  })

  const [shareData, setShareData] = useState({
    student_id: '',
    nft_asset_id: '',
  })

  const fetchCertificates = async () => {
    try {
      const res = await fetch(`http://localhost:8000/university/debug-view/${UNIVERSITY_ID}`)
      const data = await res.json()
      setCertificates(data.certificates || [])
    } catch (err) {
      console.error("Error fetching certificates:", err)
    }
  }
  console.log({
  university_id: UNIVERSITY_ID,
  university_pub: activeAddress,
  ...formData,
})


  const handleMint = async () => {
    try {
      const res = await fetch('http://localhost:8000/university/mint-certificate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          university_id: UNIVERSITY_ID,
          university_pub: activeAddress,
          ...formData,
        }),
      })
      const result = await res.json()
      console.log("Mint Result:", result)
      fetchCertificates()
    } catch (err) {
      console.error("Error minting certificate:", err)
    }
  }

  const handleShare = async () => {
    try {
      const res = await fetch('http://localhost:8000/university/share-certificate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          university_id: UNIVERSITY_ID,
          ...shareData,
        }),
      })
      const result = await res.json()
      console.log("Share Result:", result)
      fetchCertificates()
    } catch (err) {
      console.error("Error sharing certificate:", err)
    }
  }

  useEffect(() => {
    fetchCertificates()
  }, [])

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-4">University Dashboard</h2>
      <p className="text-gray-600 mb-6">Connected: {activeAddress}</p>

      {/* Mint Certificate */}
      <div className="bg-white p-4 rounded-lg shadow mb-6">
        <h3 className="text-lg font-semibold mb-2">Mint Certificate</h3>
        <input
          type="text"
          className="input input-bordered w-full mb-2"
          placeholder="Student Name"
          onChange={(e) => setFormData({ ...formData, student_name: e.target.value })}
        />
        <input
          type="text"
          className="input input-bordered w-full mb-2"
          placeholder="Student Public Address"
          onChange={(e) => setFormData({ ...formData, student_pub: e.target.value })}
        />
        <input
          type="text"
          className="input input-bordered w-full mb-2"
          placeholder="Course"
          onChange={(e) => setFormData({ ...formData, course: e.target.value })}
        />
        <input
          type="text"
          className="input input-bordered w-full mb-2"
          placeholder="Grade"
          onChange={(e) => setFormData({ ...formData, grade: e.target.value })}
        />
        <button className="btn btn-primary w-full" onClick={handleMint}>Mint NFT Certificate</button>
      </div>

      {/* Share Certificate */}
      <div className="bg-white p-4 rounded-lg shadow mb-6">
        <h3 className="text-lg font-semibold mb-2">Share Certificate</h3>
        <input
          type="text"
          className="input input-bordered w-full mb-2"
          placeholder="Student ID"
          onChange={(e) => setShareData({ ...shareData, student_id: e.target.value })}
        />
        <input
          type="text"
          className="input input-bordered w-full mb-2"
          placeholder="NFT Asset ID"
          onChange={(e) => setShareData({ ...shareData, nft_asset_id: e.target.value })}
        />
        <button className="btn btn-accent w-full" onClick={handleShare}>Share Certificate</button>
      </div>

      {/* Display Certificates */}
      <div className="bg-white p-4 rounded-lg shadow">
        <h3 className="text-lg font-semibold mb-4">Minted Certificates</h3>
        {certificates.length === 0 ? (
          <p className="text-gray-500">No certificates yet.</p>
        ) : (
          <ul className="space-y-2">
            {certificates.map((cert, idx) => (
              <li key={idx} className="p-2 border rounded">
                <p><strong>Student:</strong> {cert.student}</p>
                <p><strong>Course:</strong> {cert.course}</p>
                <p><strong>NFT:</strong> {cert.nft_asset}</p>
                <p><strong>Student ID:</strong> {cert.student_id || 'N/A'}</p>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  )
}

export default UniversityDashboard
