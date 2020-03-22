import React from 'react'
import UploadComponent from './components/upload_component'

function App() {
  return (
    <div className='container'>
      <h1 className='text-center mt-3'>Covid-19 contact tracing</h1>
      <div className='row'>
        <UploadComponent></UploadComponent>
      </div>
    </div>
  );
}

export default App;
