# Pub Service

This project is a Pub Service application that uses Terraform for infrastructure management and AWS for deployment.

## Prerequisites

- Terraform installed
- AWS CLI installed
- AWS account credentials

## Setup

1. **Clone the repository**

  ```sh
  git clone https://github.com/yourusername/pub-service.git
  cd pub-service
  ```

2. **Update the service URL**

  Open the `variables.tf` file and update the `service_url` variable with your desired URL.

  ```hcl
  variable "service_url" {
    description = "The URL for the service"
    default     = "https://your-service-url.com"
  }
  ```

  Alternatively, you can use [ngrok](https://ngrok.com/) to expose your local service to the internet and get an HTTPS URL.

  ```sh
  ngrok http 80
  ```

  Use the generated HTTPS URL as the `service_url`.

3. **Configure AWS credentials**

  Create a `.env` file in the root directory and fill in your AWS credentials.

  ```sh
  AWS_ACCESS_KEY_ID=your_access_key_id
  AWS_SECRET_ACCESS_KEY=your_secret_access_key
  AWS_DEFAULT_REGION=your_aws_region
  ```
  4. **Check for existing resources**

    If the resources are already available and created on AWS, ask the administrator for the `terraform.tfstate` file and place it into the `iac` folder.

  5. **Apply the Terraform configuration**

    Initialize Terraform and apply the configuration.

    ```sh
    terraform init
    terraform apply
    ```

## Usage

After applying the Terraform configuration, your Pub Service should be up and running at the specified service URL.

## Cleanup

To destroy the infrastructure created by Terraform, run:

```sh
terraform destroy
```

## License

This project is licensed under the MIT License.

## Development

To set up the development environment, follow these steps:

1. **Install Poetry**

  Make sure you have [Poetry](https://python-poetry.org/docs/#installation) installed on your machine.

2. **Install dependencies**

  Use Poetry to install the project dependencies.

  ```sh
  poetry install
  ```

3. **Activate the virtual environment**

  Start a new Poetry shell to activate the virtual environment.

  ```sh
  poetry shell
  ```

4. **Run the application in VSCode**

  Open the project in Visual Studio Code and use the provided `launch.json` configuration to run the application.

  ```json
  {
    "version": "0.2.0",
    "configurations": [
    {
      "name": "Python: Pub Service",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/app.py",
      "console": "integratedTerminal"
    }
    ]
  }
  ```

  You can start the application by pressing `F5` or by selecting the `Run` option in the VSCode interface.

5. **Import Postman collection**

  Use the `Pub Subs POC.postman_collection.json` file to import the collection into Postman for testing the API endpoints.