on this page...
- Glossary
- Installation
- Typical usage

---
### Glossary...

(terms sometimes used interchangeably in code, with clarifications — the first listed option is the one currently used by the project)

- **source** / document / citation

    - There is no database 'document' object. Rather, a document is, conceptually, a `Citation` and associated `Reference` entries.

- **record** / item / reference

    - These are the same, the database contains `Reference` entries, each of which provide a linkage between a `Citation` entry and `Referent` entries. A `Reference` entry also contain transcription and other information.

- **referent** / person / entrant

    - An entrant and a referent are the same. The database contains `Referent` entries; a `Referent` is an individual mentioned in a `Reference`.

    - A `Referent` provides a linkage between a `Person` and a `Reference`.

    - The interface currently allows for relationships to be defined between `Referent` entries.

-----

### Installation...

(Assumes [Docker](https://www.docker.com) is installed and running.)

- Create a local "stuff" directory (name it anything) -- and from your terminal, cd into it (one-time step)

From the terminal, run:

- `git clone git@github.com:Brown-University-Library/stolen_relations_start_data.git`<br />_(a one-time step; downloading the SR data) Note that this is a private repo, for now; the data is not yet publicly available_

- `git clone git@github.com:Brown-University-Library/disa_dj_project.git`<br/>_(a one-time step, downloads the SR codebase)_

- `cd disa_dj_project`<br />_Sets the current directory to disa\_dj\_project_

- `docker-compose up`<br />_Creates the container (which starts the webapp)_

The webapp should be running; from a browser, go to `http://127.0.0.1:8000/version/` or `http://127.0.0.1:8000/login/`. 

---

### Typical usage...

- `cd <SOME_PATH>/disa_dj_project`<br />_Sets the current directory to disa\_dj\_project_

- `docker-compose up`<br />_Creates the container (which starts the webapp)_

Note: if a code-update installs a new python-package, either:

- delete the `disa_dj_project-web` image which should force it to be rebuilt (best option), **or...**
    
- run `docker-compose up --build` to force the container to be rebuilt. (I don't think this actually creates a new image, so subsequent runs of `docker-compose up` will still use the old image.)

---
