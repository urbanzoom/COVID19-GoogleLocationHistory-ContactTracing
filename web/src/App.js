import React from 'react'
import UploadComponent from './components/upload_component'

function App() {
  return (
    <div className='container'>
      <h1 className='text-center mt-3'>Covid-19 contact tracing</h1>
      <div className='row'>
        <img className='mb-3' src='/heatmap.jpg' />
        <UploadComponent></UploadComponent>
      </div>
      <hr />
      <div className='row'>
        <div className='col-12 mt-3'>
          <div className='font-weight-bold'>What is this?</div>
          <p>
            This is an open source project for contact tracing of COVID-19 virus by leveraging your personal Location History recorded by Google<sup>*</sup>.
          </p>
        </div>
      </div>
      <section className='row'>
        <div className='col-12'>
          <div className='font-weight-bold'>FAQs:</div>
          <dl className='faq__list'>
            <dt>How do I get more info on this project?</dt>
            <dd>Check out this subreddit post on <a href='https://www.reddit.com/t/coronavirus/' alt='Coronavirus on Redit'>r/coronavirus</a>. We will try our best to answer all your questions (not found on FAQs) as possible over at Reddit. </dd>

            <dt id='how-does-this-work'>How does this work?</dt>
            <dd>We use your Location History recorded by Google (see <a href='/'>how to download your own Location History</a>) to run against a database of known clusters of COVID-19. </dd>

            <dt>Where do you source for your known clusters of COVID-19?</dt>
            <dd>As an initial demo of the project, we just take the publicly announced clusters from Malaysia and Singapore. We hope to quickly open up access to other folks so that this can be crowd-sourced from the community around the world to contribute to an ever-growing repository of possible COVID-19 clusters or previous visited locations by COVID-19 patients.</dd>

            <dt>Is my privacy protected?</dt>
            <dd>
              When you upload your Location History file, we will run it against our database for a brief moment. Once that process is completed, your file will be immediately deleted. We have no intention of storing your Location History file. We also won’t be collecting your name or contact number.
              <br /><br />
              Over time, as we open up access to other folks who have access to relevant contact tracing sources, we may ask for certain verification. More updates when that happens.
            </dd>

            <dt>I’m a government official with access to relevant contact tracing data of infected patients. How can I contribute?</dt>
            <dd>Please reach out to <a href='mailto:contact.tracing.org@gmail.com'>contact.tracing.org@gmail.com</a>. We will liaise with you from there. </dd>

            <dt>I’m a software developer or data scientist or cybersecurity experts or basically a geek. How can I contribute?</dt>
            <dd>The source code is available here on <a href='https://github.com/urbanzoom/covid-19' alt='GitHub Repo'>GitHub</a>. Feel free to contribute or clone this project to further improve on it. This is meant to be just a proof of concept. We certainly don’t have all the answers (probably we don’t even know what’re the proper questions to ask in the first place) but we believe we should just build it super quick and let the world build upon it. </dd>

            <dt>Who’s behind this project?</dt>
            <dd>This was done over a weekend by a few friends (we’re all teammates in a <a href='https://www.urbanzoom.com' alt='UrbanZoom' title='UrbanZoom'>small proptech startup</a> based in Singapore). We are Niresh, Malai, Shinn, Shawn & Michael.</dd>
          </dl>
        </div>
      </section>
      <small className='mb-3'>
        <sup>*</sup> We are not affiliated, associated, authorized, endorsed by, or in any way officially connected with Google, or any of its subsidiaries or its affiliates.
      </small>
    </div>
  );
}

export default App;
