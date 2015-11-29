
var Router = Backbone.Router.extend({
    routes: {
        "": "home",
        "feature/new/:id": "new",
    }
});
var router = new Router;
router.on('route:home', function () {
    // render user list
    projectListView.render()
})
router.on('route:new', function (id) {
    featureNewView.render()
})
Backbone.history.start();