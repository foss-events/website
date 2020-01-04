# [//foss.events](https://foss.events) website

## Build instructions

Requirements:

* Python >= 3.6
* pipenv
* virtualenv
* PHP => 7.3

```
pipenv install
make
```

Start the dev server

```
cd build
php -S localhost:8000
stunnel3 -d 1337 -r 8000 -p ../data/dev_cert/stunnel.pem -f -P ''
```

You can now access the website locally in your browser [https://localhost:1337/](https://localhost:1337/).

## Contributing

Please read the [contribute section on the website](https://foss.events/#contribute).

Pull requests are welcome as well.
