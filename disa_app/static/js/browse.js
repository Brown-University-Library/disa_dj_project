//let darkOverlay = document.getElementById("dark-overlay");
//darkOverlay.style.display = 'none';

let dragDialog = null;
let dragOffsetX = 0;
let dragOffsetY = 0;
document.addEventListener("mouseup", () => {
    if (dragDialog != null) {
        dragDialog = null;
        dragOffsetX = 0;
        dragOffsetY = 0;
    }
}, false);
document.addEventListener("mousemove", (evt) => {
    if (dragDialog != null) {
        dragDialog.style.top = Math.max(evt.screenY - dragOffsetY, 0) + "px";
        dragDialog.style.left = Math.max(evt.screenX - dragOffsetX, 0) + "px";
    }
}, false);

function showDialog(someElement) {
    let titleBar = create("div", {class: "dialog-titlebar"}, [
        create("button", "X", {class: "close-button", onclick:
             "document.body.removeChild(this.parentNode.parentNode)"})
    ]);
    titleBar.addEventListener("mousedown", (evt) => {
        dragDialog = evt.target.parentNode;
        dragOffsetX = evt.screenX - Number(evt.target.parentNode.style.left.replace("px", ""));
        dragOffsetY = evt.screenY - Number(evt.target.parentNode.style.top.replace("px", ""));
        document.body.removeChild(evt.target.parentNode);
        document.body.appendChild(evt.target.parentNode);
    }, false);
    let dialogWindow = create("div", {class: "dialog-window"}, [
        titleBar,
        create("div", {class: "dialog-content"}, [
            someElement
        ])
    ]);
    document.body.appendChild(dialogWindow);
    dialogWindow.style.top = ((document.documentElement.clientHeight - dialogWindow.clientHeight) / 2) + window.pageYOffset + "px";
    dialogWindow.style.left = ((document.documentElement.clientWidth - dialogWindow.clientWidth) / 2) + window.pageXOffset + "px";
//  document.getElementById("dialog-content").innerHTML
//      = someElement.innerHTML;
//  darkOverlay.style.display = 'flex';
}
// function hideDialog() {
//  darkOverlay.style.display = 'none';
//}

var raw_data;
function exists(x) {
    if (x == null ||
        typeof x == 'undefined' ||
        x == ""
    ) {
        return false;
    }
    return true;
}
function formatNames(names) {
    let formattedNames = "";
    for (let i = 0; i < names.length; i++) {
        if (i > 0) {formattedNames += ", ";}
        if (exists(names[i].firstName)) {
            formattedNames += names[i].firstName;
            if (exists(names[i].lastName)) {
                formattedNames += " ";
            }
        }
        if (exists(names[i].lastName)) {
            formattedNames += names[i].lastName;
        }
    }
    return formattedNames;
}
function formatTribe(tribe) {
    if (tribe == "Unspecified") {
        return "";
    }
    return tribe;
}

function formatDate(someDate) {
    let year = "";
    let month = "";
    let day = "";
    if (exists(someDate.year)) { year = someDate.year; }
    if (exists(someDate.month)) { month = someDate.month; }
    if (exists(someDate.day)) { day = someDate.day; }
    if (!(exists(year) || exists(month) || exists(day))) {
        return "";
    }
    if (String(month).length == 1) { month = "0" + month; }
    if (String(day).length == 1) { day = "0" + day; }
    return [year, month, day].join("-");
}

var formatRoleData = function (roleName, roleObjs) {
    if (roleObjs.length !== 0) {
        var role_str;
        var objs_str = roleObjs.join(', ');
        var of_list = ['child', 'parent', 'manservant',
            'maidservant', 'manslave', 'servant', 'owner',
            'pieza', 'father', 'mother'];
        if (of_list.indexOf(roleName) > -1 ){
            role_str = roleName + ' of ';
        }
        else if (roleName === 'enslaved') {
            role_str = 'owned by ';
        } else if (roleName === 'indentured servant') {
            role_str = 'indentured to ';
        } else if (roleName === 'has_mother') {
            role_str = 'child of ';
        } else if (roleName === 'has_father') {
            role_str = 'child of ';
        } else {
            role_str = roleName + ": ";
        }
        return role_str + objs_str;
    } else {
        return roleName;
    }
}

var iterateRoles = function (rolesData) {
    var lis = [];
    for (var role in rolesData) {
        lis.push(create(
            "li", formatRoleData(role, rolesData[role]),
            {style: "list-style: none;"}
        ));
    }
    return lis;
}

var iterateDocumentInfo = function (docArray) {
 out = [];
 for (var cite in docArray) {
    var doc = docArray[cite][0]
    out.push(create("h3", cite, {style: "margin-bottom: 3px;"}));
    out.push(create("ul",
            iterateRoles(doc.roles).concat([
            create("li", [
            create("span", doc.locations.join(', ')),
            create("span", formatDate(doc.date),
                {style:"margin-left: 20px;"})
            ],
            {style: "list-style: none;"})
        ]),
        {style: "margin-top: 0px;"}
    ));
    out.push(create("p", doc.comments ) );
 }
 return out;
}

function expandInformation(index) {
    var person = raw_data[index];
    showDialog(create("div", [
    create("h2", (person.first_name + " " + person.last_name).trim(),
            {style: "margin-top: 0px;"})
    ].concat(iterateDocumentInfo(person.documents))));
}

