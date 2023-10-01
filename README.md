# massive

This project aims to process the [massive](https://huggingface.co/datasets/AmazonScience/massive) dataset, focusing on generating language-specific files, such as en-xx.xlsx, for multiple languages and creating separate JSONL files for English (en), Swahili (sw), and German (de) with test, train, and dev data. Additionally, it will generate a single JSON file that contains translations from English to all languages with id and utt for the training sets. This project is designed to efficiently handle the dataset without using recursive algorithms to avoid potential memory and time complexity issues.

## Prerequisites

- Python version 3.11.5
- PyCharm version 2023.2.1

## Installation

1. Clone the repository on your local machine:

```sh
  https://github.com/mikemwai/massive.git
```

2. Navigate to the project directory and create a virtual environment on your local machine through the command line:

```sh
  py -m venv myenv
```

3. Activate your virtual environment:

- On Windows:

```sh
  myenv\Scripts\activate
```

- On Mac:

```sh
  source myenv/bin/activate
```

4. Install project dependencies on your virtual environment:

```sh
  pip install -r requirements.txt
```

5. Extract the [dataset folder](dataset.rar) on your project folder.

## Usage

Run the project on the IDE terminal:

```sh
   python main.py generate_excel_files separate_files train_translations
```

## Contributing

If you'd like to contribute to this project:

- Please fork the repository
- Create a new branch for your changes
- Submit a [pull request](https://github.com/mikemwai/massive/pulls)

Contributions, bug reports, and feature requests are welcome!

## Issues

If you have any issues with the project, feel free to open up an [issue](https://github.com/mikemwai/massive/issues).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
