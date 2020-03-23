import React from 'react'
import { FilePond, registerPlugin } from 'react-filepond'
import FilePondPluginFileValidateSize from 'filepond-plugin-file-validate-size'
import FilePondPluginFileValidateType from 'filepond-plugin-file-validate-type'
import S3 from 'aws-sdk/clients/s3'

const s3 = new S3({
  accessKeyId: process.env.REACT_APP_AWS_ACCESS_KEY_ID,
  secretAccessKey: process.env.REACT_APP_AWS_SECRET_ACCESS_KEY,
  region: process.env.REACT_APP_S3_REGION
})

class UploadComponent extends React.Component {
  constructor(props) {
    super(props);

    registerPlugin(FilePondPluginFileValidateSize)
    registerPlugin(FilePondPluginFileValidateType)

    this.state = {
      intersection: null,
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
          maxFiles={1}
          maxFileSize={'5MB'}
          acceptedFileTypes={['application/json']}
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
    if (this.state.intersection === null) {
      return ''
    } else if (this.state.intersection.length === 0) {
      return (
        <p className='text-center result__container'>
          We didn't find any matches with confirm cases in our database.
          <br /><br />
          Please avoid any crowded places and practice social distancing at all time.
        </p>
      )
    } else if (this.state.intersection === 'error') {
      return (
        <p className='text-center result__container'>
          Something went wrong with your uploaded file.
          <br /><br />
          Please check on <a href='#how-does-this-work'>the link below</a> to find out how to get the correct Location History file.
        </p>
      )
    } else {
      const clusters = this.state.intersection.slice(0,3).map((x, i) => {
        return (
          <div className='row mb-2' key={i}>
            <div className='col-6'>
              <img src={`https://maps.googleapis.com/maps/api/staticmap?markers=color:red%7C${x.lat},${x.lng}&zoom=12&size=300x200&key=${process.env.REACT_APP_GMAP_API_KEY}`} />
            </div>
            <div className='col-6 flex--center'>
              { x.clusterName }
            </div>
          </div>
        )
      })
      const match = this.state.intersection.length > 1 ? 'matches' : 'a match'

      return (
        <div className='text-center result__container'>
          We've found {match} in your travel history with the following clusters:
          <br /><br />
          {clusters}
        </div>
      )
    }
  }

  serverProcess = (fieldName, file, metadata, load, error, progress, abort) => {
    const that = this
    const fileName = Date.now() + '_' + file.name
    console.log('s3bucket:');
    console.log(process.env.REACT_APP_S3_BUCKET);
    s3.upload({
      Bucket: process.env.REACT_APP_S3_BUCKET,
      Key: fileName,
      Body: file,
      ContentType: file.type,
      ACL: 'private'
    }, function(err, data) {
      if (err) {
        console.error(err);
        error('Something went wrong');
        return;
      }
      that.notifyServer(fileName)
      // pass file unique id back to filepond
      load(data.Key);
    });
  }

  notifyServer = (filename) => {
    fetch(`${process.env.REACT_APP_ML_ENDPOINT}/?filename=${filename}`)
      .then(resp => {
        if (resp.ok) {
          return resp.json()
        } else {
          return this.setState({
            intersection: 'error'
          })
        }
      })
      .then(data => {
        this.setState({
          intersection: data.map(r => {
            return {
              clusterName: r.cluster,
              lat: r.latitude,
              lng: r.longtitude
            }
          })
        })
      })
      .catch(error => console.log(error) )
  }
}

export default UploadComponent
