export default function ColorBoxes() {
    return (
      <div style={{ display: 'flex', alignItems: 'center' }}>
        <div style={{ display: 'inline-flex', alignItems: 'center', marginRight: '10px' }}>
          <div style={{ width: '10px', height: '10px', backgroundColor: '#00D100', marginRight: '5px' }}></div>
          <span>Positive</span>
        </div>
        <div style={{ display: 'inline-flex', alignItems: 'center' }}>
          <div style={{ width: '10px', height: '10px', backgroundColor: '#f44336', marginRight: '5px' }}></div>
          <span>Negative</span>
        </div>
      </div>
    );
  }
  