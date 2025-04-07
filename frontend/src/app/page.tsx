"use client";

import { useState } from 'react';
import LeftPanel from './components/LeftPanel';
// import MiddlePanel from './components/MiddlePanel';
import MiddlePanel from './components/MiddlePanelTabs';
import RightPanel from './components/RightPanel';

interface PoemData {
  section_title: string;
  poem_title: string;
}
export default function Page() {
  const [bookContent, setBookContent] = useState<string>('');
  const [selectedText, setSelectedText] = useState<string>('');
  const [poemData, setModelResponse] = useState<string>('');

  return (
    <div style={{ display: 'flex', height: '100vh' }}>
      <div style={{ flex: 1, borderRight: '1px solid #ccc' }}>
        <LeftPanel setBookContent={setBookContent} />
      </div>
      <div style={{ flex: 2, overflow: 'hidden', position: 'relative' }}>
        <MiddlePanel
          bookContent={bookContent}
          poemData={poemData}
          setSelectedText={setSelectedText}
        />
      </div>
      <div style={{ flex: 1, borderLeft: '1px solid #ccc' }}>
        <RightPanel 
          selectedText={selectedText} 
          setModelResponse={setModelResponse}
        />
      </div>
    </div>
  );
}