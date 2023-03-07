# Trivia App API Reference

## Getting Started

* **Base URL:** At present this Project can only be run locally and is not hosted as a base URL. the backend app is hosted at the default, `httpp://127.0.0.1:5000/`
* **Authentication:** This version of the application does  not require authentication or API keys.

>## Error Handling
Errors are returned as JSON objects in the following format
<br />


```json
{ 
    "Success": False,
    "error": 400,
    "message": "bad request"
}
```


The API will return the following type of errors when requests fail
* **400:** Bad Request
* **404:** Resource Not Found
* **422:** Not Processable

>## End Points
### `GET '/categories'`
* **General:** Return a list of categories object and success value.
* **Sample request :** `curl --location 'http://127.0.0.1:5000/categories'`
* **Sample Response**
```json
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "success": true
}
```
---
### `GET '/questions'`
* **General:** Return a list of categories object, list of paginated question object and success value.
* **Sample request :** `curl --location 'http://127.0.0.1:5000/questions'` or `curl --location 'http://127.0.0.1:5000/questions?page=2'`
* **Sample Response**
  * In case page is out of bound then `404 not found error` will be returned

```json
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "questions": [
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        }
    ],
    "success": true,
    "totalQuestions": 2
}
```

---
### `POST '/questions'` : For Posting new questions
* **General:** Return success value True or False.
* **Sample request :** 
```curl
curl --location 'http://127.0.0.1:5000/questions' \
--header 'Content-Type: application/json' \
--data '{
            "question": "Here a new question string",
            "answer": "Here a new answer string",
            "difficulty": 1,
            "category": 3
        }'
```
* **Sample Response**
  * In case page is out of bound then `404 not found error` will be returned
```json
{
    "success": true
}
```
---
### `POST '/questions'`: For Searching questions
* **General:** Return list of questions matching search term.
* **Sample request :** 
```curl
curl --location 'http://127.0.0.1:5000/questions' \
--header 'Content-Type: application/json' \
--data '{
    "searchTerm": "new"
}'
```
* **Sample Response**
```json
{
    "questions": [
        {
            "answer": "Heres a new answer string",
            "category": 3,
            "difficulty": 1,
            "id": 25,
            "question": "Heres a new question string"
        },
        {
            "answer": "Here a new answer string",
            "category": 3,
            "difficulty": 1,
            "id": 27,
            "question": "Here a new question string"
        }
    ],
    "success": true,
    "totalQuestions": 2
}
```
---
### `GET '/categories/${id}/questions'` : Get questions by categories
* **General:** Return paginated questions of particular category
* **Sample request :** 
```json
curl --location --request GET 'http://127.0.0.1:5000/categories/2/questions' \
--header 'Content-Type: application/json' \
--data '{
    "searchTerm": "new"
}'
```
* **Sample Response**
```json
{
    "currentCategory": "Art",
    "questions": [
        {
            "answer": "Escher",
            "category": 2,
            "difficulty": 1,
            "id": 16,
            "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
        },
        {
            "answer": "Mona Lisa",
            "category": 2,
            "difficulty": 3,
            "id": 17,
            "question": "La Giaconda is better known as what?"
        }
    ],
    "success": true,
    "totalQuestions": 2
}
```

### `DELETE '/questions/${id}:'` delete question
* **General:** Return success value and no of deleted record
* **Sample request :** `curl --location --request DELETE 'http://127.0.0.1:5000/questions/27'`
* **Sample Response :**
```json
{
    "recordDeleted": 1,
    "success": true
}
```
---
### `POST '/quizzes':` Get next quiz question
* **General:** Return next question for quiz excluding the question id provided in **previous_questions** and belong to particular **category type**
* **Sample request :** 
```json
curl --location 'http://127.0.0.1:5000/quizzes' \
--header 'Content-Type: application/json' \
--data '{
            "previous_questions": [20, 30, 21],
            "quiz_category": {
                "type": "Science",
                "id": "1"
            }
        }'
```
* **Sample Response :** 
```json
{
    "questions": {
        "answer": "Blood",
        "category": 1,
        "difficulty": 4,
        "id": 22,
        "question": "Hematology is a branch of medicine involving the study of what?"
    },
    "success": true
}
```
---