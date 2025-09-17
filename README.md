# pdi-budget-tracker

## Setup
```
git clone https://github.com/Gh0stdee/pdi-budget-tracker.git
cd ./pdi-budget-tracker
echo . > .env
uv sync
```

### Add database file name in .env

```
DATABASE = "sqlite:///some_sql_file_name.db"
```

### Select UTF-8 if other encoding is chosen

<img width="560" height="720" alt="image" src="https://github.com/user-attachments/assets/7e23586f-5e68-482b-9848-42c1d819e1ff" />

## Usage

### Interactive Mode Example

#### Select function from function Menu

```
uv run main.py
```

<img width="280" height="180" alt="image" src="https://github.com/user-attachments/assets/287e4e4b-ee5d-404d-98bb-7c50f3a5a8b5" />

#### Create Category

<img width="280" height="180" alt="image" src="https://github.com/user-attachments/assets/280e31c1-56f3-4daf-827e-e8b958594601" />

#### Add Transaction 

<img width="360" height="360" alt="image" src="https://github.com/user-attachments/assets/82de5b4a-837d-4190-ae64-1a45c437bd68" />

#### Show Summary

<img width="540" height="720" alt="image" src="https://github.com/user-attachments/assets/63599515-4b54-49ec-a9bd-bdd9d81b5d62" />

### CLI

#### Add Category

```uv run ty-main.py add-category category_name budget```

#### Show Category

```uv run ty-main.py show-category```

#### Add Transaction

```uv run ty-main.py add-transaction amount remark category_name```

#### Print Summary

```uv run ty-main.py print-summary```
