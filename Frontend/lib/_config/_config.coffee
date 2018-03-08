# These values get propagated through the app
# E.g. The 'name' and 'subtitle' are used in seo.coffee

@Config =

	# Basic Details
	name: 'CollabCoin'
	title: ->
			TAPi18n.__ 'configTitle'
	subtitle: ->
			TAPi18n.__ 'configSubtitle'
	logo: ->
		'<b>' + @name + '</b>'
	footer: ->
		@name + ' - Copyright ' + new Date().getFullYear()

	# Emails
	emails:
		from: 'no-reply@' + Meteor.absoluteUrl()
		contact: 'hello' + Meteor.absoluteUrl()

	# Username - if true, users are forced to set a username
	username: false
	
	# Localisation
	defaultLanguage: 'en'
	dateFormat: 'D/M/YYYY'

	# Meta / Extenrnal content
	privacyUrl: 'http://collabcoin.io'
	termsUrl: 'http://collabcoin.io'

	# For email footers
	legal:
		address: 'Hong Kong'
		name: 'CollabCoin'
		url: 'http://collabcoin.io'

	about: 'http://collabcoin.io'
	blog: 'http://learn.collabcoin.io'

	socialMedia:
		github:
			url: 'http://github.com/WaqasAliAbbasi/CollabCoin'
			icon: 'github'
		info:
			url: 'http://collabcoin.io'
			icon: 'link'

	#Routes
	homeRoute: '/'
	publicRoutes: ['home']
	dashboardRoute: '/dashboard'
	backend: 'http://127.0.0.1:5000'

	#Test
	publicKey: 'GTPRhKNfTyGiExbN2mzAH7nzYsRmFwd83sGYpUrJ3avQ'
	privateKey: 'CJDMTBB7AbVQib25dBc7b8dDq1gbrod7wEo61bXeVfAS'