let imageFormatter = function(row, cell, value, columnDef, dataContext){
    return "<img src='" + value + "'/>";
};


var info_image_url = document.getElementById( "info_image_url" ).value;
console.log( "info_image_url..." + info_image_url );
let indexFormatter = function(row, cell, value, columnDef, dataContext) {
    return ("<img src=" + info_image_url + " alt='VALUE' " +
            "onclick='expandInformation(VALUE)' />").replace(/VALUE/g, value);
}

var dataView;
var grid;
var data = [
    {pic: "", id: "Johnny", name: "Johnny Saunders",
     documents: "Boston Times, Issues 54", events: "Baptism"},
    {pic: "",id: "Sammy", name: "Sammy Fletcher, Sammy Indigo",
     documents: "Old Time News", events: "Escape"},
    {pic: "",id: "Ronald", name: "Ronald Von Harrow", documents: "",
     events: "Marriage"},
];

var options = {
    enableCellNavigation: true,
    enableColumnSort: true,
    multiColumnSort: false,
    showHeaderRow: true,
    headerRowHeight: 30,
    rowHeight: 40,
    explicitInitialization: true,
    enableTextSelectionOnCells: true,
};
var columns = [
 {id: "persNumber",
  name: "",
  field: "persNumber",
  width: 20,
  formatter: indexFormatter,
  sortable: false},
 {id: "name",
  name: "Name",
  field: "name",
  width: 240,
  sortable: true},
 {id: "date",
  name: "Earliest record",
  field: "date",
  width: 135,
  sortable: true},
 {id: "sex",
  name: "Gender",
  field: "sex",
  width: 100,
  sortable: true},
 {id: "age",
  name: "Age",
  field: "age",
  width: 100,
  sortable: true},
 {id: "race",
  name: "Race",
  field: "race",
  width: 180,
  sortable: true},
 {id: "tribe",
  name: "Tribe / Nation",
  field: "tribe",
  width: 180,
  sortable: true},
 {id: "origin",
  name: "Origin",
  field: "origin",
  width: 180,
  sortable: true},
 {id: "vocation",
  name: "Vocation",
  field: "vocation",
  width: 180,
  sortable: true},
 {id: "owner",
  name: "Owner",
  field: "owner",
  width: 300,
  sortable: true},
 {id: "mother",
  name: "Mother",
  field: "mother",
  width: 200,
  sortable: true},
 {id: "father",
  name: "Father",
  field: "father",
  width: 200,
  sortable: true},
 {id: "transcription",
  name: "Notes",
  field: "transcription",
  width: 300,
  sortable: true}
];
var columnFilters = {};

function filter(item) {
    for (var columnId in columnFilters) {
        if (columnId !== undefined
            && columnFilters[columnId] !== ""
        ) {
            var c = grid.getColumns()[
                grid.getColumnIndex(columnId)
            ];
            if (!item[c.field].toLowerCase().includes(
                columnFilters[columnId].toLowerCase())
            ) { return false; }
        }
    }
    return true;
}

var dnrmlzd_jsn_url = document.getElementById( "denormalized_json_url" ).value;
console.log( "dnrmlzd_jsn_url..." + dnrmlzd_jsn_url );

// $.get("static/data/denormalized.json", (some_data, status) => {
$.get( dnrmlzd_jsn_url, (some_data, status) => {
    raw_data = some_data;
    data = [];
    console.log( "just got data" );
    console.log( "data.length..." + raw_data.length );
     for (let i = 0; i < raw_data.length; i++) {
         var rec = raw_data[i];
         // console.log( "rec, " + rec );
         data.push({
             pic: "",
             persNumber: String(i),
             id: rec.id,
             date: formatDate(rec.date),
             age: rec.description.age,
             name: (rec.first_name + " " + rec.last_name).trim(),
             race: rec.description.race,
             origin: rec.description.origin,
             tribe: formatTribe(rec.description.tribe),
             sex: rec.description.sex,
             vocation: rec.description.vocation,
             owner: rec.owner,
             spouse: rec.spouse,
             mother: rec.has_mother,
             father: rec.has_father,
             transcription: rec.comments
         });
     }
    dataView = new Slick.Data.DataView();
    grid = new Slick.Grid("#myGrid", dataView, columns, options);
    dataView.onRowCountChanged.subscribe(function (e, args) {
        grid.updateRowCount();
        grid.render();
    });
    dataView.onRowsChanged.subscribe(function (e, args) {
        grid.invalidateRows(args.rows);
        grid.render();
    });
    $(grid.getHeaderRow()).on("change keyup", ":input", function (e) {
        var columnId = $(this).data("columnId");
        if (columnId != null) {
            columnFilters[columnId] = $.trim($(this).val());
            dataView.refresh();
        }
    });
    grid.onHeaderRowCellRendered.subscribe(function(e, args) {
        $(args.node).empty();
        $("<input type='text'>")
            .data("columnId", args.column.id)
            .val(columnFilters[args.column.id])
            .appendTo(args.node);
    });
    grid.onSort.subscribe(function(e, args) {
        console.log(args);
        var comparer = function(a, b) {
            return (a[args.sortCol.field] >
                    b[args.sortCol.field]) ? 1 : -1;
        }
        dataView.beginUpdate();
        dataView.sort(comparer, args.sortAsc);
        dataView.endUpdate();
    });
    grid.init();
    dataView.beginUpdate();
    dataView.setItems(data);
    dataView.setFilter(filter);
    dataView.endUpdate();
});
