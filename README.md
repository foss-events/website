# [//foss.events](https://foss.events) website

## Build instructions

Requirements:

* [Node.js](https://nodejs.org/en/download/package-manager/) >= 12
* Python >= 3.6
* pipenv
* make

```
pipenv install
make
```

Start the dev server

```shell script
pipenv run bin/serve.py
```

You may now access the website locally in your browser [https://localhost:1337/](https://localhost:1337/).

## Contributing

Please read the [contribute section on the website](https://foss.events/about.html#contributing).

### Missing an event?

Send an e-mail to [onemore@foss.events](mailto:onemore@foss.events).

### Add an event via Git

* For [this repo](https://github.com/foss-events/website)
* Add you event to [the CSV file](https://github.com/foss-events/website/tree/master/data)
* Optionally [provide a logo](https://github.com/foss-events/website/tree/master/src/img/eventbanners)
* Open a pull request
