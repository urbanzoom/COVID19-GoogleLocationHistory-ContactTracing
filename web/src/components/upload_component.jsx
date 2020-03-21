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
      </div>
    )
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
