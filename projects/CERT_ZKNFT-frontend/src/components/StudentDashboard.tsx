import React, { useEffect, useState } from 'react'
import { useWallet } from '@txnlab/use-wallet-react'

const StudentDashboard = () => {
  const { activeAddress } = useWallet()
  const [studentId, setStudentId] = useState('')
  const [certs, setCerts] = useState([])
  const [targetUniversity, setTargetUniversity] = useState('')
  const [targetAssetId, setTargetAssetId] = useState('')
  const [zkResponse, setZkResponse] = useState<any | null>(null)

  // 🔍 Step 1: Fetch student ID & certificates
  const fetchStudentProfile = async () => {
    try {
      const res = await fetch(`http://localhost:8000/student/view-certificates/${activeAddress}`)
      const data = await res.json()
      if (!data.error) {
        setStudentId(data.student_id)
        setCerts(data.certificates || [])
      } else {
        console.warn("Student not found, maybe not registered.")
      }
    } catch (err) {
      console.error("Failed to fetch student profile:", err)
    }
  }

  // 🧠 Step 2: Apply for ZK Verification
  const handleApply = async () => {
    const res = await fetch('http://localhost:8000/student/apply-verification', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        student_id: studentId,
        university_id: targetUniversity,
        nft_asset_id: targetAssetId,
      }),
    })
    const result = await res.json()
    setZkResponse(result)
  }

  useEffect(() => {
    if (activeAddress) fetchStudentProfile()
  }, [activeAddress])

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-4">Student Dashboard</h2>
      <p className="text-gray-600 mb-6">Wallet: {activeAddress}</p>

      {/* 🎓 Certificates */}
      <div className="mb-6">
        <h3 className="text-xl font-semibold mb-2">Your Certificates</h3>
        {certs.length === 0 ? (
          <p className="text-gray-500">No certificates received yet.</p>
        ) : (
          <ul className="space-y-2">
            {certs.map((cert: any, idx: number) => (
              <li key={idx} className="p-2 border rounded shadow bg-white">
                <p><strong>Course:</strong> {cert.course}</p>
                <p><strong>Grade:</strong> {cert.grade || "N/A"}</p>
                <p><strong>NFT:</strong> {cert.nft_asset}</p>
                {cert.qr_token && (
                  <img src={`http://localhost:8000/${cert.qr_token.replace('./', '')}`} alt="QR Token" className="mt-2 w-32" />
                )}
              </li>
            ))}
          </ul>
        )}
      </div>

      {/* 🧾 Apply ZK Verification */}
      <div className="bg-white shadow rounded-lg p-4">
        <h3 className="text-lg font-semibold mb-2">Apply for Verification (ZK Proof)</h3>
        <input
          type="text"
          className="input input-bordered w-full mb-2"
          placeholder="University ID"
          onChange={(e) => setTargetUniversity(e.target.value)}
        />
        <input
          type="text"
          className="input input-bordered w-full mb-2"
          placeholder="NFT Asset ID"
          onChange={(e) => setTargetAssetId(e.target.value)}
        />
        <button className="btn btn-accent w-full" onClick={handleApply}>
          Apply with ZK Proof
        </button>

        {zkResponse && (
          <div className="mt-4 p-2 bg-green-100 rounded text-sm">
            ✅ <strong>Proof Generated:</strong>
            <pre className="whitespace-pre-wrap">{JSON.stringify(zkResponse.zk_proof, null, 2)}</pre>
          </div>
        )}
      </div>
    </div>
  )
}

export default StudentDashboard
