"use client";

import { useEffect, useState } from 'react';
import { Tab, Tabs, TabList, TabPanel } from 'react-tabs';
import 'react-tabs/style/react-tabs.css';

export default function MiddlePanel({ bookContent = "", setSelectedText }: { 
    bookContent?: string; 
    setSelectedText: (text: string) => void } 
) {
  const lines = bookContent.split('\n');
  const [startLine, setStartLine] = useState('');
  const [endLine, setEndLine] = useState('');
  const [lineRange, setLineRange] = useState<{ start: number; end: number } | null>(null);

  useEffect(() => {
    if (startLine && endLine) {
        const start = parseInt(startLine, 10);
        const end = parseInt(endLine, 10);
        if (start < end) {
            setLineRange({start, end});
        }
    }
  }, [startLine, endLine]);

  useEffect(() => {
    if (lineRange) {
      const { start, end } = lineRange;
      const selectedLines = lines.slice(start - 1, end);
      setSelectedText(selectedLines.join('\n'));
    } else {
      setSelectedText('');
    }
  }, [lineRange, lines, setSelectedText]);

  let displayedText = bookContent;

  if (lineRange) {
    const { start, end } = lineRange;
    displayedText = lines.slice(start - 1, end).join('\n');
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      <div style={{ flex: 1, overflowY: 'auto' }}>
        <Tabs>
          <TabList>
            <Tab>Full Book Text</Tab>
            <Tab>TOC Trimmer</Tab>
          </TabList>

          <TabPanel>
            <div style={{ height: 'calc(100vh - 120px)', overflowY: 'auto' }}>
              <pre style={{ padding: '16px', fontFamily: 'monospace', fontSize: '1em', lineHeight: '1.6'}}>
                {lines.map((line, index) => (
                  <div key={index}>
                    <span style={{ background: '#f4f4f4', marginRight: '16px', display: 'inline-block', minWidth: '40px', textAlign: 'right' }}>{index + 1}</span>
                    {line}
                  </div>
                ))}
              </pre>
            </div>
          </TabPanel>
          <TabPanel>
            <div style={{ height: 'calc(100vh - 120px)', display: 'flex', flexDirection: 'column'}}>
              <div style={{ margin: '4px 8px'}}>
                <input
                  type="number"
                  placeholder="Start Line"
                  value={startLine}
                  onChange={(e) => setStartLine(e.target.value)}
                  style={{ marginBottom: '8px' }}
                />
                <input
                  type="number"
                  placeholder="End Line"
                  value={endLine}
                  onChange={(e) => setEndLine(e.target.value)}
                  style={{ marginBottom: '8px' }}
                />
              </div>
              <pre style={{ padding: '16px', fontFamily: 'monospace', fontSize: '1em', lineHeight: '1.6', overflowX: 'auto', overflowY: "auto" }}>
                {lines.map((line, index) => (
                  <div key={index}>
                    <span style={{ background: '#f4f4f4', marginRight: '16px', display: 'inline-block', minWidth: '40px', textAlign: 'right' }}>{index + 1}</span>
                    {lineRange && lineRange.start - 1 <= index && index < lineRange.end ? line : ""}
                  </div>
                ))}
              </pre>
            </div>
          </TabPanel>
        </Tabs>
      </div>
    </div>
  );
}