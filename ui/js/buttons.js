var $red = $('#red');
var $blue = $('#blue');
var $yellow = $('#yellow');

function blinkButton($button) {
  var counter = 0;
  var timer = setInterval(function() {
    counter += 1;
    var bgcolor = counter % 2 == 0 ? '' : 'rgb(255, 255, 255)'
    var color = counter % 2 == 0 ? '' : 'rgb(255, 0, 0)'
    $button.css({
      backgroundColor: bgcolor,
      color: color
    });
    if (counter >= 10) {
      clearInterval(timer);
      timer = null;
      $button.css({
        backgroundColor: '',
        color: ''
      });
    }
  }, 50);
  $button.css({
    backgroundColor: 'rgb(255, 255, 255)',
    color: 'rgb(255, 0, 0)'
  });
  var stop = function() {
    if (timer) {
      clearInterval(timer);
      timer = null;
    }
    $button.css({
      backgroundColor: '',
      color: ''
    });
  };
  return stop;
}

$red.click(function() {
  console.log('red');
  var $data = {'red':5};
  var stop = blinkButton($red);
  blink($data, function() {
    stop();
  });
  ga('send', 'event', 'Lights', 'Flash', 'Red', 5);
});

$blue.click(function() {
  console.log('blue');
  var $data = {'blue':5};
  var stop = blinkButton($blue);
  blink($data, function() {
    stop();
  });
  ga('send', 'event', 'Lights', 'Flash', 'Blue', 5);
});

$yellow.click(function() {
  console.log('yellow');
  var $data = {'green':5};
  var stop = blinkButton($yellow);
  blink($data, function() {
    stop();
  });
  ga('send', 'event', 'Lights', 'Flash', 'Yellow', 5);
});

function blink($data, callback) {
  $data = JSON.stringify($data);
  $.ajax({
    type: 'POST',
    url: 'https://xmas-api.clouden.net/flash',
    data: $data,
    contentType: 'application/json; charset=utf-8',
    dataType: 'json',
    success: function(response) {
      if (callback) {
        callback();
      }
    }
  });
}
