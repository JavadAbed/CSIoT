(function(){

    loadCardInfo = function(card, data) {
        return apiCall("GET", "/ebanking/card/"+card+"/info/"+data ).done(function(data) {
          console.log(data);
          if(data['status'] == '1'){
            $("#pin2info").text(data['data']['user.first_name'] + " " + data['data']['user.last_name'])
          }else{
            $("#pin2info").text(data['message'])
          }
        });
      };


    send_otp = function(){
      return apiCall("GET", "/ebanking/send_transfer_otp" ).done(function(data) {
        console.log(data);
        if(data['status'] == '1'){
          $("#otp_result_message").text(data['message'])
        }else{
          $("#otp_result_message").text(data['message'])
        }
      });
    };


      $(function() {


        $("#pan2getinfo").on("click", function(e) {
          e.preventDefault();
          var data = btoa(JSON.stringify(["user.first_name","user.last_name"]))
          var card = $('#pan2').val().replace(/\D/g,'');
          if(card.length > 0){
            loadCardInfo(card, data)
          }
        });

        $("#sendOTP").on("click", function(e) {
          e.preventDefault();
          send_otp()
          
        });

        
        
      });
}).call(this);
