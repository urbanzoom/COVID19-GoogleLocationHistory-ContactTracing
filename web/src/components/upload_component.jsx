import React from 'react'
import { FilePond } from 'react-filepond'
import S3 from 'aws-sdk/clients/s3'

const s3 = new S3({
  accessKeyId: process.env.REACT_APP_AWS_ACCESS_KEY_ID,
  secretAccessKey: process.env.REACT_APP_AWS_SECRET_ACCESS_KEY,
  region: process.env.REACT_APP_S3_REGION
})

class UploadComponent extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      // intersection: ['Subang Jaya Medical Center', 'Sunway Medical Center'],
      intersection: [],
      files: []
    }
  }

  handleInit() {
    console.log('FilePond instance has initialised', this.pond)
  }

  render () {
    return (
      <div className='col-md-8 offset-md-2'>
        <FilePond
          ref={ref => (this.pond = ref)}
          files={this.state.files}
          maxFiles={3}
          instantUpload={true}
          server={{
            process: this.serverProcess
          }}
          oninit={() => this.handleInit()}
          onupdatefiles={fileItems => {
            // Set currently active file objects to this.state
            this.setState({
              files: fileItems.map(fileItem => fileItem.file)
            });
          }}
        />
        { this.renderMessage() }
      </div>
    )
  }

  renderMessage () {
    if (this.state.intersection.length === 0) {
      return (
        <p className='text-center'>
          We didn't find any matches with confirm cases in our database.
          <br /><br />
          Please avoid any crowded places and practice social distancing at all time.
        </p>
      )
    } else {
      const clusters = this.state.intersection.map(x => <p>  - {x}</p>)
      const match = this.state.intersection.length > 1 ? 'matches' : 'a match'

      return (
        <p className='text-center'>
          Unfortunately, we've found {match} in your travel history with the following clusters:
          <br /><br />
          {clusters}
        </p>
      )
    }
  }

  serverProcess = (fieldName, file, metadata, load, error, progress, abort) => {
    debugger;
    s3.upload({
      Bucket: process.env.REACT_APP_S3_BUCKET,
      Key: Date.now() + '_' + file.name,
      Body: file,
      ContentType: file.type,
      ACL: 'private'
    }, function(err, data) {
      if (err) {
        console.error(err);
        error('Something went wrong');
        return;
      }
      // pass file unique id back to filepond
      load(data.Key);
    });
  }
}

export default UploadComponent
