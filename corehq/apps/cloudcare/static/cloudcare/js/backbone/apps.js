
var getLocalizedString = function (property, language) {
    return this.get(property)[language] || "?";
};


var getFormUrl = function(urlRoot, appId, moduleId, formId) {
    // TODO: make this cleaner
    return urlRoot + "view/" + appId + "/modules-" + moduleId + "/forms-" + formId + "/";
};
               
var AppNavigation = Backbone.Router.extend({
    
    initialize: function() {
        // _.bindAll(this); 
    },
    
    routes: {
        "view/:app":   "app",    // #view/appid
        "":            "clear"
    },
    
});

var AppSummary = Backbone.Model.extend({
    idAttribute: "_id"
});

var AppSummaryView = Backbone.View.extend({
    tagName: 'li', 
    initialize: function() {
        _.bindAll(this, 'render', 'select');
    },
    events: {
        "click": "select"
    },
    select: function () {
        this.trigger("selected");
    }, 
    render: function() {
        $("<a />").text(this.model.get("name")).appendTo($(this.el));
        return this; 
    }
});

var AppList = Backbone.Collection.extend({
    model: AppSummary,
});

var AppListView = Backbone.View.extend({
    el: $('#app-list'), 
    
    initialize: function(){
        _.bindAll(this, 'render', 'appendItem');
        this.appList = new AppList();
        this.appList.reset(this.options.apps);
        this.render();
    },
    
    render: function () {
        var self = this;
        var ul = $("<ul />").addClass("nav nav-list").appendTo($(this.el));
        $("<li />").addClass("nav-header").text("Apps").appendTo(ul);
        _(this.appList.models).each(function(item){ 
            self.appendItem(item);
        });
    },
    appendItem: function (item) {
        var self = this;
        var appView = new AppSummaryView({
            model: item
        });
        appView.on("selected", function () {
            self.trigger("app:selected", this);
        });
        $('ul', this.el).append(appView.render().el);
    }
});

var App = Backbone.Model.extend({
    idAttribute: "_id",
    initialize: function () {
        _.bindAll(this, "updateModules");
        var self = this;
        this.updateModules();
        this.on("change", function () {
            this.updateModules();
        });
    },
    urlRoot: function () {
        return this.get("urlRoot");
    },
    updateModules: function () {
        var self = this;
        if (this.get("modules")) {
            var index = 0;
            this.modules = _(this.get("modules")).map(function (module) {
                var ret = new Module(module);
                ret.set("app_id", self.id);
                ret.set("index", index);
                index++;
                return ret;
            });
            this.trigger("modules-changed");
        } 
    }
});
var Form = Backbone.Model.extend({
    initialize: function () {
        _.bindAll(this, 'getLocalized');
    },
    getLocalized: getLocalizedString
});

var Module = Backbone.Model.extend({
    initialize: function () {
        _.bindAll(this, 'getLocalized', 'updateForms', 'getDetail');
        this.updateForms();
        this.on("change", function () {
            this.updateForms();
        });
    },
    getLocalized: getLocalizedString,
    
    getDetail: function (type) {
        return _(this.get("details")).find(function (elem) {
            return elem.type === type;
        });
    },
    
    updateForms: function () {
        var self = this;
        if (this.get("forms")) {
            var index = 0;
            this.forms = _(this.get("forms")).map(function (form) {
                var ret = new Form(form);
                ret.set("app_id", self.get("app_id"));
                ret.set("module_index", self.get("index"));
                ret.set("index", index);
                index++;
                return ret;
            });
            this.trigger("forms-changed");
        } 
    } 
});

var ModuleView = Backbone.View.extend({
    tagName: 'li', 
    initialize: function() {
        _.bindAll(this, 'render', 'select');
    },
    events: {
        "click": "select"
    },
    select: function () {
        this.trigger("selected");
    }, 
    render: function() {
        $("<a />").text(this.model.getLocalized("name", this.options.language)).appendTo($(this.el));
        return this;
    }
});

var ModuleList = Backbone.Collection.extend({
    model: Module
});

var ModuleListView = Backbone.View.extend({
    el: $('#module-list'), 
    initialize: function () {
        _.bindAll(this, 'render', 'appendItem', 'updateModules');
        var self = this;
        this.moduleList = new ModuleList([], {
            language: this.options.language
        });
        this.moduleList.on("reset", function () {
            self.updateModules();
        });
        this.render();
    },
    render: function () {
        this.updateModules();
    },
    updateModules: function () {
        // clear
        $(this.el).html("");
        var self = this;
        var ul = $("<ul />").addClass("nav nav-list").appendTo($(this.el));
        $("<li />").addClass("nav-header").text("Modules").appendTo(ul);
        _(this.moduleList.models).each(function(item){ 
            self.appendItem(item);
        });
    },
    appendItem: function (item) {
        var self = this;
        var moduleView = new ModuleView({
            model: item,
            language: this.options.language
            
        });
        moduleView.on("selected", function () {
            self.trigger("module:selected", this);
        });
        $('ul', this.el).append(moduleView.render().el);
    }
});

