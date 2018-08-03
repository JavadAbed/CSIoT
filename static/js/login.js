
(function(){
    login = function(e) {
        e.preventDefault();
        return apiCall("POST", "/auth/login", $("#login-form").serializeObject()).done(function(data) {
          if(data['status'] == '1'){
            window.location.href = "/dashboard";
          }else{
            // show error
          }
        });
      };

      $(function() {
        $("#login-form").on("submit", login);
      });
}).call(this);
