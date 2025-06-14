import React from 'react'
import { useNavigate } from 'react-router-dom'
import { useWallet } from '@txnlab/use-wallet-react'
import ConnectWallet from './components/ConnectWallet'

const Home = () => {
  const { activeAddress } = useWallet()
  const navigate = useNavigate()

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-b from-blue-100 to-white text-center p-6">
      <h1 className="text-4xl font-bold text-teal-700 mb-4">Welcome to CERT-ZKNFT</h1>
      <p className="text-gray-600 mb-6">Decentralized ZK-NFT Certificate Platform</p>

      <ConnectWallet />

      {activeAddress && (
        <div className="mt-8 space-y-4">
          <h2 className="text-xl font-semibold text-gray-800 mb-2">Select Role</h2>
          <div className="flex flex-col space-y-2">
            <button className="btn btn-primary" onClick={() => navigate('/university')}>
              🎓 University Dashboard
            </button>
            <button className="btn btn-secondary" onClick={() => navigate('/student')}>
              🎒 Student Dashboard
            </button>
            <button className="btn btn-accent" onClick={() => navigate('/employer')}>
              🏢 Employer Dashboard
            </button>
          </div>
        </div>
      )}
    </div>
  )
}

export default Home
