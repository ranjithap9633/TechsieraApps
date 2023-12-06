odoo.define("ts_event_management_system.custom_info_widget", function (require) {
    "use strict";

    var FieldWidget = require("web.FieldWidget");

    var CustomInfoWidget = FieldWidget.extend({
        template: "ts_event_management_system.CustomInfoWidget",
        events: _.extend({}, FieldWidget.prototype.events, {
            "click .o-attendance-info": "_onInfoClick",
        }),

        start: function () {
            this._render();
            return this._super();
        },

        //        _onInfoClick: function (ev) {
        //        },
    });

    return CustomInfoWidget;
});
