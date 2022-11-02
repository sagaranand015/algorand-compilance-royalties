import { useEffect, useState } from "react"
// import { controlsData } from "../controlsData";
import HttpClient from "react-http-client";
import algosdk from "algosdk";
import { useAuth } from '../utils/authProvider.js';
import { formatJsonRpcRequest } from "@json-rpc-tools/utils";
import { connector } from "../utils/authProvider.js";

export const authToken = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2Njc1MDg0MjcsImlhdCI6MTY2NzQyMjAyNywic3ViIjoiV1JPQ0ZPVVZaTUVURTc2TVFUU0tUUE83NUJVTVpFQzNGQ1dEUkhMR1lDWFY2MkNETllGTVJHT1RITSJ9.Rm2IprsKDJ8wGJ5Vh25LF524dfEq2inCQjdAKTPHf4E"

const client = new algosdk.Algodv2("", "https://testnet-api.algonode.cloud", "");

async function OptIntoComplianceNft(account, assetIndex) {
    console.log("==== opting in and receiving the compliance NFT...");

    let params = await client.getTransactionParams().do();
    let biz_sender = account;
    const optInTxn = algosdk.makeAssetTransferTxnWithSuggestedParamsFromObject({
        amount: 0,
        from: account,
        to: account,
        assetIndex: assetIndex,
        suggestedParams: params,
    });

    const encodedTxn = Buffer.from(algosdk.encodeUnsignedTransaction(optInTxn)).toString("base64");
    const txnObj = [{
        txn: encodedTxn,
        message: 'Sign me with Wallet Connect to opt into the compliance NFT',
    }]
    const request = formatJsonRpcRequest("algo_signTxn", [txnObj]);
    const result = await connector.sendCustomRequest(request);
    console.log("========== result is: ", result);
    const decodedResult = result.map(element => {
        return new Uint8Array(Buffer.from(element, "base64"));
    });
    console.log("========= decodedResult of optIn: ", decodedResult, typeof (decodedResult));

    let opttx = (await client.sendRawTransaction(decodedResult[0]).do());
    // Wait for confirmation
    let confirmedTxn = await algosdk.waitForConfirmation(client, opttx.txId, 4);
    //Get the completed Transaction
    console.log("Transaction " + opttx.txId + " confirmed in round " + confirmedTxn["confirmed-round"]);
}

const ComplianceTypes = () => {

    const [controlsData, setControlsData] = useState(null)
    const [selectedControl, setSelectedControl] = useState(0)
    const [emissionValue, setEmissionValue] = useState(0)
    const { currentAccount } = useAuth()

    useEffect(() => {
        const fetchControls = async () => {
            try {
                const controlsResponse = await HttpClient.get("http://localhost:8080/regulator/controls", {}, {
                    'Authorization': authToken
                });
                if (!controlsResponse.status) {
                    console.log("Unable to Fetch Controls");
                }
                else {
                    setControlsData(controlsResponse.controls)
                }
            } catch (e) {
                console.log("Fetch Controls FAILED", e);
            }
        }

        fetchControls()
    }, [])

    const handleEmissionValueChange = (e) => {
        setEmissionValue(e.target.value)
    }

    const handleNFTMint = async () => {
        try {
            const nftMintResponse = await HttpClient.post("http://localhost:8080/compliance/mint", {
                "emission_param": String(controlsData[selectedControl].emission_param)
                // "emission_param": "Methane"
            }, {
                'Authorization': authToken
            });
            if (!nftMintResponse.status) {
                console.log("Unable to Mint NFT");
            }
            else {
                console.log(nftMintResponse)
                OptIntoComplianceNft(currentAccount,nftMintResponse.nft_id)
            }
        } catch (e) {
            console.log("NFT Mint FAILED", e);
        }
    }

    return (
        <div>
            <div className="flex flex-wrap min-w-fit mt-8">
            {controlsData && controlsData.map((control, index) => (
                <div>
                    {index === selectedControl ? (
                        <div key={control.emission_param} className="rounded-lg p-4 bg-slate-300 focus:bg-slate-300 hover:bg-slate-300 active:bg-slate-300 mr-5 cursor-pointer" onClick={() => { setSelectedControl(index) }}>
                            <p className="text-2xl font-bold">{control.emission_param}</p>
                            <p className="mt-4 text-gray-600">{control.emission_desc}</p>
                            <p className="mt-4"><span className="text-lg font-bold">{control.emission_max}</span> <span className="text-gray-500">max emissions</span></p>
                        </div>
                    ) : (
                        <div key={control.emission_param} className="rounded-lg p-4 bg-slate-100 focus:bg-slate-300 hover:bg-slate-300 active:bg-slate-300 mr-5 cursor-pointer" onClick={() => { setSelectedControl(index) }}>
                            <p className="text-2xl font-bold">{control.emission_param}</p>
                            <p className="mt-4 text-gray-600">{control.emission_desc}</p>
                            <p className="mt-4"><span className="text-lg font-bold">{control.emission_max}</span> <span className="text-gray-500">max emissions</span></p>
                        </div>
                    )}
                </div>
            ))}
            </div>

            <div className="mt-8">
                {
                    controlsData && (
                        <div>
                            <p>Enter your {controlsData[selectedControl].emission_param} emissions</p>
                            <input className="block mt-4 bg-gray-100 px-4 py-2 w-[20%]" type="number" name="EmissionValue" placeholder="Number of Emissions" value={emissionValue} onChange={handleEmissionValueChange} />
                            {emissionValue > 0 && emissionValue <= Number(controlsData[selectedControl].emission_max) && (
                                <div className="mt-4">
                                    <p>You are eligible to mint an nft</p>
                                    <button className="block bg-orange-400 px-4 py-2 mt-2" onClick={handleNFTMint}>Mint Now</button>
                                </div>
                            )}
                            {emissionValue > Number(controlsData[selectedControl].emission_max) && (
                                <div className="mt-4">
                                    <p>Sorry you are not eligible for nft</p>
                                </div>
                            )}
                        </div>
                    )
                }

            </div>
        </div>
    )
}

export default ComplianceTypes