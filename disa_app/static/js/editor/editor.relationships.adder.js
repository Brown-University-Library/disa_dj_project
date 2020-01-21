class RelationshipAdder {
  constructor($elem) {
    this._$root = $elem;
    this._ctrl_sbj = $('<select/>', {'class' : 'form-control'});
    this._ctrl_prop = $('<select/>', {'class' : 'form-control'});
    this._ctrl_val = $('<select/>', {'class' : 'form-control'});
    this._ctrl_add = $('<button/>', {'class': 'btn btn-primary add-rel'});
    this._sbj = '';
    this._prop = '';
    this._val = '';
    this.setData = this.setData.bind(this);
    this._$root[0].addEventListener('change', this);

    this.initialize();
  }

  initialize() {
    var $tr, $span,
      $td_sbj, $td_rel, $td_obj, $td_add,
      $sel_sbj, $sel_rel, $sel_obj, $button;
    $tr = $('<tr/>');
    $span = $('<span/>', {'class': 'fas fa-plus-circle'});
    $td_sbj = $('<td/>').append(this._ctrl_sbj);
    $td_rel = $('<td/>').append(this._ctrl_prop);
    $td_obj = $('<td/>').append(this._ctrl_val);
    $td_add = $('<td/>').append(this._ctrl_add.append($span));
    $tr.append($td_sbj).append($td_rel).append($td_obj).append($td_add);
    this._$root.append($tr);
  }

  makeOptions(objectArray) {
    let opts = [];

    for (let i=0; i < objectArray.length; i++) {
      let data = objectArray[i];
      let $opt = $('<option/>', {'value': data.id, 'text': data.name });
      opts.push($opt);
    }

    return opts;
  }

  load(personObjs, relationshipObjs) {
    this._ctrl_sbj.empty().append(this.makeOptions(personObjs));
    this._ctrl_sbj.children().eq(0).prop("selected", true);
    this._ctrl_prop.empty().append(this.makeOptions(relationshipObjs));
    this._ctrl_val.empty().append(this.makeOptions(personObjs));
    this._ctrl_val.children().eq(1).prop("selected", true);

    this.setData();
  }

  getData() {
    let data = {
      'sbj': parseInt(this._sbj),
      'rel': parseInt(this._prop),
      'obj': parseInt(this._val)
    };

    return data;
  }

  setData() {
    this._sbj = this._ctrl_sbj.val();
    this._prop = this._ctrl_prop.val();
    this._val = this._ctrl_val.val();
  }

  flipOption(target) {
    if (this._sbj === this._val) {
      if ($(target).is(this._ctrl_sbj)) {
        this._ctrl_val.find(`option[value!=${this._sbj}]`).eq(0).prop("selected", true);
      } else if ($(target).is(this._ctrl_val)) {
        this._ctrl_sbj.find(`option[value!=${this._val}]`).eq(0).prop("selected", true);
      }
    }
  }

  handleEvent(event) {
    switch(event.type) {
      case "change":
        this.setData();
        this.flipOption(event.target);
        this.setData();
        return;
      default:
        return;
    }
  }
}