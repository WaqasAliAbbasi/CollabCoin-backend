@Schemas = {}

# Non collection Schemas
Schemas.updatePassword = new SimpleSchema
  old:
    type: String
    label: "Current Password"
    max: 50

  new:
    type: String
    min: 6
    max: 20
    label: "New Password"

  confirm:
    type: String
    min: 6
    max: 20
    label: "Confirm new Password"

Schemas.buyStock = new SimpleSchema
  symbol:
    type: String
    min: 1
    max: 10

  quantity:
    type: Number
    min: 1

  owner:
    type: String
    regEx: SimpleSchema.RegEx.Id
    autoValue: ->
      if this.isInsert
        Meteor.userId()
    autoform:
      options: ->
        _.map Meteor.users.find().fetch(), (user)->
          label: user.emails[0].address
          value: user._id