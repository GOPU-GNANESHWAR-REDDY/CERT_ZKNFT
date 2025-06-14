import React, { useState } from 'react'

const EmployerDashboard = () => {
  const [universityId, setUniversityId] = useState('')
  const [studentId, setStudentId] = useState('')
  const [assetId, setAssetId] = useState('')
  const [zkProof, setZkProof] = useState('')
  const [result, setResult] = useState<any | null>(null)

  const handleVerify = async () => {
    const res = await fetch('http://localhost:8000/employer/verify-student-cert', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        university_id: universityId,
        student_id: studentId,
        nft_asset_id: assetId,
        zk_proof: zkProof,
      }),
    })

    const data = await res.json()
    setResult(data)
  }

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-4">Employer Dashboard</h2>
      <p className="text-gray-600 mb-6">Enter details and ZK proof to verify a certificate.</p>

      <div className="bg-white p-4 rounded shadow space-y-4 max-w-xl mx-auto">
        <input
          className="input input-bordered w-full"
          placeholder="University ID"
          value={universityId}
          onChange={(e) => setUniversityId(e.target.value)}
        />
        <input
          className="input input-bordered w-full"
          placeholder="Student ID"
          value={studentId}
          onChange={(e) => setStudentId(e.target.value)}
        />
        <input
          className="input input-bordered w-full"
          placeholder="NFT Asset ID"
          value={assetId}
          onChange={(e) => setAssetId(e.target.value)}
        />
        <textarea
          className="textarea textarea-bordered w-full"
          placeholder="ZK Proof"
          rows={3}
          value={zkProof}
          onChange={(e) => setZkProof(e.target.value)}
        />

        <button className="btn btn-primary w-full" onClick={handleVerify}>
          Verify Certificate
        </button>
      </div>

      {result && (
        <div className={`mt-6 p-4 rounded ${result.valid ? 'bg-green-100' : 'bg-red-100'}`}>
          <h3 className="text-xl font-semibold mb-2">
            {result.valid ? '✅ Certificate is valid' : '❌ Invalid Proof'}
          </h3>
          {result.valid && (
            <pre className="text-sm bg-white p-2 rounded overflow-x-auto">
              {JSON.stringify(result.certificate, null, 2)}
            </pre>
          )}
        </div>
      )}
    </div>
  )
}

export default EmployerDashboard
