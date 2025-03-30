odoo.define('ctx_aged_receivable_salesperson.account_report_generic', function (require) {
'use strict';

    var core = require('web.core');
    var RelationalFields = require('web.relational_fields');
    var Context = require('web.Context');
    var StandaloneFieldManagerMixin = require('web.StandaloneFieldManagerMixin');
    var { WarningDialog } = require("@web/legacy/js/_deprecated/crash_manager_warning_dialog");
    var Widget = require('web.Widget');
    var accountReports = require('account_reports.account_report');
    var QWeb = core.qweb;
    var _t = core._t;


    accountReports.accountReportsWidget.include({
        custom_events: _.extend({}, accountReports.accountReportsWidget.prototype.custom_events, {
            'salesperson_filter_changed': function (ev) {
                var self = this;
                self.report_options.salesperson_ids = ev.data.salesperson_ids;
                return self.reload().then(function () {
                    self.$searchview_buttons.find('.account_salesperson_filter').click();
                });
            },
        }),

        render_searchview_buttons: function () {
            var self = this;

            self._super();
            if (this.report_options.salesperson) {
                if (!this.salesperson_m2m_filter) {
                    var fields = {};
                    if ('salesperson_ids' in this.report_options) {
                        fields['salesperson_ids'] = {
                            label: _t('Persons'),
                            modelName: 'res.users',
                            value: this.report_options.salesperson_ids.map(Number),
                        };
                    }
                    if (!_.isEmpty(fields)) {
                        this.salesperson_m2m_filter = new accountReports.M2MFilters(this, fields, 'salesperson_filter_changed');
                        this.salesperson_m2m_filter.appendTo(this.$searchview_buttons.find('.js_account_salesperson_m2m'));
                    }
                } else {
                    this.$searchview_buttons.find('.js_account_salesperson_m2m').append(this.salesperson_m2m_filter.$el);
                }
            }

        },

    });

});