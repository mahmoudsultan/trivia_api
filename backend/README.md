# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 


## Error Handling

Errors are returned in json format e.g.:
```
{
    "success": False, 
    "error": 404,
    "message": "resource not found."
}
```

Possible Errors:
- 404: Resource Not Found
- 400: Bad Request
- 422: Unprocessible Entity
- 500: Internal Server Error


## API Endpoints

### Categories

#### GET /categories

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category

- Request Arguments: None

- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.

- Example Response:
```
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}
```

#### GET /categories/:id/questions
- Returns a list of questions linked to this category.

- Example request:
```
curl localhost:5000/categories/3/questions
```

- Example Response:
```
{
  "current_category": {
    "id": 3, 
    "type": "Geography"
  }, 
  "questions": [
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ], 
  "success": true, 
  "total_questions": 2
}
```

### Questions

### GET /questions

- Fetches paginated list of questions along side available categories in the same format mentioned above

- Example Request:

```
curl 'localhost:5000/questions?page=2'
```

- Example Response:

```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": 1, 
  "questions": [
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }, 
    {
      "answer": "One", 
      "category": 2, 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }, 
    {
      "answer": "Jackson Pollock", 
      "category": 2, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }, 
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }, 
    {
      "answer": "Scarab", 
      "category": 4, 
      "difficulty": 4, 
      "id": 23, 
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    }, 
    {
      "answer": "Yes", 
      "category": 2, 
      "difficulty": 3, 
      "id": 24, 
      "question": "Is this project bad ?"
    }, 
    {
      "answer": "Yes", 
      "category": 2, 
      "difficulty": 3, 
      "id": 25, 
      "question": "Is this really project bad ?"
    }, 
    {
      "answer": "Yes", 
      "category": 2, 
      "difficulty": 3, 
      "id": 26, 
      "question": "Is this really project bad ?"
    }
  ], 
  "success": true, 
  "total_questions": 45
}
```

#### DELETE /questions/:id

- Deletes a specific questions by id.

- Example Request:
```
curl -X DELETE localhost:5000/questions/9
```
- Example Response:

```
{
    "question": {
        "answer": "Muhammad Ali", 
        "category": 4, 
        "difficulty": 1, 
        "id": 9, 
        "question": "What boxer's original name is Cassius Clay?"
  }, 
  "success": true
}
```

#### POST /questions
- Creates a new question linked to a specific category.

- Example Request:
```
curl -X POST localhost:5000/questions -H "Content-Type: application/json" -d '{ "question": "question", "answer": "answer", "category": 1, "difficulty": 2 }'
```

- Example Response

```
{
  "question": {
    "answer": "answer", 
    "category": 1, 
    "difficulty": 2, 
    "id": null, 
    "question": "question"
  }, 
  "success": true
}
```

#### POST /questions/search
- Returns a list of questions which title matches a search term.

- Example Request:
```
curl -X POST localhost:5000/questions/search -H "Content-Type: application/json" -d '{"searchTerm": "fantasy"}'
```

- Example Response:
```
{
  "questions": [
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ], 
  "success": true, 
  "total_questions": 1
}
```

### Quizzes

#### POST /quizzes
- Uses a category id and a list of questions ids returns a random question in this category and is not included in the previous questions list.

- Example Request:

```
curl -X POST localhost:5000/quizzes -H "Content-Type: application/json" -d '{ "quiz_category": { "type": "Science", "id": 1}, "previous_questions": ["20"]}'
```

- Example Response:
```
{
  "question": {
    "answer": "Question Answer", 
    "category": 1, 
    "difficulty": 1, 
    "id": 51, 
    "question": "Question Title"
  }, 
  "success": true
}
```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```