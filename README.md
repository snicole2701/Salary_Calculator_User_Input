# User Input Service

## Introduction
The User Input Service is a microservice developed as part of the Salary Calculator project to validate user-provided data. This microservice ensures that inputs such as the month, year, age, and optional income components conform to strict validation rules, allowing reliable downstream processing.

## Service Overview
Built with Flask, the service provides a lightweight API endpoint /validate that accepts user input in JSON format. It checks the validity of the month (e.g., "January" or "February"), year (integers between 1900 and 2100), age (integers between 0 and 120), and optional income fields such as basic_salary, commission, bonus, overtime, and leave_pay, which are validated to ensure they are positive numbers if provided.

## Validation and Testing
If the input passes validation, the service returns a success response indicating that the data is valid, and if errors are present, detailed messages explain what went wrong. Locally, the service can be tested using pytest to ensure the validation logic operates as expected, providing outputs confirming the functionality.

## Deployment
The microservice is structured to be easily deployed to a test instance or production using Render. Deployment can be automated through CI/CD pipelines configured for testing and deployment after every code update. The deployment process involves several steps:
1.	Containerization: The microservice is containerized using Docker, ensuring consistency across different environments.
2.	Continuous Integration (CI): Automated tests are run on every code commit to ensure that the codebase remains stable and functional.
3.	Continuous Deployment (CD): Once the tests pass, the code is automatically deployed to the staging environment for further testing.
4.	Production Deployment: After successful testing in the staging environment, the code is deployed to the production environment, making the new features and fixes available to users.

## Conclusion
With its robust design, clear functionality, and seamless integration capabilities, this microservice plays a vital role in ensuring consistent and accurate input handling within the Salary Calculator project.
