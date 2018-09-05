/* globals requirejs */
requirejs.config({
    baseUrl: '/static/',
    paths: {
        "jquery": "jquery/dist/jquery.min",
        "underscore": "underscore/underscore",
        "bootstrap": "bootstrap/dist/js/bootstrap.min",
        "knockout": "knockout/dist/knockout.debug",
        "ko.mapping": "hqwebapp/js/lib/knockout_plugins/knockout_mapping.ko.min",
        "datatables": "datatables/media/js/jquery.dataTables.min",
        "datatables.fixedColumns": "datatables-fixedcolumns/js/dataTables.fixedColumns",
        "datatables.bootstrap": "datatables-bootstrap3/BS3/assets/js/datatables",
    },
    shim: {
        "ace-builds/src-min-noconflict/ace": { exports: "ace" },
        "accounting/js/lib/stripe": { exports: 'Stripe' },
        "bootstrap": { deps: ['jquery'] },
        "ko.mapping": { deps: ['knockout'] },
        "hqwebapp/js/hq.helpers": { deps: ['jquery', 'bootstrap', 'knockout', 'underscore'] },
        "datatables.bootstrap": { deps: ['datatables'] },
        "jquery.rmi/jquery.rmi": {
            deps: ['jquery', 'knockout', 'underscore'],
            exports: 'RMI',
        },
        "nvd3/nv.d3.min":{deps:['d3/d3.min']},
    },
    map: {
        "datatables.fixedColumns": {
            "datatables.net": "datatables",
        },
    },

    // This is really build config, but it's easier to define a js function here than in requirejs.yaml
    onBuildRead: function (moduleName, path, contents) {
        return contents.replace(/hqDefine/g, 'define');
    },
});
