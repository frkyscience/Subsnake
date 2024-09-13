# SubSnake 🐍👀 | GUI Version -> [SubSnake GUI](https://github.com/frkyscience/SubSnakeGUI)  WIP!!!!


SubDomain Seeker is a Python tool for enumerating subdomains associated with a domain. It leverages various techniques and sources to discover hidden subdomains efficiently.🕵️‍♂️
![Schermafbeelding 2024-09-13 063236](https://github.com/user-attachments/assets/6b641eab-850e-4280-8a8f-b364b42b3c7a)

## Features✨

- Discover subdomains using DNS queries and web services.
- Save results to a file for further analysis.
- Support for multiple subdomain discovery techniques.
- Fast and reliable subdomain enumeration.
- Find IP adresses
- Find header response and open ports

### Installation🔧

1. Clone the repository:
git clone (https://github.com/frkyscience/Subbersnake)
cd Subsnake

2. run with python Subsnake.py 


### Running the Program🏃

To enumerate subdomains without saving to a file:
python Subsnake.py -s example.com



To enumerate subdomains and save the results to a file:
python Subsnake.py -s example.com --save results.txt

Example of a pipeline 
python Subnake.py -pc -ipp -s example.com
![Schermafbeelding 2024-09-13 065422](https://github.com/user-attachments/assets/f93e3fe6-7f78-4c74-911a-9e2b57af7983)

### Options⚙️
- `-h`: Option to list all the possibile commands in the program.
- `-s`: Specify the domain to enumerate subdomains for.
- `--save`: Optional parameter to save the subdomains to a file.
-  `-pc`: Probe and print HTTP status codes for each subdomain
-  `-ipp`: Probe and print IP adresss for each subdomain

## Contributing🤝

Contributions are welcome! Feel free to open issues and pull requests.

## License📜

Appache 
