$("#login").click(function() {
   $.ajax("/login", {
     data:"{\"password\":\"password\"}",
     contentType : 'application/json',
     type : 'POST',
     success: function(data) {
     }
   })
 });

 $("#pause").click(function() {
   $.ajax("/load", {
     contentType : 'application/json',
     type : 'POST',
     success: function(data) {
     }
   })
 });

 $("#play").click(function() {
   $.ajax("/train", {
     contentType : 'application/json',
     type : 'POST',
     success: function(data) {
     }
   })
 });

 $("#stop").click(function() {
   $.ajax("/stop", {
     contentType : 'application/json',
     type : 'POST',
     success: function(data) {
     }
   })
 });

 $("#save").click(function() {
   $.ajax("/save", {
     contentType : 'application/json',
     type : 'POST',
     success: function(data) {
     }
   });
 });
