<a name="readme-top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="#">
    <img src="./about/projLogo.png" alt="Logo" width="200">
  </a>
  <div style="font-size:10px;margin:20px;">
    <a href="https://www.flaticon.com/free-icons/email" title="email icons">Email icons created by ChilliColor - Flaticon</a>
  </div>

  <h1 align="center">Batch Messages Handler</h1>

  <p align="center" style="font-size:16px">
    A tool for processing messages stored in csv file
    <br />
  </p>
</div>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#built-with">Built With</a></li>
    <li><a href="#note-about-building-app">Note about building app</a></li>
    <li><a href="#functions-showcase">Functions Showcase</a></li>
  </ol>
</details>


<!-- ABOUT THE PROJECT -->
## About The Project

![frontpage](/about/screenshot.PNG)

### Backend API server
  This server offers two HTTP routes and a socket connection:
  * For http requests:
    * root (**/**): Respond with the app interface to the client.
    * **exitSignal**: Initiates the server process shutdown.
  * For socket connection:
    * **send_mails**: Manage mail sending, provide results for each sending in real time, and record all outcomes (success and failures) in the corresponding files (**Processed_list.txt**, **error.log**) for future tracing. 
  
  Note: In this project, two server implementations, Flask and Sanic, are available. If you are concerned about the workload of the mail processing API (not referring to **send_mails** API), choose the Flask server. Alternatively, for enhanced mail sending efficiency, consider using the Sanic server. 


### Frontend layout architecture
  ![layout architecture](/about/batchMsgHandler_layout.png)

  The diagram above provides a straightforward depiction of this application's layout. Three main blocks, **DataField**, **OperationField**, and **MailHandler** are in this app. Here are the details about each block: 

  * **DataField**: Presents the content of the imported CSV file in a tabular format.
  * **OperationField**:
    * Manage content operations such as *create*, *edit*, and *delete* for rows, columns, and cells.
    * Facilitate time configuration for mails' public release.
    * Offer corresponding configurations for mapping table columns to mail field.
    * Provides options to export and clear the current table content (to import another csv file).
    * Include a function to gracefully turn off the app.
  * **MailHandler**:
    * Display current configuration including column to field correspondence and mail public release time.
    * Initiate mail sending request and display current processing progress.


<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Built With

### Frontend (batch message handler)
* [![Vue][Vue-badge]][Vue-url]
* [![Quasar][Quasar-badge]][Quasar-url]
* [![Axios][Axios-badge]][Axios-url]
* [![Fontawesome][Fontawesome-badge]][Fontawesome-url]
* [![Socketio][Socketio-badge]][Socketio-url]

### Backend (api server)
* [![Flask][Flask-badge]][Flask-url]
* [![flask_socketio][flask_socketio-badge]][flask_socketio-url]
* [![Sanic][Sanic-badge]][Sanic-url]


<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Note for building
Here are the solutions when running the artifact built by `pyinstaller`
* ValueError: Invalid async_mode specified
  * flask_server.spec: Add `engineio.async_drivers.threading` to the property `hiddenimports`.
  * sanic_server.spec: Add `engineio.async_drivers.sanic` to the property `hiddenimports`.
* **[sanic server]** Infinite process spawn occur on Windows
  * sanic_server.py: Make sure the function `freeze_support` is called in main module.
  ```sh
  if __name__ == '__main__':
    multiprocessing.freeze_support()
    # main logic code ...
  ```
* **[sanic server]** FileNotFoundError: No such file ro directory (tracerite\style.css)
  * Add this option `--collect-all=tracerite` when using pyinstaller command.
* **[sanic server]** OSError: could not get source code
  * Add this option `--collect-all=sanic` when using pyinstaller command.


## Functions Showcase

### Import data
![Import data](/about/importData.gif)

### Edit content
![Edit content](/about/editContent.gif)

### Add/Delete data
![Add/Delete data](/about/addDelData.gif)

### Config public time
![Config public time](/about/configPublicTime.gif)

### Map column to field
![Map column to field](/about/mapCol2Field.gif)

### Process request
![Process request](/about/processReq.gif)


<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[product-screenshot]: images/screenshot.PNG

[Vue-badge]: https://img.shields.io/badge/Vue-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Quasar-badge]: https://img.shields.io/badge/Quasar-blue?style=for-the-badge&logo=quasar
[Quasar-url]: https://quasar.dev/
[AWS-badge]: https://img.shields.io/badge/Amazon_AWS-232f3e?style=for-the-badge&logo=amazonaws
[AWS-url]: https://aws.amazon.com/tw/
[Fastify-badge]: https://img.shields.io/badge/fastify-027804?style=for-the-badge&logo=fastify
[Fastify-url]: https://fastify.dev/
[Axios-badge]: https://img.shields.io/badge/Axios-purple?style=for-the-badge&logo=axios
[Axios-url]: https://axios-http.com/
[Fontawesome-badge]: https://img.shields.io/badge/Font_awesome-lightyellow?style=for-the-badge&logo=fontawesome
[Fontawesome-url]: https://fontawesome.com/
[DragSelect-badge]: https://img.shields.io/badge/dragSelect-skyblue?style=for-the-badge
[DragSelect-url]: https://dragselect.com/
[Sanic-badge]: https://img.shields.io/badge/sanic-ff2ec0?style=for-the-badge&logo=sanic
[Sanic-url]: https://sanic.dev/en/
[Flask-badge]: https://img.shields.io/badge/Flask-00f7ff?style=for-the-badge&logo=flask
[Flask-url]: https://flask.palletsprojects.com/en/3.0.x/
[Socketio-badge]: https://img.shields.io/badge/socketio-grey?style=for-the-badge&logo=socketdotio
[Socketio-url]: https://socket.io/
[flask_socketio-badge]: https://img.shields.io/badge/flask_socketio-lightgray?style=for-the-badge
[flask_socketio-url]: https://flask-socketio.readthedocs.io/en/latest/


[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com
