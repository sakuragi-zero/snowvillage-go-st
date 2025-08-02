import React from 'react';
import { createRoot } from 'react-dom/client';
import MyComponent from './src/MyComponent';

const App: React.FC = () => {
  return (
    <div>
      <MyComponent />
    </div>
  );
};

export default App;

if (typeof window !== 'undefined') {
  const container = document.getElementById('root');
  if (container) {
    const root = createRoot(container);
    root.render(<App />);
  }
}