$.fn.serializeObject = function () {
    var o = {};
    var a = this.serializeArray();
    $.each(a, function () {
        if (o[this.name] !== undefined) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            o[this.name].push(this.value || '');
        } else {
            o[this.name] = this.value || '';
        }
    });
    return o;
};



var ProjectListView = Backbone.View.extend({
    el: '.page',
    render: function () {
        var that = this;
        var projects = new Projects();
        projects.fetch({
            success: function (projects) {
                console.log('fetched projects')
                var template = _.template($('#project-list-template').html(), { projects: projects.models });
                that.$el.html(template);
            }
        })
    }
});
var projectListView = new ProjectListView();

var FeatureNewView = Backbone.View.extend({
    el: '.page',
    events: {
        'submit .new-feature-form': 'saveFeature',
    },
    saveFeature: function (ev) {
        $.fn.serializeObject = function () {
            var o = {};
            var a = this.serializeArray();
            $.each(a, function () {
                if (o[this.name] !== undefined) {
                    if (!o[this.name].push) {
                        o[this.name] = [o[this.name]];
                    }
                    o[this.name].push(this.value || '');
                } else {
                    o[this.name] = this.value || '';
                }
            });
            return o;
        };



        var featureDetails = $(ev.currentTarget).serializeObject();
        var user = new Feature();
        user.save(featureDetails, {
            success: function (feature) {
                router.navigate('', { trigger: true });
            }
        });
        return false;
    },
    render: function (options) {
        var that = this;
        var template = _.template($('#feature-form-template').html(), {project: options});
        that.$el.html(template);
    }
});
var featureNewView = new FeatureNewView();