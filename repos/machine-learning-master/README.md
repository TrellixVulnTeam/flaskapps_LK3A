# Machine Learning [![Build Status](https://travis-ci.org/jeff1evesque/machine-learning.svg?branch=master)](https://travis-ci.org/jeff1evesque/machine-learning) [![Coverage Status](https://coveralls.io/repos/github/jeff1evesque/machine-learning/badge.svg?branch=master)](https://coveralls.io/github/jeff1evesque/machine-learning?branch=master)

This project provides a [web-interface](https://github.com/jeff1evesque/machine-learning/blob/master/README.md#web-interface),
 as well as a [programmatic-api](https://github.com/jeff1evesque/machine-learning/blob/master/README.md#programmatic-interface)
 for various machine learning algorithms.

**Supported algorithms**:

- [Support Vector Machine](https://en.wikipedia.org/wiki/Support_vector_machine) (SVM)
- [Support Vector Regression](https://en.wikipedia.org/wiki/Support_vector_machine#Regression) (SVR)

## Contributing

Please adhere to [`contributing.md`](https://github.com/jeff1evesque/machine-learning/blob/master/contributing.md),
 when contributing code. Pull requests that deviate from the
 [`contributing.md`](https://github.com/jeff1evesque/machine-learning/blob/master/contributing.md),
 could be [labelled](https://github.com/jeff1evesque/machine-learning/labels)
 as `invalid`, and closed (without merging to master). These best practices
 will ensure integrity, when revisions of code, or issues need to be reviewed.

**Note:** support, and philantropy can be [inquired](https://jeff1evesque.github.io/machine-learning.docs/latest/html/contribution/support),
 to further assist with development.

## Configuration

Fork this project, using of the following methods:

- [simple clone](https://jeff1evesque.github.io/machine-learning.docs/latest/html/configuration/setup-clone#simple-clone):
 clone the remote master branch.
- [commit hash](https://jeff1evesque.github.io/machine-learning.docs/latest/html/configuration/setup-clone#commit-hash):
 clone the remote master branch, then checkout a specific commit hash.
- [release tag](https://jeff1evesque.github.io/machine-learning.docs/latest/html/configuration/setup-clone#release-tag):
 clone the remote branch, associated with the desired release tag.

## Installation

To proceed with the installation for this project, users will need to decide
whether to use the rancher ecosystem, or use `docker-compose`. The former will
likely be less reliable, since the corresponding install script, may not work
nicely across different operating systems. Additionally, this project will
assume rancher as the primary method to deploy, and run the application. So,
when using the `docker-compose` alternate, keep track what the corresponding
[endpoints](https://github.com/jeff1evesque/machine-learning/blob/master/README.md#execution)
should be.

If users choose rancher, both docker and rancher must be installed.
Installing docker must be done manually, to fulfill a set of [dependencies](https://jeff1evesque.github.io/machine-learning.docs/latest/html/installation/dependencies).
Once completed, rancher can be installed, and automatically configured, by simply
executing a provided bash script, from the docker quickstart terminal:

```bash
cd /path/to/machine-learning
./install-rancher
```

**Note:** the installation, and the configuration of rancher, has been [outlined](https://jeff1evesque.github.io/machine-learning.docs/latest/html/installation/rancher)
if more explicit instructions are needed.

If users choose to forgo rancher, and use the `docker-compose`, then simply
install `docker`, as well as `docker-compose`. This will allow the application
to be deployed from any terminal console:

```bash
cd /path/to/machine-learning
docker-compose up
```

**Note:** the installation, and the configuration of `docker-compose`, has been [outlined](https://jeff1evesque.github.io/machine-learning.docs/latest/html/installation/docker-compose)
if more explicit instructions are needed.

## Execution

Both the web-interface, and the programmatic-api, have corresponding
 [unit tests](https://github.com/jeff1evesque/machine-learning/blob/master/doc/test/pytest.rst)
 which can be reviewed, and implemented. It is important to remember,
 the installation of this application will dictate the endpoint. More
 specifically, if the application was installed via rancher, then the
 endpoint will take the form of `https://192.168.99.101:XXXX`. However,
 if the `docker-compose up` alternate was used, then the endpoint will
 likely change to `https://localhost:XXXX`, or `https://127.0.0.1:XXXX`.

### Web Interface

The [web-interface](https://github.com/jeff1evesque/machine-learning/blob/master/interface/templates/index.html),
 can be accessed within the browser on `https://192.168.99.101:8080`:

![web-interface](https://user-images.githubusercontent.com/2907085/39499223-97b96fce-4d7a-11e8-96e2-c4e31f6b8e09.JPG 'web-interface')

The following sessions are available:

- `data_new`: store the provided dataset(s), within the implemented sql
 database.
- `data_append`: append additional dataset(s), to an existing representation
 (from an earlier `data_new` session), within the implemented sql database.
- `model_generate`: using previous stored dataset(s) (from an earlier
- `data_new`, or `data_append` session), generate a corresponding model into
- `model_predict`: using a previous stored model (from an earlier
 `model_predict` session), from the implemented nosql datastore, along with
 user supplied values, generate a corresponding prediction.

When using the web-interface, it is important to ensure the csv, xml, or json
 file(s), representing the corresponding dataset(s), are properly formatted.
 Dataset(s) poorly formatted will fail to create respective json dataset
 representation(s). Subsequently, the dataset(s) will not succeed being stored
 into corresponding database tables. This will prevent any models, and subsequent
 predictions from being made.

The following dataset(s), show acceptable syntax:

- [CSV sample datasets](https://github.com/jeff1evesque/machine-learning/tree/master/interface/static/data/csv/)
- [XML sample datasets](https://github.com/jeff1evesque/machine-learning/tree/master/interface/static/data/xml/)
- [JSON sample datasets](https://github.com/jeff1evesque/machine-learning/tree/master/interface/static/data/json/web_interface)

**Note:** each dependent variable value (for JSON datasets), is an array
 (square brackets), since each dependent variable may have multiple
 observations.

### Programmatic Interface

The programmatic-interface, or set of API, allow users to implement the
 following sessions:

- `data_new`: store the provided dataset(s), within the implemented sql
 database.
- `data_append`: append additional dataset(s), to an existing representation
 (from an earlier `data_new` session), within the implemented sql database.
- `model_generate`: using previous stored dataset(s) (from an earlier
- `data_new`, or `data_append` session), generate a corresponding model into
- `model_predict`: using a previous stored model (from an earlier
 `model_predict` session), from the implemented nosql datastore, along with
 user supplied values, generate a corresponding prediction.

A post request, can be implemented in python, as follows:

```python
import requests

endpoint = 'https://192.168.99.101:9090/load-data'
headers = {
    'Authorization': 'Bearer ' + token,
    'Content-Type': 'application/json'
}

requests.post(endpoint, headers=headers, data=json_string_here)
```

**Note:** more information, regarding how to obtain a valid `token`, can be further
 reviewed, in the `/login` [documentation](https://jeff1evesque.github.io/machine-learning.docs/latest/html/programmatic-interface/authentication/login).

**Note:** various `data` [attributes](https://jeff1evesque.github.io/machine-learning.docs/latest/html/programmatic-interface/data-attributes) can be nested in above `POST` request.

It is important to remember that the [`docker-compose.development.yml`](https://github.com/jeff1evesque/machine-learning/blob/3889788a8343a4b7cef2cf84166f9bd35d83021c/docker-compose.development.yml#L33-L43),
 has defined two port forwards, each assigned to its corresponding reverse
 proxy. This allows port `8080` on the host, to map into the `webserver-web`
 container. A similar case for the programmatic-api, uses port `9090` on the
 host.
