
(function() {

    $.fn.serializeObject = function() {
        var a, o;
        o = {};
        a = this.serializeArray();
        $.each(a, function() {
          if (o[this.name]) {
            if (!o[this.name].push) {
              o[this.name] = [o[this.name]];
            }
            return o[this.name].push(this.value || '');
          } else {
            return o[this.name] = this.value || '';
          }
        });
        return o;
      };


    this.apiCall = function(type, url, data) {
        return $.ajax({
        url: url,
        type: type,
        data: data,
        cache: false
        }).fail(function(jqXHR, text) {
            return console.log("Server is down.",text);
        });
    };
}).call(this);
