import React from 'react';
import logo from './logo.svg';
import './App.css';
import { useState, useEffect } from "react";
// import { Network, APIProvider, getAlgodClient } from "beaker-ts/lib/clients/index.js";
import WalletConnect from '@walletconnect/client';
import { formatJsonRpcRequest } from "@json-rpc-tools/utils";

import QRCodeModal from "algorand-walletconnect-qrcode-modal";
import algosdk from "algosdk";
import { type } from 'os';
// import { APIProvider, getAlgodClient, Network } from 'beaker-ts/lib/clients';


function App() {

  let account: string = "";

  // const [apiProvider, setApiProvider] = useState(APIProvider.AlgoNode);
  // const [network, setNetwork] = useState(Network.TestNet);

  // // // Init our algod client
  // const algodClient = getAlgodClient(apiProvider, network);

  const connector = new WalletConnect({
    bridge: "https://bridge.walletconnect.org", // Required
    qrcodeModal: QRCodeModal,
  });

  const client = new algosdk.Algodv2("", "https://testnet-api.algonode.cloud", "");

  async function subscribeToEvents() {
    // const { connector } = this.state;
    if (!connector) {
      console.log("======== no connector. Please try again!");
      return;
    }
    connector.on("session_update", async (error, payload) => {
      console.log(`connector.on("session_update")`);
      if (error) {
        throw error;
      }
      const { accounts } = payload.params[0];
      account = accounts;
    });

    connector.on("connect", (error, payload) => {
      console.log(`connector.on("connect")`);
      if (error) {
        throw error;
      }
      console.log("========= onConnect", payload);
      const address = payload.params[0].accounts[0];
      account = address;
      console.log("========= onConnect DONE", payload, address);
    });

    connector.on("disconnect", (error, payload) => {
      console.log(`connector.on("disconnect")`, payload);

      if (error) {
        throw error;
      }
      account = "";
    });

    if (connector.connected) {
      console.log("======= I'm already connected!");
      const { accounts } = connector;
      const address = accounts[0];
      account = address;
    }
  };

  async function GetAccountBalance() {

    if (connector.connected) {
      const { accounts } = connector;
      const address = accounts[0];
      console.log("======= connected here too!", accounts, address);
      account = address;
    }

    console.log("========= account balance of address: ", account);
    const accountInfo = await client
      .accountInformation(account)
      .setIntDecoding(algosdk.IntDecoding.BIGINT)
      .do();
    console.log("======== account info is: ", accountInfo);
    console.log("======== account balance is: ", accountInfo.amount);
  }

  // async function CreateComplianceNft() {
  //   console.log("==== creating the compliance NFT...");

  //   // signing and sending "txn" allows "addr" to create an asset
  //   let txn = algosdk.makeAssetCreateTxnWithSuggestedParams(
  //     addr,
  //     note,
  //     totalIssuance,
  //     decimals,
  //     defaultFrozen,
  //     manager,
  //     reserve,
  //     freeze,
  //     clawback,
  //     unitName,
  //     assetName,
  //     assetURL,
  //     assetMetadataHash,
  //     params);

  //   let rawSignedTxn = txn.signTxn(recoveredAccount1.sk)
  //   let tx = (await algodclient.sendRawTransaction(rawSignedTxn).do());

  //   let assetID = null;
  //   // wait for transaction to be confirmed
  //   const ptx = await algosdk.waitForConfirmation(algodclient, tx.txId, 4);
  //   // Get the new asset's information from the creator account
  //   assetID = ptx["asset-index"];
  //   //Get the completed Transaction
  //   console.log("Transaction " + tx.txId + " confirmed in round " + ptx["confirmed-round"]);
  // }

  async function OptIntoComplianceNft() {
    console.log("==== opting in and receiving the compliance NFT...");

    let params = await client.getTransactionParams().do();
    let biz_sender = account;
    const optInTxn = algosdk.makeAssetTransferTxnWithSuggestedParamsFromObject({
      amount: 0,
      from: account,
      to: account,
      assetIndex: 120023374,
      suggestedParams: params,
    });

    const encodedTxn = Buffer.from(algosdk.encodeUnsignedTransaction(optInTxn)).toString("base64");
    const txnObj = [{
      txn: encodedTxn,
      message: 'Sign me with Wallet Connect to opt into the compliance NFT',
    }]
    const request = formatJsonRpcRequest("algo_signTxn", [txnObj]);
    const result: Array<string> = await connector.sendCustomRequest(request);
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

  async function OptInRewardToken() {
    console.log("==== opting into 1 Reward Token...");

    let params = await client.getTransactionParams().do();
    let biz_sender = account;
    const optInTxn = algosdk.makeAssetTransferTxnWithSuggestedParamsFromObject({
      amount: 0,
      from: account,
      to: account,
      assetIndex: 120027897,
      suggestedParams: params,
    });

    const encodedTxn = Buffer.from(algosdk.encodeUnsignedTransaction(optInTxn)).toString("base64");
    const txnObj = [{
      txn: encodedTxn,
      message: 'Sign me with Wallet Connect to opt into the compliance NFT',
    }]
    const request = formatJsonRpcRequest("algo_signTxn", [txnObj]);
    const result: Array<string> = await connector.sendCustomRequest(request);
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

  // async function GetAssetTransfer() {
  //   let params = await client.getTransactionParams().do();
  //   let xtxn = algosdk.makeAssetTransferTxnWithSuggestedParams(
  //     "FDWRJOSEPJI3GINGCGRLJK3IC6RKWU22MPVWUAZTARDEMHU3HBN5QPTC6I",
  //     account,
  //     undefined,
  //     undefined,
  //     1,
  //     undefined,
  //     120012207,
  //     params);

  //   let txgroup = algosdk.assignGroupID([xtxn]);
  //   const encodedXTxn = Buffer.from(algosdk.encodeUnsignedTransaction(xtxn)).toString("base64");
  //   const XtxnObj = [{
  //     txn: encodedXTxn,
  //     message: 'Get the Compliance NFT now!',
  //   }]

  //   const Xrequest = formatJsonRpcRequest("algo_signTxn", [XtxnObj]);
  //   const Xresult: Array<string | null> = await connector.sendCustomRequest(Xrequest);
  //   console.log("========== actual transfer result is: ", Xresult);
  // }

  async function DisconnectWallet() {
    await connector.killSession();
  };

  async function ConnectWallet() {
    if (!connector.connected) {
      await connector.createSession();
    }
    // connector.connect();
    await subscribeToEvents();
  };

  return (
    <div className="App">
      <header className="App-header">
        <button onClick={() => ConnectWallet()}>Connect Wallet</button>
        <button onClick={() => DisconnectWallet()}>DisConnect Wallet</button>
        <button onClick={() => GetAccountBalance()}>Get Account Balance</button>
        <button onClick={() => OptIntoComplianceNft()}>Opt Into Compliance NFT</button>
        <button onClick={() => OptInRewardToken()}>Opt Into Reward Token</button>
      </header>
    </div>
  );
}

export default App;