var ModuleDetailsView = Backbone.View.extend({
    el: $('#form-list'), 
    initialize: function () {
        _.bindAll(this, 'render');
    },
    render: function () {
        var self = this;
        $(this.el).html("");
        var formUl = $("<ul />").addClass("nav nav-list").appendTo($(this.el));
        $("<li />").addClass("nav-header").text("Forms").appendTo(formUl);
        _(this.model.forms).each(function (form) {
            var formLi = $("<li />");
            var formLink = $("<a />").text(form.getLocalized("name", self.options.language)).appendTo(formLi);
            formLi.appendTo(formUl);
            formLink.click(function () {
                form.trigger("selected");
            });
            form.on("selected", function () {
                self.trigger("form:selected", this);
            });
        });
        return this;
    }    
});
var AppView = Backbone.View.extend({
    el: $('#app-list'), 
    
    initialize: function(){
        _.bindAll(this, 'render', 'showModule');
        var self = this;
        this.render();
        this.moduleListView = new ModuleListView({
            language: this.options.language
        });
        this.moduleDetailsView = new ModuleDetailsView({
            language: this.options.language
        });
        
        this.moduleDetailsView.on("form:selected", function (form) {
            var modView = this;
            if (form.get("requires") === "none") {
                // go play the form
                var url = getFormUrl(self.options.urlRoot, form.get("app_id"), 
                                     form.get("module_index"), form.get("index"));
                window.location.href = url;
                
            } else if (form.get("requires") === "case") {
                var listDetails = modView.model.getDetail("case_short");
                var summaryDetails = modView.model.getDetail("case_long");
                // clear anything existing
                if (modView.caseView) {
                    $(modView.caseView.el).html("");
                }
                modView.caseView = new CaseMainView({                    el: $("#cases"),
                    listDetails: listDetails,
                    summaryDetails: summaryDetails,
                    language: modView.options.language,
                    // TODO: clean up how filtering works
                    caseUrl: self.options.caseUrlRoot + "?properties/case_type=" + modView.model.get("case_type")
                });
                modView.caseView.listView.on("case:selected", function (caseView) {
                    if (!modView.enterForm) {
                        modView.enterForm = $("<a />").text("Enter Form").addClass("btn btn-primary").appendTo(
                            $(modView.caseView.detailsView.el));
                    }
                    modView.enterForm.click(function () {
                        var url = getFormUrl(self.options.urlRoot, form.get("app_id"), form.get("module_index"), form.get("index"));
                        window.location.href = url + "?case_id=" + caseView.model.id;
                    });
                });
                modView.caseView.listView.on("case:deselected", function (caseView) {
                    if (modView.enterForm) {
                        modView.enterForm.detach();
                        modView.enterForm = null;                      
                    }
                });
            }
        });
         
        this.moduleListView.on("module:selected", function (moduleView) {
            self.showModule(moduleView.model);
            
        });
        this.model.on("modules-changed", function () {
            self.moduleListView.moduleList.reset(this.modules);
        });
    },
    showModule: function (module) {
        this.moduleDetailsView.model = module;
        this.moduleDetailsView.render();
    },
    render: function () {
        var self = this;
    }
});

var AppMainView = Backbone.View.extend({
    el: $('#app-main'),
     
    initialize: function () {
        _.bindAll(this, 'render', 'selectApp'); 
        var self = this;
        this.router = new AppNavigation();
        this.router.on("route:app", function (appId) {
            // TODO
            self.selectApp(appId);
        });
        this.router.on("route:clear", function () {
            // TODO
        });
        this.appListView = new AppListView({
            apps: this.options.apps,
            language: this.options.language
        });
        this.appListView.on("app:selected", function (app) {
            self.selectApp(app.model.id);
        });
    },
    
    selectApp: function (appId) {
        this.router.navigate("view/" + appId);
        this.app = new App({
            _id: appId,
        });
        this.app.set("urlRoot", this.options.appUrlRoot);
        this.app.fetch();
        this.appView = new AppView({
            model: this.app,
            language: this.options.language,
            caseUrlRoot: this.options.caseUrlRoot,
            urlRoot: this.options.urlRoot
        });
    },
    
    render: function () {
        return this;
    }
});
