class DISASource {

  constructor(baseURL) {
    this._base = baseURL;
    this._apps = {};
    this._base = base_url_segment;  // `base_url_segment` prepared in '/record/relationships/<recId>' and passed to base.html <script/> header-element.
    console.log( "in DISASource constructor(); this._base, ```" + this._base + "```" );
  }

  registerApp( name, app ) {
    this._apps[name] = app;
  }

  getREST( endpoint, callback ) {
    console.log( "in getREST(); endpoint, ```" + endpoint + "```" );
    $.ajax({
      type: "GET",
      dataType: "json",
      url: endpoint,
      success: function( data ) {
        callback( data );
      }
    });
  }

  postREST( endpoint, payload, callback ) {
    $.ajax({
      type: "POST",
      data: JSON.stringify(payload),
      contentType: "application/json",
      dataType: "json",
      url: endpoint,
      success: function( data ) {
        callback( data );
      }
    });
  }

  delREST( endpoint, payload, callback ) {
    $.ajax({
      type: "DELETE",
      data: JSON.stringify(payload),
      contentType: "application/json",
      dataType: "json",
      url: endpoint,
      success: function( data ) {
        callback( data );
      }
    });
  }

  getRelationships(sectionId) {
    console.log( "in getRelationships(); this._base, ```" + this._base + "```" );
    let endpoint = this._base + `/data/sections/${sectionId}/relationships/`;
    let callback = this._apps['rel-mgmt'].setUp;
    this.getREST(endpoint, callback);
  }

  addRelationship(obj) {
    let endpoint = this._base + `/data/relationships/`;
    let callback = this._apps['rel-mgmt'].setUp;
    this.postREST(endpoint, obj, callback);
  }

  deleteRelationship(sectionId, relId) {
    let endpoint = this._base + `/data/relationships/${relId}`;
    let callback = this._apps['rel-mgmt'].setUp;
    this.delREST(endpoint, { 'section': sectionId }, callback);
  }

  getLocations(sectionId) {
    var endpoint = this._base + `/data/locations/${sectionId}`;
    let callback = this._apps['loc-mgmt'].loadData
    this.getREST(endpoint, callback);
  }
}
