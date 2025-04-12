# Code Citations

## License: Apache_2_0
https://github.com/Zero-True/zero-true/tree/0836c0f30fb6e46175e91c0f6af93a0ae017d71a/.github/workflows/run_tests.yml

```
:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-
```


## License: desconocido
https://github.com/kh3dron/scifi-database/tree/b7bf30754a1c007cd46a3d268a3f4a74368805b8/.github/workflows/readme_generator.yml

```
- name: Checkout code
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: 3.9

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install
```


## License: desconocido
https://github.com/Pahlwan/flask_app/tree/43beebaf60215d72547179c17aa115505919496a/.github/workflows/test-and-deploy.yml

```
actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: 3.9

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name
```

