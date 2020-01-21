class RelationshipStore {

  constructor($elem) {
    this._$root = $elem;
    this._data = [];
    this._$root[0].addEventListener('mouseover', this);
    this._$root[0].addEventListener('mouseout', this);
  }

  compareData(d1, d2) {
    if (d1.data.sbj.name < d2.data.sbj.name) { 
      return -1;
    }
    if (d1.data.sbj.name > d2.data.sbj.name) {
      return 1;
    }
    if (d1.data.rel.name < d2.data.rel.name) { 
      return -1;
    }
    if (d1.data.rel.name > d2.data.rel.name) {
      return 1;
    }
    if (d1.data.obj.name < d2.data.obj.name) { 
      return -1;
    }
    if (d1.data.obj.name > d2.data.obj.name) {
      return 1;
    }
    return 0;
  }

  load( data ) {
    var curr_sbj, curr_rel,
      stripe_toggle;

    this._$root.empty();
    this._data = data.sort(this.compareData);

    stripe_toggle = false;
    for (var i=0; i < this._data.length; i++) {
      var obj, rel_id, rel_data, $row;
      
      obj = this._data[i];
      rel_id = obj.id;
      rel_data = obj.data;
      if (curr_sbj !== rel_data.sbj.id) {
        stripe_toggle = !stripe_toggle;
      }
      $row = this.makeRow(rel_data, rel_id, stripe_toggle,
        (rel_data.sbj.id===curr_sbj), (rel_data.rel.id===curr_rel));
      this._$root.append($row);
      curr_sbj = rel_data.sbj.id;
      curr_rel = rel_data.rel.id;
    }
  }

  makeRow( data, relId, rowStripe, sbjIsRepeat, relIsRepeat ) {
    var
      $row, $td_sbj, $td_rel, $td_obj,
      $td_del, $button, $span;
    $row = $('<tr/>', {'class': 'relationship-row'});
    $row.addClass( rowStripe ? 'rel-row-1' : 'rel-row-2');
    $td_sbj = $('<td/>').append(
      $('<span/>', { 'text': data.sbj.name,
        'class' : sbjIsRepeat ? 'repeated' : '' }) );
    $td_rel = $('<td/>').append(
      $('<span/>', { 'text': data.rel.name,
        'class' : (sbjIsRepeat && relIsRepeat) ? 'repeated' : '' }) );
    $td_obj = $('<td/>', { 'text': data.obj.name });
    $td_del = $('<td/>');
    $button = $('<button/>',
      { 'class': 'btn btn-danger del-rel repeated',
        'data-rel-id': relId });
    $span = $('<span/>', {'class': 'fas fa-times-circle'});
    $row.append($td_sbj).append($td_rel).append($td_obj).append(
      $td_del.append($button.append($span)));
    return $row;
  }

  getRow( idx ) {
    return this._data[idx];
  }

  handleEvent(event) {
    let target = event.target;
    
    switch(event.type) {
      case "mouseover":
        var row = $(target).closest('.relationship-row');
        row.find('.repeated').addClass('show-repeated');
        return;
      case "mouseout":
        var row = $(target).closest('.relationship-row');
        row.find('.repeated').removeClass('show-repeated');
        return;
      default:
        return;
    }
  }
}