# -*- coding: utf-8 -*-
from couchdb.design import ViewDefinition
from openprocurement.api import design
from openprocurement.api.design import add_index_options

FIELDS = [
    'planID',
]
CHANGES_FIELDS = FIELDS + [
    'dateModified',
]


def add_design():
    for i, j in globals().items():
        if "_view" in i:
            setattr(design, i, j)


def add_design_db(db):
    """ add local views *_view to database
    :param db: database
    """
    views = [j for i, j in globals().items() if "_view" in i]
    ViewDefinition.sync_many(db, views, callback=add_index_options)


plans_all_view = ViewDefinition('plans', 'all', '''function(doc) {
    if(doc.doc_type == 'Plan') {
        emit(doc.planID, null);
    }
}''')

plans_by_dateModified_view = ViewDefinition('plans', 'by_dateModified', '''function(doc) {
    if(doc.doc_type == 'Plan') {
        var fields=%s, data={};
        for (var i in fields) {
            if (doc[fields[i]]) {
                data[fields[i]] = doc[fields[i]]
            }
        }
        emit(doc.dateModified, data);
    }
}''' % FIELDS)

plans_real_by_dateModified_view = ViewDefinition('plans', 'real_by_dateModified', '''function(doc) {
    if(doc.doc_type == 'Plan' && !doc.mode) {
        var fields=%s, data={};
        for (var i in fields) {
            if (doc[fields[i]]) {
                data[fields[i]] = doc[fields[i]]
            }
        }
        emit(doc.dateModified, data);
    }
}''' % FIELDS)

plans_test_by_dateModified_view = ViewDefinition('plans', 'test_by_dateModified', '''function(doc) {
    if(doc.doc_type == 'Plan' && doc.mode == 'test') {
        var fields=%s, data={};
        for (var i in fields) {
            if (doc[fields[i]]) {
                data[fields[i]] = doc[fields[i]]
            }
        }
        emit(doc.dateModified, data);
    }
}''' % FIELDS)

plans_by_local_seq_view = ViewDefinition('plans', 'by_local_seq', '''function(doc) {
    if(doc.doc_type == 'Plan') {
        var fields=%s, data={};
        for (var i in fields) {
            if (doc[fields[i]]) {
                data[fields[i]] = doc[fields[i]]
            }
        }
        emit(doc._local_seq, data);
    }
}''' % CHANGES_FIELDS)

plans_real_by_local_seq_view = ViewDefinition('plans', 'real_by_local_seq', '''function(doc) {
    if(doc.doc_type == 'Plan' && !doc.mode) {
        var fields=%s, data={};
        for (var i in fields) {
            if (doc[fields[i]]) {
                data[fields[i]] = doc[fields[i]]
            }
        }
        emit(doc._local_seq, data);
    }
}''' % CHANGES_FIELDS)

plans_test_by_local_seq_view = ViewDefinition('plans', 'test_by_local_seq', '''function(doc) {
    if(doc.doc_type == 'Plan' && doc.mode == 'test') {
        var fields=%s, data={};
        for (var i in fields) {
            if (doc[fields[i]]) {
                data[fields[i]] = doc[fields[i]]
            }
        }
        emit(doc._local_seq, data);
    }
}''' % CHANGES_FIELDS)

conflicts_view = ViewDefinition('conflicts', 'all', '''function(doc) {
    if (doc._conflicts) {
        emit(doc._rev, [doc._rev].concat(doc._conflicts));
    }
}''')
