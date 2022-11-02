import { Html, Head, Main, NextScript } from 'next/document'

export default function Document() {
    return (
        <Html>
            <Head>
                <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins"></link>
                <script src='https://kit.fontawesome.com/a076d05399.js' crossOrigin='anonymous'></script>
            </Head>
            <body>
                <Main />
                <NextScript />
            </body>
        </Html>
    )
}