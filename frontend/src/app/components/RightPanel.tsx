"use client";

import { useState } from 'react';

async function promptModel(selectedText: string, setModelResponse: (content: string) => void) {
  try {
    const response = await fetch(`http://localhost:8000/model/?text=${encodeURIComponent(selectedText)}`);
    if (response.status === 404) {
      console.log("Error with model request");
      return null;
    }
    const jsonData = await response.json();
    console.log(jsonData);
    setModelResponse(JSON.stringify(jsonData, null, 2)); 
    return jsonData;
  } catch (error) {
    console.error("Error fetching data:", error);
    return null;
  }
}

export default function RightPanel({ selectedText, setModelResponse }: { 
  selectedText: string,
  setModelResponse: (content: string) => void 
}) {
  const [isLoading, setIsLoading] = useState(false);
  const [selectedModel, setSelectedModel] = useState("default");

  const handleExtractTitles = async () => {
    setIsLoading(true);
    await promptModel(selectedText, setModelResponse);
    setIsLoading(false);
  };

  return (
    <div style={{ 
      padding: '16px', 
      display: 'flex', 
      flexDirection: 'column', 
      height: '100%',
      gap: '24px'
    }}>
      {/* Model Selection Section */}
      <section>
        <h2 style={{ marginBottom: '12px', borderBottom: '2px solid #ccc', paddingBottom: '8px' }}>
          Model Selection
        </h2>
        <div style={{ marginBottom: '16px' }}>
          <label htmlFor="model-select" style={{ display: 'block', marginBottom: '8px' }}>
            Choose AI Model:
          </label>
          <select 
            id="model-select"
            value={selectedModel}
            onChange={(e) => setSelectedModel(e.target.value)}
            style={{
              width: '100%',
              padding: '8px',
              borderRadius: '4px',
              border: '1px solid #ccc'
            }}
          >
            <option value="default">Default Poetry Extractor</option>
            <option value="advanced">Advanced Poetry Analysis</option>
            <option value="detailed">Detailed Poetry Extraction</option>
          </select>
        </div>
      </section>

      {/* Execution Section */}
      <section style={{ marginTop: 'auto' }}>
        <h2 style={{ marginBottom: '12px', borderBottom: '2px solid #ccc', paddingBottom: '8px' }}>
          Execute
        </h2>
        <div>
          <div 
            title="Results will be displayed in the 'Model Response' tab of the middle panel"
            style={{ 
              display: 'inline-block', 
              position: 'relative',
              width: '100%'
            }}
          >
            <button 
              onClick={handleExtractTitles}
              disabled={isLoading} 
              style={{ 
                width: '100%',
                padding: '12px 16px',
                backgroundColor: isLoading ? '#cccccc' : '#0070f3',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: isLoading ? 'not-allowed' : 'pointer',
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                fontWeight: 'bold'
              }}
            >
              {isLoading ? (
                <>
                  <span style={{ display: 'inline-block', marginRight: '8px' }}>Processing...</span>
                  <div style={{ 
                    width: '16px', 
                    height: '16px', 
                    border: '3px solid rgba(255,255,255,0.3)', 
                    borderRadius: '50%', 
                    borderTopColor: 'white', 
                    animation: 'spin 1s linear infinite'
                  }} />
                  <style jsx>{`
                    @keyframes spin {
                      to { transform: rotate(360deg); }
                    }
                  `}</style>
                </>
              ) : (
                'Extract Poem Titles'
              )}
            </button>
            <div style={{ 
              marginTop: '8px', 
              fontSize: '12px', 
              color: '#666', 
              textAlign: 'center' 
            }}>
              Hover for more info • Results appear in Model Response tab
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}