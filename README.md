# server-monitor-dashboard

## Status

[![Download](https://api.bintray.com/packages/geldtech/debian/server-monitor-dashboard/images/download.svg)](https://bintray.com/geldtech/debian/server-monitor-dashboard#files)
[![Build Status](https://travis-ci.org/geld-tech/server-monitor-dashboard.svg?branch=master)](https://travis-ci.org/geld-tech/server-monitor-dashboard)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)


## Description

Server monitoring dashboard Web UI built with Python Flask and Vue.js


## Demo

A sample demo of the project is hosted on <a href="http://geld.tech">geld.tech</a>.


## Usage

* Install the repository information and associated GPG key (to ensure authenticity):
```
$ echo "deb https://dl.bintray.com/geldtech/debian /" | sudo tee -a /etc/apt/sources.list.d/geld-tech.list
$ sudo apt-key adv --recv-keys --keyserver keyserver.ubuntu.com EA3E6BAEB37CF5E4
```

* Update repository list of available packages and clean already installed versions
```
$ sudo apt update
$ sudo apt clean
```

* Install package
```
$ sudo apt install server-monitor-dashboard
```

* Reload services and start ours
```
$ sudo systemctl daemon-reload
$ sudo systemctl start server-monitor-dashboard
$ sudo systemctl status server-monitor-dashboard
```


## Development

Use `local-dev.sh` script to build and run locally the Flask server with API and the Vue web application with DevTools enabled for [Firefox](https://addons.mozilla.org/en-US/firefox/addon/vue-js-devtools/) and [Chrome](https://chrome.google.com/webstore/detail/vuejs-devtools/nhdogjmejiglipccpnnnanhbledajbpd):

```
$ ./local-dev.sh
```
Then, access the application locally using a browser at the address: [http://0.0.0.0:5000/](http://0.0.0.0:5000/).
