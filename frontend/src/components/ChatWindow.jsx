import React, {useState} from 'react';
import {useDebouncedCallback} from "use-debounce";
import axios from 'axios';

function Chat() {

    const [userInput, setUserInput] = useState("");
    const [chat, setChat] = useState([])
    const [isLoading, setLoading] = useState(false)

    // Debounced function to fetch data
    const fetchData = useDebouncedCallback(async (data) => {
        try {
            setLoading(true)
            // Fetch data from the server
            const response = await axios.post('http://localhost:5001/query', {user_message: data});
            // Update chat with server response
            setChat([{
                text: response.data.ai_response,
                isUser: false
            }, ...chat]);

        } catch (error) {
            console.error('Error:', error);
        } finally {
            setLoading(false)
        }
    }, 500)

    // Handle form submission
    const handleSubmit = async (e) => {
        e.preventDefault()
        const text = userInput.trim()
        if (!text) return
        let timer;
        setChat([{
            text: text,
            isUser: true
        }, ...chat
        ]);

        setUserInput("")
        await fetchData(text)

    };

    return (
        <div className={"sidebar"}>
            <div className={"chat-window"}>
                {/* Display loading indicator if data is being fetched */}
                {isLoading && <p className=" chat-text bot-text">Wait please...</p>}
                {chat.length > 0 ? chat.map((ch, index) => {
                        return <p key={index}
                                  className={`chat-text ${ch.isUser ? "user-text" : "bot-text"}`}>{ch.text}</p>
                    }) :
                    <div className={"info-chat"}>
                        <div className={"avatar-image"}></div>
                        <p className={"info-text"}>Hi, I am Test Bot: Your Personal AI Assistant choose
                            your communication style, send me your @username</p>
                    </div>
                }
                //
            </div>
            <form onSubmit={handleSubmit}>
                <input
                    type={"text"}
                    id={"input-text"}
                    className={"input"}
                    placeholder={"Type a reply"}
                    value={userInput}
                    onChange={(e) => setUserInput(e.target.value)}
                />
            </form>
        </div>
    );
}

export default Chat;