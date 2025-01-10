odoo.define('bi_pos_stock.pos', function(require) {
	"use strict";

	var { Order, PosGlobalState} = require('point_of_sale.models');
	const Registries = require('point_of_sale.Registries');


	const POSCustomStockLocation = (PosGlobalState) => class POSCustomStockLocation extends PosGlobalState {

		async _processData(loadedData) {
	        await super._processData(...arguments);
	        this.custom_stock_locations = loadedData['stock.location'] || [];
        }
    }

	Registries.Model.extend(PosGlobalState, POSCustomStockLocation);

	const PosOrder = (Order) => class PosOrder extends Order {
		constructor(obj, options) {
			super(...arguments);
		}
		product_total(){
			let order = this.pos.get_order();
			var orderlines = order.get_orderlines();
			return orderlines.length;
		}
		set_interval(interval){
			this.interval=interval;
		}
	}

	Registries.Model.extend(Order, PosOrder);
});
