# Control Frameworks API

![License](https://img.shields.io/github/license/j-paro/control-frameworks)
![Stars](https://img.shields.io/github/stars/j-paro/control-frameworks?style=social)

## Overview

The Control Frameworks API provides structured access to various cybersecurity control frameworks, allowing users to retrieve and navigate frameworks, categories, and controls via a RESTful interface. This API uses [FastAPI](https://fastapi.tiangolo.com/).

## Supported Frameworks

Currently, the API supports the following control frameworks:

- **NIST CSF v1.1**
- **NIST CSF v2.0**
- **NIST SP 800-171**
- **NIST Privacy Framework**
- **CSA CCM v4.05**
- **CIS CSC v8**

## Roadmap for Future Frameworks

- **ISO 27001**
- **FCAT**
- **NIST SP 800-53**
- **NIST SP 800-66**
- **NIST SP 800-218**
- **Trusted Services Criteria**
- **PCI DSS v3**
- **PCI DSS v4**

## Roadmap for Future Features

- **Control Mappings**

## Features

- **Structured Data Access:** Retrieve frameworks, categories, and controls efficiently.
- **Categories In a Tree Structure:** Categories can be returned in a hierarchical structure.
- **RESTful API:** Seamlessly integrates with other tools and applications.
- **Search Functionality:** Search for controls and categories based on simple text search.
- **Documentation:** Comprehensive API documentation using Swagger UI.
- **Data Loaded Into Memory on Startup:** Fast access to data with minimal overhead.

## Installation

### Build and Run with Docker

1. **Build the Docker Image:**

   ```bash
   docker build -t control-frameworks-api .
   ```

2. **Run the Docker Container:**

   ```bash
   docker run -d -p 8000:8000 control-frameworks-api
   ```

   The API will be accessible at `http://localhost:8000`.

## API Endpoints

### Frameworks

- **`GET /frameworks`**: Lists all available frameworks.
- **`GET /frameworks/id/{framework_id}`**: Retrieves details of a specific framework.

### Categories

- **`GET /categories/by_framework/{framework_id}`**: Returns categories in a hierarchical structure if applicable.
- **`GET /categories/id/{category_id}`**: Returns details for a specific category.
- **`GET /categories/search`**: Retrieves categories based on the given search string query parameter.
  The term "Category" is generic. E.g., a NIST CSF "Function" is classified as a "Category".

### Controls

- **`GET /controls/id/{control_id}`**: Gets details for a specific control
- **`GET /controls/by_control_string_id/{control_string_id}`**: Retrieves a control or controls based on the given string. This supports partial strings. I.e., this is essentially a search on the "control_string_id". You could use this to get all controls that have "PR.AC" in their string ID.
- **`GET /controls/by_category/{category_id}`**: Returns all controls for the given category, and if the given category has "children", then it returns those controls as well in a tree structure.
- **`GET /controls/by_framework/{framework_id}`**: Returns a flat list of all controls associated with the specified framework.
- **`GET /controls/search`**: Retrieves controls based on the given search string query parameter.

For detailed API documentation, refer to the [API Documentation](http://localhost:8000/docs) once the server is running.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`feature-branch`).
3. Commit your changes with clear messages.
4. Submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/j-paro/control-frameworks/blob/main/LICENSE) file for details.

## Contact

For questions, suggestions, or collaboration opportunities, open an issue or reach out via GitHub.
