
import React from 'react';

function Message({ text, isUser }) {
  return (
    <div className={isUser ? "user-message" : "bot-message"}>
      <p>{text}</p>
    </div>
  );
}

export default Message;
