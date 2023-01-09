### Glossary...

(terms sometimes used interchangeably in code, with clarifications)

- document / citation

    - There is no database 'document' object. Rather, a document is, conceptually, a `Citation` and associated `Reference` entries.

- record / item / reference

    - These are the same, the database contains `Reference` entries, each of which provide a linkage between a `Citation` entry and `Referent` entries. A `Reference` entry also contain transcription and other information.

- person / entrant / referent

    - An entrant and a referent are the same. The database contains `Referent` entries; a `Referent` is an individual mentioned in a `Reference`.

    - A `Referent` provides a linkage between a `Person` and a `Reference`.

    - The interface currently allows for relationships to be defined between `Referent` entries.

----

### Installation...

(Assumes [Docker](https://www.docker.com) is installed and running.)

- Create a local "stuff" directory (name it anything) -- and from your terminal, cd into it (one-time step)

From the terminal...

- Run `git clone git@github.com:Brown-University-Library/stolen_relations_start_data.git` (a private repo, for now; the data is not yet publicly available) (one-time step)

- Run `git clone git@github.com:Brown-University-Library/disa_dj_project.git` -- and cd into it (one-time step)

- Run `docker-compose up`

The webapp should be running; from a browser, go to <http://127.0.0.1:8000/version/> or <http://127.0.0.1:8000/login/>. 

---