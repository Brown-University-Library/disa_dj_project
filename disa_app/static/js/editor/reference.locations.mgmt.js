class LocationMgmt {

  constructor(referenceId, source, $elem) {
    var $tbody = $('<tbody/>');
    var $tfoot = $('<tfoot/>');
    $elem.append($tbody).append($tfoot);

    this._reference = referenceId;
    this._source = source;
    this._$root = $elem;
    this._$body = $tbody;
    this._$foot = $tfoot;
    this._loc_inputs = [];
    this._data = [];
    this._loc_types = {};
    this._loc_type_map = {};
    this._$root[0].addEventListener('click', this);
    this._$root[0].addEventListener('change', this);
  }

  load() {
    $.widget( "custom.catcomplete", $.ui.autocomplete, {
      _create: function() {
        this._super();
        this.widget().menu( "option", "items", "> :not(.ui-autocomplete-category)" );
      },
      _renderMenu: function( ul, items ) {
        var that = this,
          currentCategory = "";
        $.each( items, function( index, item ) {
          var li;
          if ( item.category != currentCategory ) {
            ul.append( "<li class='ui-autocomplete-category'>" + item.category + "</li>" );
            currentCategory = item.category;
          }
          li = that._renderItemData( ul, item );
          if ( item.category ) {
            li.attr( "aria-label", item.category + " : " + item.label );
          }
        });
      }
    });
    this._source.getLocations(this._reference);
  }

  loadData(data) {
    this._data = data.reference_locations;
    this._loc_type_map = data.locations_by_type;
    this._loc_types = data.location_types;
    this.populate();
  }

  swapIndex(first, second) {
    var front, back, block;
    if ( (first > second) || (second == 0) || (second + 1 > this._data.length) ) {
      return;
    }
    front = this._data.slice(0, first);
    back = this._data.slice(second + 1, this._data.length);
    block = [ this._data[second], this._data[first] ];
    this._data = front.concat(block).concat(back);
    this.populate();
  }

  populate() {
    var $row_add, $td_add, $btn_add;

    this._loc_inputs = [];
    this._$body.empty();
    this._$foot.empty();

    for (var i=0; i < this._data.length; i++) {
      var obj,
        loc_id, loc_name, loc_type,
        $row;
      
      obj = this._data[i];
      loc_id = obj.loc_id;
      loc_name = obj.name;
      loc_type = obj.loc_type_id;

      $row = this.makeRow(loc_id, loc_name, i, loc_type);
      this._$body.append($row);
    }

    $row_add = $('<tr/>');
    $td_add = $('<td/>');
    $btn_add = $('<button/>',
      { 'class': 'btn btn-primary add-loc',
        'text': 'Additional location' });
    $row_add.append($td_add.append($btn_add)).append($('<td/>'))
      .append($('<td/>')).append($('<td/>')).append($('<td/>'));
    this._$foot.append($row_add);
  }

  makeRow( locId, locName, locIdx, locTypeId ) {
    var
      $row, 
      $td_name, $td_type, $td_del, $td_up, $td_down,
      $input_name, $select_type,
      $button_del, $button_up, $button_down,
      $span_del, $span_up, $span_down;

    $row = $('<tr/>',
        {'class': 'location-row',
         'data-loc-id': locId,
         'data-loc-idx': locIdx });
    $td_name = $('<td/>');
    $input_name = $('<input/>',
      { 'class': 'form-control location-name',
        'type': 'text',
        'value': locName });
    $td_type = $('<td/>');
    $select_type = $('<select/>',
      { 'class': 'select-loc-type',
        'data-loc-idx': locIdx });
    $td_del = $('<td/>');
    $td_up = $('<td/>');
    $button_up = $('<button/>',
      { 'class': (locIdx == 0) ? 'btn btn-light loc-up' : 'btn btn-light move-loc loc-up',
        'data-loc-idx': locIdx });
    $span_up = $('<span/>',
      { 'class': (locIdx == 0) ? 'fas fa-ban no-loc' : 'fa fa-arrow-up' });
    $td_down = $('<td/>');
    $button_down = $('<button/>',
      { 'class': (locIdx == this._data.length - 1) ? 'btn btn-light loc-down' : 'btn btn-light move-loc loc-down',
        'data-loc-idx': locIdx });
    $span_down = $('<span/>',
      { 'class': (locIdx == this._data.length - 1) ? 'fas fa-ban no-loc' : 'fa fa-arrow-down' });
    $button_del = $('<button/>',
      { 'class': 'btn btn-danger del-loc',
        'data-loc-idx': locIdx });
    $span_del = $('<span/>', {'class': 'fas fa-times-circle'});

    $row.append($td_name.append($input_name))
        .append($td_type.append($select_type))
        .append($td_up.append($button_up.append($span_up)))
        .append($td_down.append($button_down.append($span_down)))
        .append($td_del.append($button_del.append($span_del)));

    this.addLocationTypeOptions($select_type, locTypeId);
    this.addAutoComplete($input_name, locTypeId);
    this._loc_inputs.push($input_name);
    return $row;
  }

  addRow() {
    var new_loc = { id: 'new', name: '', loc_id: '', loc_type_id: ''};
    this._data.push(new_loc);
    this.populate();
  }

  deleteLocation(locIdx) {
    if (this._data.length == 1) {
      var new_loc = { id: 'new', name: ''};
      this._data = [ new_loc ];
    }
    else {
      this._data.splice(locIdx, 1);
    }
    this.populate();
  }

  addLocationTypeOptions($select, existingTypeId) {
    for (var type_id in this._loc_types) {
      var opt, $opt_elem;
      opt = this._loc_types[type_id];
      $opt_elem = $("<option/>",
        { 'value': opt.id ,
          'text': opt.name });
        $select.append($opt_elem);
    }
    $select.val(existingTypeId);
  }

  filterLocationTypes(locType) {
    var loc_vals = this._loc_type_map[locType];
  }

  addAutoComplete($input, locType) {
    var loc_vals = this._loc_type_map[locType];
    $input.catcomplete({
        source: loc_vals,
        minLength: 2,
        delay: 10,
        autoFocus: true,
        response: function (event, ui) {
            if (ui.content.length == 0) {
                ui.content.push({
                    label: $(this).val(),
                    value: $(this).val(),
                    id: -1
                });
            }
        }
    });
  }

  handleEvent(event) {
    let target = event.target;
    switch(event.type) {
      case "click":
        if (target.classList.contains('del-loc')) {
          var loc_idx = parseInt(target.getAttribute('data-loc-idx'));
          this.deleteLocation(loc_idx);
        }
        else if (target.classList.contains('move-loc')) {
          var loc_idx = parseInt(target.getAttribute('data-loc-idx'));
          if (target.classList.contains('loc-up')) {
            this.swapIndex(loc_idx - 1, loc_idx);
          } else if (target.classList.contains('loc-down')) {
            this.swapIndex(loc_idx, loc_idx + 1);
          }
        }
        else if (target.classList.contains('add-loc')) {
          this.addRow();
        }
        return;
      case "change":
        if (target.classList.contains('select-loc-type')) {
          var loc_idx = parseInt(target.getAttribute('data-loc-idx'));
          var type_val = target.value;
          this.setLocationType(loc_idx, type_val);
        }
      default:
        return;
    }
  }
}