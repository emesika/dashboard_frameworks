
# Dashboard Frameworks

This repository contains implementations of a dashboard application using various frameworks including Streamlit, Dash, and React.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Directory Structure](#directory-structure)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This project demonstrates the creation of a dashboard application using three different frameworks: Streamlit, Dash, and React. Each implementation utilizes the same dataset and logo for consistency in comparison.

## Features

- **Streamlit Dashboard**
- **Dash Dashboard**
- **React Dashboard**
- Shared assets for logo and styles

## Installation

### Prerequisites

- Python 3.7+
- Node.js and npm (for React)

### Clone the Repository

```sh
git clone https://github.com/emesika/dashboard_frameworks.git
cd dashboard_frameworks
```

### Streamlit

1. Navigate to the Streamlit directory:

    ```sh
    cd streamlit
    ```

2. Install system dependencies:

    ```sh
    sudo dnf install python3-devel
    ```

3. Install the required Python packages:

    ```sh
    pip install -r requirements.txt
    ```

4. Run the Streamlit app:

    ```sh
    streamlit run src/dashboard.py
    ```

### Dash

1. Navigate to the Dash directory:

    ```sh
    cd dash
    ```

2. Install system dependencies:

    ```sh
    sudo dnf install python3-devel
    ```

3. Install the required Python packages:

    ```sh
    pip install -r requirements.txt
    ```

4. Run the Dash app:

    ```sh
    python src/dashboard.py
    ```

### React

1. Navigate to the React directory:

    ```sh
    cd react
    ```

2. Install Node.js and npm:

    ```sh
    sudo dnf install nodejs npm
    ```

3. Install the required npm packages:

    ```sh
    npm install
    ```

4. Start the React app:

    ```sh
    npm start
    ```

## Usage

Each framework-specific directory contains the source code and assets required to run the respective dashboard application. Refer to the [Installation](#installation) section for instructions on setting up and running each framework.

## Directory Structure

```plaintext
dashboard_frameworks/
├── dash/
│   ├── assets/
│   │   ├── styles.css
│   │   └── logo.png
│   ├── src/
│   │   └── dashboard.py
│   └── requirements.txt
├── react/
│   ├── public/
│   │   └── logo.png
│   ├── src/
│   │   └── App.js
│   ├── package.json
│   └── package-lock.json
└── streamlit/
    ├── assets/
    │   ├── styles.css
    │   └── logo.png
    ├── src/
    │   └── dashboard.py
    └── requirements.txt
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes or improvements.

