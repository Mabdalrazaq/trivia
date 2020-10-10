# Trivia
Trivia is a website were you can find a lot of trivia questions based on a search, a category or randomly!
Questions have initially hidden answers, difficulty from 1-5 and certain categories.
You can add your own questions to owr pool of questions, and you can also play a game were you choose a category and attempt to answer 5 questions from this category, and get a score out of 5 when you finish.
The project uses React for frontend, python flask for backend and Postgresql using SQLALCHEMY ORM for database
This project was part of my Full Stack Developer Nanodegree from Udacity.

## Getting Started
This project is not deployed, but you can easily set it on your local device following these steps:
1. clone this project on your local device
2. Set up the frontend:
    - cd into frontend directory
    - run `npm install` to install all front end dependencies
    - run `npm start`to host the front end on port 3000 on your local host
3. Set up the backend:
    - cd into backend directory
    - run `pip install -r requirements` to install all backend dependencies
    - run `export FLASK_APP=flaskr` and `export FLASK_ENV=development` to configure flask upp
    - run `flask run` to start your flask app server on port 5000 on your local host
    - you can now make requests to this locally set up API using base URL http://localhost:5000
4. Set up database:
    - [download](https://www.postgresql.org/download/) postgresql on your device if you haven't already
    - start your server using [this](https://tableplus.com/blog/2018/10/how-to-start-stop-restart-postgresql-server.html) method
    - run `sudo -u postgres -i` to login as postgres username, to use the postgres database
    - run `createdb trivia` and `createdb trivia_test` to initialize two databases, one of them for testing.
    - run `psql trivia < trivia.psql` and `psql trivia_test < trivia.psql` to seed data into both trivia and trivia_test databases
5. Open https://localhost:3000 on your browser and you are ready to go!

#### Tests
You can edit flaskr_test.py to edit the tests, and you can run them whenever using
    ```
    dropdb trivia_test
    createdb trivia_test
    psql trivia_test < trivia.psql
    python test_flaskr.py
    ```

## API Reference
- The API for this project defines the process of speaking to the flask server.
- For all API transactions we use the baseUrl http://localhost:5000.
- CORS is enabled for all origins and all methods.
#### Endpoints
- GET /categories
    - Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
    - Request Arguments: None
###### Response
```
{
"success":true
"categories":[
  {
  "id",
  "type": type of category, i.e: science,art,etc...
  },
...
]
}
```

- GET /questions
    - Fetches a dictionary of questions paginated based on the page, each page holds a maximum of 10 querys.
    - Request Arguments:
        - page: the page you are on, if not specified you get questions belonging to page 1
        - current_category: the category id to fetch all questions from, if not specified, or if it is a string with a value of 'null', all questions are fetched
        - search_term: a string specifying a search operation, searches are case insensetive, if not specified, all qestions are fetched
###### Response
```
{
"success":true
"questions":[
  {
  "id",
  "question": string representing the question text,
  "answer": string representing the answer text,
  "category": integer representing category id of question,
  "difficulty": integer representing difficulty of question from 1 to 5
  },
...
]
"total_questions":integer: number of total questions based on category or search, not only these paginated in questions,
"current_category": integer: category of fetched questions, None if not specified in URL
"categories": list of all categories, categories response is demonistrated in another response.
}
```

- DELETE /questions/:id
    - Deletes question specified from database.
    - Request Arguments: None
###### Response
```
{
"id":id of deleted question
"success":true
}
```

- POST /questions
    - Creates a new question, or initializes a new search
    - Request Body:
        - searchTerm: if specified, then it is a search, if not then it is a create
        - question: string representing question text
        - answer: string representing answer text
        - difficulty: integer representing difficulty from 1 to 5
        - category: integer representing category id of question

###### Response
1. create:
```
{
"created":id of created question
"success":true
}
```

2. search:
```
{
"success":true,
'questions':searched questions paginated
"total_questions":Number of total searched questions
"current_category":always None here
}
```

- GET /categories/:id/questions
    - Returns all questions from certain category
    - Request Arguments: None
###### Response 
```
{
"success":true,
"questions":specified categories' questions paginated,
"total_questions":Number of total questions in this category,
"current_category":id of current category
}
```

- POST /quizzes
    - Returns a random question based on a category that is not part of a list of questions
    - Request Body:
        - previous_questions: a list of questions ids, returned question must not be one of them
        - quiz_category: integer specifying the category of wanted question, if 0 then all categories
###### Response 
```
{
"success":true,
"question" A random question that is from category specified and not one of previous questions specified
}
```

#### Errors
All errors follow the following form:

```
{
"success":false,
"error": status code
"message": error message
}
```

## Auhtors
- Udacity: All starting code
- Mohammad Abdallah: Implementation and documentation and testing












