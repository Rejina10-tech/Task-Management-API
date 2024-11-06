<script>
  $(function() {
    $( ".datepicker" ).datepicker({
      changeMonth: true,
      changeYear: true,
      yearRange: "1900:2012",
      // You can put more options here.

    })
  });
  </script>


var message_timeout = document.getElementById("message-timer");

setTimeout(function()
{


  message_timeout.style.display = 'none';
}, 5000);






