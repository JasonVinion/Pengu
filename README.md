# Pengu Network Tools

Welcome to the Pengu Network Tools project! This repository contains a collection of useful network tools packaged into an executable file along with their corresponding source code. These tools are designed to be easy to use without the need for any Python packages or installations.

## Current Issues
- Currently, it is recommended to run the project through the Python source as the exe is running into errors finding files on some systems. (hotfix underway) 

## Project Structure

The project is organized into the following folders:

- `pengu.exe`: The main executable file for Pengu Network Tools.
- `tools/`: This folder contains additional batch and executable files for various network tasks.
- `source/`: This folder contains the source code for all the tools included in this project.


## Features Included

1. **http_ping**
   - A batch file to perform HTTP ping operations.

2. **ping**
   - A batch file to perform standard ping operations.

3. **tcp_ping**
   - A batch file to perform TCP port ping operations.

4. **port_scanner**
   - A Python script for scanning open ports on a specified IP address.

5. **subdomain_finder**
   - A Python script for discovering subdomains for a given domain.

6. **traceroute**
   - A Python script to perform traceroute operations to trace the path packets take to a network host.

7. **Tracker**
   - A Python script to perform WHOIS lookups alongside GeoIP lookups to retrieve domain registration / IP information.

## How to Use

### Running the Executables

Simply download the repository and run the `pengu.exe`

### Running the Source Code

If you prefer to review and run the source code:
1. Navigate to the `source/` folder.
2. Ensure you have Python and the required packages installed.
3. Run the script. 

## Notes

- .exe files were compiled using `auto-py-to-exe`, which is known to cause some false flags in anti-virus programs.
- This project was mostly just for me to try out some new ideas I had, however I will keep it updated. 

## Contributing

Contributions are welcome! Please fork this repository and submit pull requests with your improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Disclaimer

Use these tools responsibly. I and any other authors are not responsible for any misuse or damage caused by these tools.
