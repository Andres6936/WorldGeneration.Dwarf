import React from 'react'
import ParentSize from '@visx/responsive/lib/components/ParentSize';
import ReactDOM from 'react-dom/client'
import App from './app.tsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
    <React.StrictMode>
        <ParentSize>
            {({width, height}) => <App width={width} height={height}/>}
        </ParentSize>
    </React.StrictMode>,
)