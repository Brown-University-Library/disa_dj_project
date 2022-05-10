### notes

- references
    - <https://en.wikipedia.org/wiki/HATEOAS>
    - <https://repository.library.brown.edu/studio/api-docs/>

- goals
    - cleanest possible api to reflect data
    - most useful (minimal extraneous stuff) data returned for interface-purpose

- I'm using the term `referent_relationship` a lot because there's a world of interesting things we could do with the _concept_ of relationships apart from individuals. Example: ```'Newport' --> 'had-the-name-of__by-local-native-americans__in-1750' --> 'X'```. So I'm explicitly reminding myself that this relationship project is not that.

---


### list of all referent-relationships

- GET
- `/referent_relationships/list/`
- (don't think this is useful -- putting it here for mental exercise completeness)

```
{
    'meta': {
        'count': 1,234,
        'range_start': 0,
        'range_end': 100
    },
    'relationships': [
        'https.../referent_relationships/123',
        'https.../referent_relationships/124',
        etc
    ]
}
```

---


### list of specific referent-relationships

- GET
- `/referent_relationships/123,124/`

```
{
    'meta': {
        ?
    },
    'referent_relationships': [
         {
            'relationship_id': '123',
            'subject_referent': 'https.../referent/987',
            'object_referent': 'https.../referent/783',
            'relationship_string': 'is-the-same-person-as',  # always this, yes? Not, eg `Father of`
            'confidence': 'high',
            'approved': 'yes'
        },
         {
            'relationship_id': '124',
            'subject_referent': 'https.../referent/321',
            'object_referent': 'https.../referent/956',
            'relationship_string': 'is-the-same-person-as',
            'confidence': 'medium',
            'approved': 'no'
        },
    ]

}
```

- BIG QUESTION -- are we _ONLY_ having the single ``is-the-same-as` relationship for this referent-relationship project? And letting stuff like 'Father-of' be inferred (for the other is-the-same-as person)>
- Only relevant if we're doing stuff like "Father of" -- type' could be one of: [ 'document', 'inferred_auto', 'inferred_candidate', 'inferred_approved' ]
- Q: do we want to track the user that establishes the relationship, and the user who 'approves' it?

---


### list of referent-relationships for a specific referent

- GET
- `/referent_relationships/referent/123/`

```
{
    'meta': {
        'count': 6
        ?
    },
    'referent_relationships': [
        'https.../referent_relationships/123',
        'https.../referent_relationships/124',
        etc
    ]
}
```

- possible idea (don't think it's a good one) -- break out the referent_relationships by type, so the list of explicitly-entered ones from the document, and then the list of inferred-ones, etc -- with counts reflecting those.
