import React from 'react'
import { useContext } from 'react';
import { useState, useEffect } from 'react';
import WalletConnect from "@walletconnect/client";
import QRCodeModal from "algorand-walletconnect-qrcode-modal";

const AuthContext = React.createContext();

export const connector = new WalletConnect({
    bridge: "https://bridge.walletconnect.org", // Required
    qrcodeModal: QRCodeModal,
});

function AuthProvider(props) {
    // const connector = new WalletConnect({
    //     bridge: "https://bridge.walletconnect.org", // Required
    //     qrcodeModal: QRCodeModal,
    // });

    const [currentAccount, setCurrentAccount] = useState(null)

    const checkWalletIsConnected = async () => {

        if (connector.connected) {
            console.log("======= I'm already connected!");
            const { accounts } = connector;
            const address = accounts[0];
            setCurrentAccount(address);
        }
    }

    useEffect(() => {
        checkWalletIsConnected()
    }, [])

    const connectWalletHandler = async () => {
        if (!connector) {
            console.log("======== no connector. Please try again!")
            return
        }

        if (!connector.connected) {
            await connector.createSession();
        }
        connector.on("connect", (error, payload) => {
            if (error) {
                throw error;
            }
            const address = payload.params[0].accounts[0];
            setCurrentAccount(address);
        });
    }

    const disconnectWalletHandler = () => {
        connector.killSession()
        connector.on("disconnect", (error) => {

            if (error) {
                console.log("Disconnect Error: " + error)
                throw error;
            }
            setCurrentAccount(null)
        });
    }

    return (
        <AuthContext.Provider value={{ currentAccount, setCurrentAccount: connectWalletHandler, disconnectAccount: disconnectWalletHandler }}>
            {props.children}
        </AuthContext.Provider>
    );
}

function useAuth() {
    const authContext = useContext(AuthContext);
    return { ...authContext };
}

export { AuthProvider, useAuth };