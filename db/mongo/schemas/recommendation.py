schema = {
  "$jsonSchema": {
    "bsonType": "object",
    "required": [
      "model",
      "provider",
      "response",
      "archived",
      "created_at",
      "updated_at"
    ],
    "properties": {
      "model": {
        "bsonType": "string",
        "description": "must be a string and is required"
      },
      "provider": {
        "bsonType": "string",
        "description": "must be a string and is required"
      },
      "response": {
        "bsonType": "object",
        "description": "must be an object and is required"
      },
      "archived": {
        "bsonType": "bool",
        "description": "must be a bool and is required"
      },
      "created_at": {
        "bsonType": "date",
        "description": "must be a date and is required"
      },
      "updated_at": {
        "bsonType": "date",
        "description": "must be a date and is required"
      }
    }
  }
}