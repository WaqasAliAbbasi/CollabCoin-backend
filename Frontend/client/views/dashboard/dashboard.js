Template.addPost.helpers({
	"yearOptions": function() {
    return [
        {label: "2013", value: 2013},
        {label: "2014", value: 2014},
        {label: "2015", value: 2015}
    ];
    }
});

Template.stocks.helpers({
  stocks: function(){
    return JSON.parse(ReactiveMethod.call('getStocks'));
  }
});

Template.addPost.events({
	'click #buy': function(e){
		e.preventDefault();
		symbol = $('#buy').parent().find('input[name="symbol"]').val();
		quantity = $('#buy').parent().find('input[name="quantity"]').val()
		waitingDialog.show("Processing");
		Meteor.call('buyStock',symbol,quantity,function(error,response){
			waitingDialog.hide();
			console.log(response);
			$('#stockModalPrice').text("Bought for $" + response);
			$('#stockModal').modal('show');
		});
	}
});

Template.stocks.events({
	'click #sell': function(e){
		e.preventDefault();
		txid=$(e.target).attr("txid");
		waitingDialog.show("Processing");
		Meteor.call('sellStock',txid,function(error,response){
			waitingDialog.hide();
			$('#stockModalPrice').text("Sold for $" + response);
		$('#stockModal').modal('show');
		});
	},
	'click #submitportfolio': function(e){
		waitingDialog.show("Processing");
		setTimeout(function(){
			waitingDialog.hide();
			$('#doneModal').modal('show');
		},1500);
	}
});

Handlebars.registerHelper("inc", function(value, options)
{
    return parseInt(value) + 1;
});
/**
 * Module for displaying "Waiting for..." dialog using Bootstrap
 *
 * @author Eugene Maslovich <ehpc@em42.ru>
 */

var waitingDialog = waitingDialog || (function ($) {
    'use strict';

	// Creating modal dialog's DOM
	var $dialog = $(
		'<div class="modal fade" data-backdrop="static" data-keyboard="false" tabindex="-1" role="dialog" aria-hidden="true" style="padding-top:15%; overflow-y:visible;">' +
		'<div class="modal-dialog modal-m">' +
		'<div class="modal-content">' +
			'<div class="modal-header"><h3 style="margin:0;"></h3></div>' +
			'<div class="modal-body">' +
				'<div class="progress progress-striped active" style="margin-bottom:0;"><div class="progress-bar" style="width: 100%"></div></div>' +
			'</div>' +
		'</div></div></div>');

	return {
		/**
		 * Opens our dialog
		 * @param message Custom message
		 * @param options Custom options:
		 * 				  options.dialogSize - bootstrap postfix for dialog size, e.g. "sm", "m";
		 * 				  options.progressType - bootstrap postfix for progress bar type, e.g. "success", "warning".
		 */
		show: function (message, options) {
			// Assigning defaults
			if (typeof options === 'undefined') {
				options = {};
			}
			if (typeof message === 'undefined') {
				message = 'Loading';
			}
			var settings = $.extend({
				dialogSize: 'm',
				progressType: '',
				onHide: null // This callback runs after the dialog was hidden
			}, options);

			// Configuring dialog
			$dialog.find('.modal-dialog').attr('class', 'modal-dialog').addClass('modal-' + settings.dialogSize);
			$dialog.find('.progress-bar').attr('class', 'progress-bar');
			if (settings.progressType) {
				$dialog.find('.progress-bar').addClass('progress-bar-' + settings.progressType);
			}
			$dialog.find('h3').text(message);
			// Adding callbacks
			if (typeof settings.onHide === 'function') {
				$dialog.off('hidden.bs.modal').on('hidden.bs.modal', function (e) {
					settings.onHide.call($dialog);
				});
			}
			// Opening dialog
			$dialog.modal();
		},
		/**
		 * Closes dialog
		 */
		hide: function () {
			$dialog.modal('hide');
		}
	};

})(jQuery);
