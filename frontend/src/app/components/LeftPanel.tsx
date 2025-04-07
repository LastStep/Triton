"use client";

import { useState } from 'react';

async function fetchBookById(bookId: string, dataSource: string, setBookContent: (content: string) => void) {
  try {
    const isLoading = true;
    const response = await fetch(`http://localhost:8000/book/?bookID=${encodeURIComponent(bookId)}&source=${encodeURIComponent(dataSource)}`);
    if (response.status === 404) {
      console.log("Book not found");
      return null;
    }
    const text = await response.text();
    setBookContent(text);
    return text;
  } catch (error) {
    console.error("Error fetching book:", error);
    return null;
  }
}

export default function LeftPanel({ setBookContent }: { setBookContent: (content: string) => void }) {
  const [bookId, setBookId] = useState('');
  const [dataSource, setDataSource] = useState('default');
  const [isLoading, setIsLoading] = useState(false);

  const handleFetch = async () => {
    setIsLoading(true);
    await fetchBookById(bookId, dataSource, setBookContent);
    setIsLoading(false);
  };

  return (
    <div style={{ padding: '12px', display: 'flex', flexDirection: 'column', height: '100%', gap: '16px' }}>
      <h2 style={{ margin: '0 0 8px 0', borderBottom: '2px solid #ccc', paddingBottom: '6px', fontSize: '1.2rem' }}>Data Source</h2>
      
      {/* Data Source Selection */}
      <div>
        <select
          value={dataSource}
          onChange={(e) => setDataSource(e.target.value)}
          style={{
            width: '100%',
            padding: '6px',
            marginBottom: '8px',
            borderRadius: '4px',
            border: '1px solid #ccc'
          }}
        >
          <option value="default">Default Library</option>
          <option value="gutenberg">Project Gutenberg</option>
          <option value="archive">Internet Archive</option>
          <option value="local">Local Repository</option>
        </select>
      </div>
      
      {/* Book ID Input */}
      <div style={{ display: 'flex', gap: '8px' }}>
        <input
          type="text"
          placeholder="Enter Book ID"
          value={bookId}
          onChange={(e) => setBookId(e.target.value)}
          style={{ 
            flex: '1',
            padding: '6px',
            borderRadius: '4px',
            border: '1px solid #ccc'
          }}
        />
        <button 
          onClick={handleFetch} 
          disabled={isLoading || !bookId.trim()} 
          style={{ 
            padding: '6px 12px',
            backgroundColor: isLoading ? '#cccccc' : '#0070f3',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: isLoading || !bookId.trim() ? 'not-allowed' : 'pointer',
            whiteSpace: 'nowrap'
          }}
        >
          {isLoading ? 'Loading...' : 'Fetch'}
        </button>
      </div>
      
      {/* Quick Access Bookmarks */}
      <div style={{ marginTop: 'auto' }}>
        <h3 style={{ margin: '0 0 6px 0', fontSize: '0.9rem', color: '#555' }}>Quick Access</h3>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '4px' }}>
          {['1342', '2701', '84', '1661', '11'].map(id => (
            <button
              key={id}
              onClick={() => {
                setBookId(id);
                handleFetch();
              }}
              style={{ 
                padding: '4px 8px',
                fontSize: '0.8rem',
                backgroundColor: '#f0f0f0',
                border: '1px solid #ddd',
                borderRadius: '4px',
                cursor: 'pointer'
              }}
            >
              {id}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}