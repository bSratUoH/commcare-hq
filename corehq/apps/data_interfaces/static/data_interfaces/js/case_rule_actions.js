hqDefine("data_interfaces/js/case_rule_actions", [
    'jquery',
    'knockout',
    'hqwebapp/js/initial_page_data',
], function (
    $,
    ko,
    initialPageData
) {
    var CaseRuleActions = function (initial) {
        'use strict';
        var self = this;

        self.actions = ko.observableArray();

        self.get_ko_template_id = function (obj) {
            if (obj instanceof CloseCaseDefinition) {
                return 'close-case-action';
            } else if (obj instanceof UpdatePropertyDefinition) {
                return 'update-case-property-action';
            } else if (obj instanceof CustomActionDefinition) {
                return 'custom-action';
            }
        };

        self.get_js_class = function (templateId) {
            if (templateId === 'close-case-action') {
                return CloseCaseDefinition;
            } else if (templateId === 'update-case-property-action') {
                return UpdatePropertyDefinition;
            } else if (templateId === 'custom-action') {
                return CustomActionDefinition;
            }
        };

        self.close_case = ko.computed(function () {
            var result = 'false';
            $.each(self.actions(), function (index, value) {
                if (value instanceof CloseCaseDefinition) {
                    result = 'true';
                }
            });
            return result;
        });

        self.properties_to_update = ko.computed(function () {
            var result = [];
            $.each(self.actions(), function (index, value) {
                if (value instanceof UpdatePropertyDefinition) {
                    result.push({
                        name: value.name() || '',
                        value_type: value.value_type() || '',
                        value: value.value() || '',
                    });
                }
            });
            return JSON.stringify(result);
        });

        self.custom_action_definitions = ko.computed(function () {
            var result = [];
            $.each(self.actions(), function (index, value) {
                if (value instanceof CustomActionDefinition) {
                    result.push({
                        name: value.name() || '',
                    });
                }
            });
            return JSON.stringify(result);
        });

        self.action_already_added = function (js_class) {
            for (var i = 0; i < self.actions().length; i++) {
                if (self.actions()[i] instanceof js_class) {
                    return true;
                }
            }

            return false;
        };

        self.add_action = function (templateId) {
            if (templateId === 'select-one') {
                return;
            }
            var js_class = self.get_js_class(templateId);

            if (js_class === CloseCaseDefinition && self.action_already_added(CloseCaseDefinition)) {
                return;
            }

            self.actions.push(new js_class());
        };

        self.remove_action = function () {
            self.actions.remove(this);
        };

        self.load_initial = function () {
            if (initial.close_case === 'true') {
                var obj = new CloseCaseDefinition();
                self.actions.push(obj);
            }

            $.each(initial.properties_to_update, function (index, value) {
                var obj = new UpdatePropertyDefinition();
                obj.name(value.name);
                obj.value_type(value.value_type);
                obj.value(value.value);
                self.actions.push(obj);
            });

            $.each(initial.custom_action_definitions, function (index, value) {
                var obj = new CustomActionDefinition();
                obj.name(value.name);
                self.actions.push(obj);
            });
        };
    };

    var CloseCaseDefinition = function () {
        'use strict';
        var self = this;

        // This model matches up with the Django UpdateCaseDefinition.close_case model attribute
    };

    var UpdatePropertyDefinition = function () {
        'use strict';
        var self = this;

        // This model matches up with one instance in the Django UpdateCaseDefinition.properties_to_update model attribute
        self.name = ko.observable();
        self.value_type = ko.observable();
        self.value = ko.observable();
    };

    var CustomActionDefinition = function () {
        'use strict';
        var self = this;

        // This model matches the Django model with the same name
        self.name = ko.observable();
    };

    var actions_model = null;

    $(function () {
        actions_model = new CaseRuleActions(initialPageData.get('actions_initial'));
        $('#rule-actions').koApplyBindings(actions_model);
        actions_model.load_initial();
    });

    return {
        get_actions_model: function () {return actions_model;},
    };

});
