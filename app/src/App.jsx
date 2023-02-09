import './App.css';

import MediaResource from './MediaResource';

function App() {
  return (
    <div className="App">
      <h1 className="text-3xl font-bold ">
      </h1>
      <div className='flex flex-col'>
        <MediaResource />
        <MediaResource />
      </div>
    </div>
  );
}

export default App;
