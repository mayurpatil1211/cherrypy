var express = require('express');
var app = express();
var bodyparser = require('body-parser');
var portNumber = process.env.PORT || 8070;
app.use(bodyparser.urlencoded({ extended: true }));
app.use(bodyparser.json());
app.use(express.static(__dirname +'/public'));

var allowCrossDomain = function(req, res, next) {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE');
    res.header('Access-Control-Allow-Headers', 'Content-Type');
    console.log("testing cross origin")
    next();
}

app.use(allowCrossDomain);

app.listen(portNumber)
console.log("listening on port "+portNumber)

