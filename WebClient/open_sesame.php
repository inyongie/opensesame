<!doctype html>
<html>
  <head>
    <title>OpenSesame</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=320px, user-scalable=false;">
    <style type="text/css">
      body {
        text-align: center;
        min-width: 300px;
      }
      .defaultFont {
      	font-family: 'Lucida Grande', Helvetica, Arial, Sans-Serif;
      }
      #log {
	overflow-y:hidden;
	overflow-x:hidden;
	width:300px; 
	height:100px;
	background-color:#cccccc; 
	margin:auto; 
	text-align:left;
      	font-size: 10px;
      }
      #msg {
	background:#fff;
	width:294px;
      }
      .tb5 {
	border:3px solid #456879;
	border-radius:10px;
	height: 30px;
	margin:	10px 0 10px 0;
      	font-size: 24px;
      }
      .button {
	width: 300px;
	border-top: 1px solid #9ff797;
      	background: #65d66c;
      	background: -webkit-gradient(linear, left top, left bottom, from(#4b9c3e), to(#65d66c));
      	background: -webkit-linear-gradient(top, #4b9c3e, #65d66c);
      	background: -moz-linear-gradient(top, #4b9c3e, #65d66c);
      	background: -ms-linear-gradient(top, #4b9c3e, #65d66c);
      	background: -o-linear-gradient(top, #4b9c3e, #65d66c);
      	padding: 20px 40px;
      	-webkit-border-radius: 5px;
      	-moz-border-radius: 5px;
      	border-radius: 5px;
      	-webkit-box-shadow: rgba(0,0,0,1) 0 1px 0;
      	-moz-box-shadow: rgba(0,0,0,1) 0 1px 0;
      	box-shadow: rgba(0,0,0,1) 0 1px 0;
      	text-shadow: rgba(0,0,0,.4) 0 1px 0;
      	color: white;
      	font-size: 24px;
      	text-decoration: none;
      	vertical-align: middle;
      }
      .button:hover {
	border-top-color: #2e7828;
      	background: #2e7828;
      	color: #ccc;
      }
	.button:active {
      	border-top-color: #2d5c1b;
      	background: #2d5c1b;
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
          var decodedMsg = JSON.parse(msg);
          $("#log").html($("#log").html() + "<br/>" + hr + ":" + min + ":" + sec + " - " +  decodedMsg.message);
          //$("#log").animate({ scrollTop: $('#log')[0].scrollHeight}, 100);
          $('#log').scrollTop($('#log')[0].scrollHeight);
        }
 
        var sender = function() {
          var msg = $("#msg").val();
          if (msg.length > 0) {
            if(msg == "open")
              ws.send('{"type":"request"}');
            else
              ws.send('{"type":"miscMsg","message":"'+msg+'"}');
          }
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
    <div id="log" class="defaultFont"></div>
    <input type="text" class="tb5 defaultFont" id="msg" /><br/>
    <input type="button" id="thebutton" class="button defaultFont" value="Open Sesame" />
  </body>
</html>
