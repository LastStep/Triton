import { FC } from 'react';

interface PoemData {
  section_title: string;
  poem_title: string;
}

interface PoemsTableProps {
  data: PoemData[];
}

const PoemsTable: FC<PoemsTableProps> = ({ data }) => {
  return data.length > 0 ? (
    <div style={{ marginBottom: '16px', overflowY: 'auto' }}>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            <th style={{ padding: '8px', textAlign: 'left', borderBottom: '1px solid #ddd' }}>Section Title</th>
            <th style={{ padding: '8px', textAlign: 'left', borderBottom: '1px solid #ddd' }}>Poem Title</th>
          </tr>
        </thead>
        <tbody>
          {data.map((item, index) => (
            <tr key={index}>
              <td style={{ padding: '8px', borderBottom: '1px solid #ddd' }}>{item.section_title}</td>
              <td style={{ padding: '8px', borderBottom: '1px solid #ddd' }}>{item.poem_title}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  ) : (
    <div style={{ marginBottom: '16px' }}>No data available.</div>
  );
};

export default PoemsTable;
