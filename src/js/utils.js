'use strict';
var cmi = cmi || {};

cmi.utils = {
  render_template: function(settings) {
    /**
     * Dependencies: Handlebar.js, jQuery.js
     *
     * settings = {
     *   template: '#script-id',
     *   target: '#query-string',
     *   context: {},
     *   append: boolean (optional),
     *   prepend: boolean (optional)
     * }
     */
    // get Handlebar template
    if (!settings.template || settings.template ==='') {
      $(settings.target).html(''); // if template is empty, clear HTML of target
      return;
    }
    var template = Handlebars.compile($(settings.template).html());

    // render it (check it we have a context)
    var html = template( settings.context ? settings.context : {} );

    if (settings.append) $(settings.target).append(html);
    else if (settings.prepend) $(settings.target).prepend(html);
    else $(settings.target).html(html);

  },

  load_localStorage: function (storage_name) {
    return JSON.parse(localStorage.getItem(storage_name));
  },

  save_localStorage: function (storage_name, JSON_data) {
    localStorage.setItem(storage_name, JSON.stringify(JSON_data));
    console.log('data saved: ' + storage_name);
  },

  clear_localStorage: function (storage_name) {
    localStorage.removeItem(storage_name);
    console.log('data removed: ' + storage_name);
  }

}
