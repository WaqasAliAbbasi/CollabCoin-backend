Meteor.methods({
	buyStock: function(symbol,quantity){
		try {
			response = HTTP.call( 'POST', Config.backend + "/asset/order", {
				headers: {
				"Content-Type" : "application/json"
				},
				data: {
					"playerID": Config.publicKey,
					"orderAction": "BUY",
					"orderSymbol": symbol,
					"orderQuantity": quantity
				}
			});
			return JSON.parse(response.content)["purchasePrice"];
		} catch(error){
			console.log(error);
		}
	},
	sellStock: function(txid){
		try {
			response = HTTP.call( 'POST', Config.backend + "/asset/order", {
				headers: {
					"Content-Type" : "application/json"
				},
				data: {
					"playerID": Config.publicKey,
					"orderAction": "SELL",
					"txID": txid,
					"privateKey": Config.privateKey
				}
			});
			return JSON.parse(response.content)["purchasePrice"];
		} catch(error){
			console.log(error);
		}
	},
	getStocks: function() {
        console.log('getting stocks');
        try {
        	var result = HTTP.get(Config.backend + "/assets/" + Config.publicKey);
        	return result.content;
        } catch(e) {
        	console.log( "Cannot get owned stocks", e );
        }
    }
});