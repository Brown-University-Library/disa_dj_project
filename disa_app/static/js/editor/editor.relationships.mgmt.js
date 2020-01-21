class RelationshipMgmt {
  constructor (sectionId, source, $elem) {
    this._section = sectionId;
    this._source = source;
    this._$root  = $elem;
    this._store = new RelationshipStore($elem.find('.rel-store'));
    this._adder = new RelationshipAdder($elem.find('.rel-adder'));
    this._$root[0].addEventListener('click', this);
    this.setUp = this.setUp.bind(this);
  }

  load() {
    this._source.getRelationships(this._section);
  }

  setUp(data) {
    this._store.load(data.store);
    this._adder.load(data.people, data.relationships);
  }

  handleEvent(event) {
    switch(event.type) {
      case "click":
        let btn = event.target.closest('button');
        if (btn.classList.contains('add-rel')) {
          let obj = this._adder.getData();
          obj['section'] = this._section;
          this._source.addRelationship(obj);
        } else if (btn.classList.contains('del-rel')) {
          let rel_id = parseInt(btn.getAttribute('data-rel-id'));
          this._source.deleteRelationship(this._section, rel_id);
        }
        return;
      default:
        return;
    }
  }
}