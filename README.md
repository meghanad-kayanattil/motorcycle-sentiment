# What do people say about a motorcycle?

## A ready to deploy real time sentiment analysis web app
### Made with HTML+CSS front end and Flask (Python) back end using latest Transformers NLP models. Dockerized and ready to deploy



This repository contains a web app devoleped for assessing the sentiment for motorcycles from comments including their name available from different popular subreddits. 
The program uses <code> psaw </code> to scrape the target subreddit within a given time frame and the resulting data is analysied with the help of popular Natural Language Processing library <code>Transformers</code>.

All of this process is implementad in the backend of the webapp using the popular <code>Flask</code> library in Python, with correspondingly written <code>html</code> front end which is further styled using <code>css</code> style file. 



## Screenshots

![App Screenshot](https://via.placeholder.com/468x300?text=App+Screenshot+Here)


## Run Locally

Clone the project

```bash
  git clone https://link-to-project
```

Go to the project directory



Install dependencies

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  flask run
```
Go to the default port displayed in your terminal and add a "/home" to the end of the weblink

