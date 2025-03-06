
# **Scalable Domain Validator**

## **Overview**
The **Scalable Domain Validator** is a Python script designed for bulk validation of domain names. It efficiently checks domain status, including availability, HTTP status codes, and potential redirections. Using **Dask** for parallel processing, it can handle large datasets of domains, ensuring scalability and performance.

## **Key Features**
- **Parallelised Domain Validation**: Leverages **Dask** for parallel domain checks, speeding up processing for large datasets.
- **Flexible Domain Checking**: Supports multiple URL prefixes (e.g., `http://`, `https://`, `www.`) for thorough validation.
- **Detailed Reporting**: Includes HTTP status codes, domain validity, and redirection details.
- **Scalability**: Optimised for processing large volumes of domain data using **Dask**'s distributed computing model.
- **CSV Input/Output**: Reads from and writes to CSV files for easy integration.

## **Technologies & Tools**
- **Python**: Used for scripting and implementing domain validation.
- **Dask**: A parallel computing framework for distributed task execution, boosting performance for large datasets.
- **Requests**: For making HTTP requests to domains and retrieving their status.
- **Pandas**: Handles reading, processing, and saving data in CSV format.
- **Regex**: Cleans and standardises domain names before checking.

## **Installation**
Ensure you have the following dependencies installed:

```bash
pip install requests pandas dask
```

## **Usage**

### **Input Data Format**
The input file must be a CSV with domain names in the first column. Example of `input.csv`:
```csv
domain1.com
example.org
website.net
```

### **Sample Output (`output.csv`)**
```csv
input domain,status code,status,redirected domain
domain1.com,200,Valid,
example.org,301,Redirected,www.example.org
website.net,404,Invalid,
```

The output CSV will contain:
- **input domain**: The original domain.
- **status code**: HTTP status code.
- **status**: Domain status (**Valid**, **Invalid**, or **Redirected**).
- **redirected domain**: The final URL if redirected.

## **Code Architecture**

### **Functions**
1. **`clean_domain(url)`**: Removes prefixes like `http://`, `https://`, `www.`, and trailing slashes for consistent validation.
2. **`check_domain_for_dask(domain, prefixes, session)`**: The core function wrapped with **Dask**'s `delayed` decorator for parallel execution. It validates a domain with multiple prefixes and returns its status and redirection info.
3. **`check_domain_status(input_file, output_file)`**: Reads domain list, processes them in parallel using **Dask**, and saves results to an output CSV.

## **Security Considerations**
- **Sensitive Data**: Secure any credentials or API keys by using environment variables.
- **Rate Limiting**: Domains may block repeated requests. Implement rate-limiting or use proxies when working with large datasets.

## **Contributing**
Feel free to fork the repository, make changes, and submit pull requests. Contributions and suggestions are welcome!
