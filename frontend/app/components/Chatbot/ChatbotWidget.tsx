'use client';

import { useState, useRef, useEffect } from 'react';
import styles from './ChatbotWidget.module.css';
import { Bot, X, Send, MessageSquare } from 'lucide-react';

interface Message {
  id: string;
  type: 'bot' | 'user';
  text: string;
}

export default function ChatbotWidget() {
  const [isOpen, setIsOpen] = useState(true);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      type: 'bot',
      text: "Hello! I'm Stitch, your HDFC investment expert. How can I help you grow your wealth today?"
    }
  ]);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async (e?: React.FormEvent) => {
    e?.preventDefault();
    if (!input.trim() || isLoading) return;

    const userQuery = input.trim();
    setInput('');
    
    // Add user message
    const userMsg: Message = { id: Date.now().toString(), type: 'user', text: userQuery };
    setMessages(prev => [...prev, userMsg]);
    setIsLoading(true);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: userQuery })
      });

      if (!response.ok) {
        throw new Error('API Error');
      }

      const data = await response.json();
      
      const botMsg: Message = { 
        id: (Date.now() + 1).toString(), 
        type: 'bot', 
        text: data.response || "I couldn't process that request right now." 
      };
      setMessages(prev => [...prev, botMsg]);
      
    } catch (error) {
      console.error('Chat error:', error);
      const errorMsg: Message = { 
        id: (Date.now() + 1).toString(), 
        type: 'bot', 
        text: "Sorry, I am having trouble connecting to the server. Please try again later." 
      };
      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSuggestion = (text: string) => {
    setInput(text);
  };

  return (
    <div className={styles.widgetContainer}>
      <div className={`${styles.chatbotWindow} ${!isOpen ? styles.closed : ''}`}>
        <div className={styles.chatHeader}>
          <div className={styles.headerInfo}>
            <div className={styles.botIconWrapper}>
              <Bot size={20} />
            </div>
            <div>
              <div className={styles.botName}>Stitch AI</div>
              <div className={styles.botStatus}>
                <span className={styles.statusDot}></span>
                Investment Assistant Online
              </div>
            </div>
          </div>
          <button className={styles.closeBtn} onClick={() => setIsOpen(false)}>
            <X size={20} />
          </button>
        </div>

        <div className={styles.messagesArea}>
          {messages.map((msg) => (
            <div key={msg.id} className={`${styles.message} ${styles[msg.type]}`}>
              {msg.text}
            </div>
          ))}
          {isLoading && (
            <div className={`${styles.message} ${styles.bot}`}>
              Typing...
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {messages.length === 1 && (
          <div className={styles.suggestions}>
            <button className={styles.suggestionChip} onClick={() => handleSuggestion("Compare Funds")}>Compare Funds</button>
            <button className={styles.suggestionChip} onClick={() => handleSuggestion("Risk Assessment")}>Risk Assessment</button>
            <button className={styles.suggestionChip} onClick={() => handleSuggestion("SIP Calculator")}>SIP Calculator</button>
          </div>
        )}

        <div className={styles.inputArea}>
          <form className={styles.inputForm} onSubmit={handleSend}>
            <input 
              type="text" 
              className={styles.chatInput} 
              placeholder="Ask Stitch anything..." 
              value={input}
              onChange={(e) => setInput(e.target.value)}
              disabled={isLoading}
            />
            <button type="submit" className={styles.sendBtn} disabled={!input.trim() || isLoading}>
              <Send size={18} />
            </button>
          </form>
        </div>
      </div>

      {!isOpen && (
        <button className={styles.toggleBtn} onClick={() => setIsOpen(true)}>
          <MessageSquare size={28} />
        </button>
      )}
    </div>
  );
}
