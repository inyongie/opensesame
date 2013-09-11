<!doctype html>
<html>
  <head>
    <title>OpenSesame</title>
    <meta charset="utf-8" />
    <style type="text/css">
      body {
        text-align: center;
        min-width: 500px;
      }
    </style>
    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>
    <script>
      $(function(){
        var ws;
        var logger = function(msg){
          var now = new Date();
          var sec = now.getSeconds();
          var min = now.getMinutes();
          var hr = now.getHours();
	  if(sec < 10) {
	    sec = "0"+sec;
	  }
	  if(min < 10) {
	    min = "0"+min;
	  }
	  if(hr < 10) {
	    hr = "0"+hr;
	  }
          $("#log").html($("#log").html() + "<br/>" + hr + ":" + min + ":" + sec + " - " +  msg);
          //$("#log").animate({ scrollTop: $('#log')[0].scrollHeight}, 100);
          $('#log').scrollTop($('#log')[0].scrollHeight);
        }
 
        var sender = function() {
          var msg = $("#msg").val();
          if (msg.length > 0)
            ws.send(msg);
          $("#msg").val(msg);
        }
 
        ws = new WebSocket("ws://inyongie.com:8888/ws");
        ws.onmessage = function(evt) {
 
          logger(evt.data);
        };
        ws.onclose = function(evt) { 
          $("#log").text("Connection was closed..."); 
          $("#thebutton #msg").prop('disabled', true);
        };
        ws.onopen = function(evt) { $("#log").text("Opening socket..."); };

	var clearTextBox = function() {
	  $("#msg").val('');
	}
 
        $("#msg").keypress(function(event) {
          if (event.which == 13) {
             sender();
	     clearTextBox();
           }
        });
 
        $("#thebutton").click(function(){
          sender();
	  clearTextBox();
        });
      });
    </script>
  </head>
 
  <body>
    <h1>OpenSesame</h1>
    <div id="log" style="overflow:scroll;width:500px; height:200px;background-color:#ffeeaa; margin:auto; text-align:left">Messages go here</div>
 
    <div style="margin:10px">
      <input type="text" id="msg" style="background:#fff;width:200px"/>
      <input type="button" id="thebutton" value="Send" />
    </div>
  </body>
</html>
