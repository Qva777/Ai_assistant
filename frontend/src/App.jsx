import React from 'react';
import Chat from './components/ChatWindow.jsx';
import Navbar from './components/Navbar.jsx';
import MainContent from "./components/MainContent.jsx";

function App() {
    return (
        <>
            <Navbar/>
            <div className={"container"}>
                <MainContent/>
                <Chat/>
            </div>
        </>
    );
}

export default App;
