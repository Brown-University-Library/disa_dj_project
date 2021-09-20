
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "searchRule": {
        "$ref": "searchRule"
      },
      "resourceSelector": {
        "type": "object",
        "properties": {
          "tag": {
            "oneOf": [
              {
                "type": "integer"
              },
              {
                "type": "array",
                "items": {
                  "type": "integer"
                }
              }
            ]
          },
          "category": {
            "oneOf": [
              {
                "type": "integer"
              },
              {
                "type": "array",
                "items": {
                  "type": "integer"
                }
              }
            ]
          },
          "id": {
            "oneOf": [
              {
                "type": "integer"
              },
              {
                "type": "array",
                "items": {
                  "type": "integer"
                }
              }
            ]
          }
        }
      }
    },
    "required": ["searchRule", "resourceSelector"]
  },
  "$defs": {
    "fieldId": {
      "$id": "fieldId",
      "enum": [
        "all_name", 
        "name_last", 
        "enslavement_status", 
        "sex", 
        "all_tribes", 
        "all_races", 
        "reference_data.all_locations", 
        "year", 
        "reference_data.transcription", 
        "referent_db_id", 
        "vocation", 
        "age", 
        "reference_data.reference_db_id", 
        "enslaved_by", 
        "enslaved",
        "general-search"
      ]
    },
    "searchRule": {
      "$id": "searchRule",
      "anyOf": [
        {
          "$ref": "searchRuleInitialState"
        },
        {
          "$ref": "searchRuleEquals"
        },
        {
          "$ref": "searchRuleIsNotEmpty"
        },
        {
          "$ref": "searchRuleMatches"
        },
        {
          "$ref": "searchRuleAnd"
        },
        {
          "$ref": "searchRuleOr"
        }
      ]
    },
    "searchRuleInitialState": {
      "$id": "searchRuleInitialState",
      "type": "object",
      "properties": {
        "ruleType": {
          "type": "string",
          "const": "init"
        }
      },
      "required": ["ruleType"]
    },
    "searchRuleEquals": {
      "$id": "searchRuleEquals",
      "type": "object",
      "properties": {
        "ruleType": {
          "type": "string",
          "const": "equals"
        },
        "fieldId": {
          "$ref": "fieldId"
        },
        "value": {
          "type": "string"
        }
      },
      "required": [
        "ruleType",
        "fieldId",
        "value"
      ]
    },
    "searchRuleIsNotEmpty": {
      "$id": "searchRuleIsNotEmpty",
      "type": "object",
      "properties": {
        "ruleType": {
          "type": "string",
          "const": "isNotEmpty"
        },
        "fieldId": {
          "$ref": "fieldId"
        }
      },
      "required": [
        "ruleType",
        "fieldId"
      ]
    },
    "searchRuleMatches": {
      "$id": "searchRuleMatches",
      "type": "object",
      "properties": {
        "ruleType": {
          "type": "string",
          "const": "matches"
        },
        "fieldId": {
          "$ref": "fieldId"
        },
        "value": {
          "type": "string"
        }
      },
      "required": [
        "ruleType",
        "fieldId",
        "value"
      ]
    },
    "searchRuleAnd": {
      "$id": "searchRuleAnd",
      "type": "object",
      "properties": {
        "ruleType": {
          "type": "string",
          "const": "and"
        },
        "rules": {
          "type": "array",
          "items": {
            "$ref": "searchRule"
          }
        }
      },
      "required": [
        "ruleType",
        "rules"
      ]
    },
    "searchRuleOr": {
      "$id": "searchRuleOr",
      "type": "object",
      "properties": {
        "ruleType": {
          "type": "string",
          "const": "or"
        },
        "rules": {
          "type": "array",
          "items": {
            "$ref": "searchRule"
          }
        }
      },
      "required": [
        "ruleType",
        "rules"
      ]
    }
  }
}

