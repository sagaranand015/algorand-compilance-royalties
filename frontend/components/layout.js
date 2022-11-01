import Link from 'next/link'
import { useState, useEffect } from 'react';
import { useAuth } from '../utils/authProvider.js';
import algosdk from "algosdk";

const shortenAddress = (address) => {
    if (address)
        return address.substring(0, 6) + "..." + address.substring(address.length - 4, address.length)
}

export default function Layout({ children }) {

    const client = new algosdk.Algodv2("", "https://testnet-api.algonode.cloud", "");

    const { currentAccount, setCurrentAccount, disconnectAccount } = useAuth()
    const [accountBalance, setAccountBalance] = useState(0)

    useEffect(() => {
      const fetchAccountBalance = async (account) => {
        const accountInfo = await client
        .accountInformation(account)
        .setIntDecoding(algosdk.IntDecoding.BIGINT)
        .do();

        setAccountBalance(Number(accountInfo.amount))
      }

      if (currentAccount) {
        fetchAccountBalance(currentAccount)
      }
  }, [currentAccount])

    return (
        <div className="h-screen p-6">
            <div>
                <header className="flex justify-between mb-6">
                    <div className="flex items-center">
                        <h3 className="text-xl font-extrabold"><Link href="/">Compliance Royalties</Link></h3>
                        {currentAccount && <p className="ml-8 text-gray-600"><Link href="/dashboard">Dashboard</Link></p>}
                    </div>
                    {currentAccount ? (
                        <div className="flex items-center">
                          <p className="mr-6 border px-4 py-2">{accountBalance} ALGO</p>
                          <h4 onClick={disconnectAccount} className="cursor-pointer">{shortenAddress(currentAccount)}</h4>
                        </div>
                        
                    ) : (
                        <button className="px-4 py-2 text-lg border border-orange-600 text-orange-600" onClick={setCurrentAccount}>Connect Wallet</button>
                    )}
                </header>
                <main>
                    {children}
                </main>
            </div>

            <footer>
                <div className="mt-8 mb-6 border border-grey-600"></div>
                <div className="flex justify-between">
                    <p>Life is in this moment. There is no other meaning of life.</p>
                </div>
            </footer>
        </div>
    )
}