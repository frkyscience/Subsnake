# SubbberSnake 🐍👀

SubDomain Seeker is a Python tool for enumerating subdomains associated with a domain. It leverages various techniques and sources to discover hidden subdomains efficiently.🕵️‍♂️

## Features✨

- Discover subdomains using DNS queries and web services.
- Save results to a file for further analysis.
- Support for multiple subdomain discovery techniques.
- Fast and reliable subdomain enumeration.


### Installation🔧

1. Clone the repository:
```sh
git clone (https://github.com/frkyscience/Subbersnake)
cd Subbersnake
```
2. Install dependencies
```sh
pip install -r requirements.txt
```

3. Run with Subbersnake.py 
```sh
python main.py
```

### Running the Program🏃

To enumerate subdomains without saving to a file:
```sh
python main.py -s example.com
```


To enumerate subdomains and save the results to a file:
```sh
python main.py -s example.com --save results.txt
```

### Options⚙️
- `-h`: Option to list all the possibile commands in the program.
- `-s`: Specify the domain to enumerate subdomains for.
- `--save`: Optional parameter to save the subdomains to a file.

## Contributing🤝

Contributions are welcome! Feel free to open issues and pull requests.

## License📜
Apache-2.0
