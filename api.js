/* 	Node API demo
	Author: Tim Pierson, Dartmouth CS61, Spring 2020

	Add config.js file to root directory
	To run: nodemon api.js <local|sunapee>
	App will use the database credentials and port stored in config.js for local or sunapee server
	Recommend Postman app for testing verbs other than GET, find Postman at https://www.postman.com/
*/

var express=require('express');
let mysql = require('mysql');
const bodyParser = require('body-parser'); //allows us to get passed in api calls easily
var app=express();

// get config
var env = process.argv[2] || 'local'; //use localhost if enviroment not specified
var config = require('./config')[env]; //read credentials from config.js


//Database connection
app.use(function(req, res, next){
	global.connection = mysql.createConnection({
		host     : config.database.host, 
		user     : config.database.user, 
		password : config.database.password, 
		database : config.database.schema 
	});
	connection.connect();
	next();
});

app.use(bodyParser.urlencoded({extended:true}));
app.use(bodyParser.json());
const bcrypt = require('bcrypt-nodejs');
const saltRounds = 10;

// set up router
var router = express.Router();

// log request types to server console
router.use(function (req,res,next) {
	console.log("/" + req.method);
	next();
});

function get_pkey(table){

	switch (table){
		case "Employee":
		  return "EmployeeID";
		case "EmployeeShift":
			return "ShiftID";
		case "EmployeeType":
			return "EmployeeTypeID";
		case "Patient":
			return "PatientID";
		case "ShiftType":
			return "ShiftTypeID";
		case "Task":
			return "TaskID";
		case "TaskCode":
			return "TaskCodeID";
		case "Room":
			return "RoomID";
		default:
			return "BadTable";
	}

}

// set up routing
// calls should be made to /api/:table/:user/:password with GET/PUT/POST/DELETE verbs
// you can test GETs with a browser using URL http://localhost:3000/api/:table/:user/:password or http://localhost:3000/api/employees/30075445
// recommend Postman app for testing other verbs, find it at https://www.postman.com/
router.get("/",function(req,res){
	res.send("Yo!  This my API.  Call it right, or don't call it at all!");
});

// GET - read data from database, return status code 200 if successful
router.get("/api/:table/:user/:password",function(req,res){
	const table= req.params.table;
const p_key= get_pkey(table);
const username=req.params.user;
	const password=req.params.password;
	global.connection.query('SELECT Password, IsAdmin, EmployeeID FROM Employee WHERE Username = ?', [username],function (error, results, fields) {
		if (error) throw error;
		if (results[0]==undefined){
		res.send(JSON.stringify({"status": 401, "error": "invalid credentials"}));
		return;
		}
		const hash = results[0].Password;const admin=results[0].IsAdmin;const empid=results[0].EmployeeID;
	  bcrypt.compare(password, hash, function(err, success) {
		if (err) throw err;
       if (success && (admin == 1)){ 
	qr_str="";
	qr_str=qr_str.concat("Select * FROM ", table," WHERE True ?")
	var quer=req.query
	// get all employees (limited to first 10 here), return status code 200
	global.connection.query(qr_str,[quer],function (error, results, fields) {
		if (error) throw error;
		res.send(JSON.stringify({"status": 200, "error": null, "response": results}));
	});
} else {

res.send(JSON.stringify({"status": 401, "error": "invalid credentials"}));
console.log("invalid credentials")
}
});
});});
router.get("/api/:table/:user/:password/:id",function(req,res){
	console.log(req.params.id);
		const table= req.params.table;
const p_key= get_pkey(table);
const username=req.params.user;
	const password=req.params.password;
	global.connection.query('SELECT Password, IsAdmin, EmployeeID FROM Employee WHERE Username = ?', [username],function (error, results, fields) {
		if (error) throw error;
		if (results[0]==undefined){
		res.send(JSON.stringify({"status": 401, "error": "invalid credentials"}));
		return;
		}
		const hash = results[0].Password;const admin=results[0].IsAdmin;const empid=results[0].EmployeeID;
	  bcrypt.compare(password, hash, function(err, success) {
		if (err) throw err;
	  if (success && (admin == 1 )){

		  qr_str=""
		  qr_str=qr_str.concat("Select * FROM ",table," WHERE ",p_key," = ?")
	// get all employees (limited to first 10 here), return status code 200
	//read a single employee with RestauantID = req.params.id (the :id in the url above), return status code 200 if successful, 404 if not
	global.connection.query(qr_str, [req.params.id],function (error, results, fields) {
		if (error) throw error;
		res.send(JSON.stringify({"status": 200, "error": null, "response": results}));
	});
} else {
res.send(JSON.stringify({"status": 401, "error": "invalid credentials"}));
console.log("invalid credentials")
}
});
});});
// PUT - UPDATE data in database, make sure to get the ID of the row to update from URL route, return status code 200 if successful
router.put("/api/:table/:user/:password/:id",function(req,res){
	console.log(req.query);
			const table= req.params.table;
const p_key= get_pkey(table);
const username=req.params.user;
	const password=req.params.password;
	global.connection.query('SELECT Password, IsAdmin, EmployeeID FROM Employee WHERE Username = ?', [username],function (error, results, fields) {
		if (error) throw error;
if (results[0]==undefined){
		res.send(JSON.stringify({"status": 401, "error": "invalid credentials"}));
		return;
		}
		const hash = results[0].Password;const admin=results[0].IsAdmin;const empid=results[0].EmployeeID;
	  bcrypt.compare(password, hash, function(err, success) {
		if (err) throw err;
if (success && (admin == 1 )){
	var quer=req.query
	quer_str="";
	  quer_str=quer_str.concat("UPDATE ",table," SET ? WHERE ",p_key," = ?");
	if (table == "Employee"){
	bcrypt.genSalt(saltRounds,function (err,salt){
	if (err) throw error;

	bcrypt.hash(req.query.Password, salt,null, function(err, hash) {
	if (err) throw error;
	console.log(hash);
	if (typeof quer.Password !== 'undefined'){
	quer.Password=hash;}
	console.log(quer);
	//read a single employee with RestauantID = req.params.id (the :id in the url above), return status code 200 if successful, 404 if not
	global.connection.query(quer_str, [quer, req.params.id],function (error, results, fields) {
		if (error) throw error;
		res.send(JSON.stringify({"status": 200, "error": null, "response": results}));
	});
	});
	});} else{
global.connection.query(quer_str, [quer, req.params.id],function (error, results, fields) {
		if (error) throw error;
		res.send(JSON.stringify({"status": 200, "error": null, "response": results}));
	});


	}
	
	
	} else {

res.send(JSON.stringify({"status": 401, "error": "invalid credentials"}));
console.log("invalid credentials")
}
});
});
});


// PUT -[TaskComplete] UPDATE data in database, make sure to get the ID of the row to update from URL route, return status code 200 if successful
router.put("/api/Complete/Task/:user/:password/:id",function(req,res){
    const table= 'Task';
    const p_key= get_pkey(table);
    const username=req.params.user;
    const password=req.params.password;
    var empid=0
    global.connection.query('SELECT Password, IsAdmin, EmployeeID FROM Employee WHERE Username = ?', [username],function (error, results, fields) {
        if (error) throw error;
        if (results[0]==undefined){
                res.send(JSON.stringify({"status": 401, "error": "invalid credentials"}));
                return;
                }
                const hash = results[0].Password;const admin=results[0].IsAdmin;empid=results[0].EmployeeID;
            bcrypt.compare(password, hash, function(err, success) {
                if (err) throw err;
        if (success && (admin == 1 )){
            global.connection.query('UPDATE Task SET IsComplete=1 WHERE TaskID = ?', [req.params.id],function (error, results, fields) {
                if (error) throw error;
                res.send(JSON.stringify({"status": 200, "error": null, "response": results}));
            });
        } else { // Check if user is attempting to update their own task by checking the Task's ShiftID, the Shift's EmployeeID to see if it matches the user's
            global.connection.query('SELECT ShiftID FROM Task WHERE TaskID = ?', [req.params.id],function (error, results, fields) {
                if (error) throw error;
                console.log(results[0].ShiftID)
                global.connection.query('SELECT EmployeeID FROM EmployeeShift WHERE ShiftID = ?', [results[0].ShiftID], function (error, results, fields) {
                    if (error) throw error;
                    empid_of_update = results[0].EmployeeID
                    if (empid_of_update != empid){
                        res.send(JSON.stringify({"status": 401, "error": "invalid credentials"})); 
                        console.log("invalid credentials")
                    } else { // If the user is not the admin, they can only mark their own task as complete
                        global.connection.query('UPDATE Task SET IsComplete=1 WHERE TaskID = ?', [req.params.id],function (error, results, fields) {
                            if (error) throw error;
                            res.send(JSON.stringify({"status": 200, "error": null, "response": results}));
                        });
                    }
                });
            });
        }
});
});
});



// POST -- create new employee, return location of new restaurant in location header, return status code 200 if successful
router.post("/api/:table/:user/:password",function(req,res){
//	console.log(req.query);
	const table= req.params.table;
//const p_key= get_pkey(table);
const username=req.params.user;
	const password=req.params.password;
	global.connection.query('SELECT Password, IsAdmin, EmployeeID FROM Employee WHERE Username = ?', [username],function (error, results, fields) {
	//	if (username!="admin" && password != "admin"){
		if (error) throw error;
		if (results[0]==undefined){
		res.send(JSON.stringify({"status": 401, "error": "invalid credentials"}));
		return;
		}
		const hash = results[0].Password;const admin=results[0].IsAdmin;const empid=results[0].EmployeeID;
	//	}else {
	//	admin=1
	//	hash=234234
	//	}
	  bcrypt.compare(password, hash, function(err, success) {
	//	if (err) throw err;
	//	if (success && admin == 1){
		  if (admin==1){
	var quer=req.query
	qr_str="";
	qr_str=qr_str.concat("INSERT INTO ",table," SET ?");

	console.log(qr_str);
			  if (table == "Employee"){
	bcrypt.genSalt(saltRounds,function (err,salt){
	if (err) throw error;

	bcrypt.hash(req.query.Password, salt,null, function(err, hash) {
	if (err) throw error;
	console.log(hash);
	quer.Password=hash;
	console.log(quer);
	//read a single employee with RestauantID = req.params.id (the :id in the url above), return status code 200 if successful, 404 if not
	global.connection.query(qr_str, [quer],function (error, results, fields) {
		if (error) throw error;
		res.send(JSON.stringify({"status": 200, "error": null, "response": results}));
	});
	});
	});
			} else {
	global.connection.query(qr_str, [quer],function (error, results, fields) {
		if (error) throw error;
		res.send(JSON.stringify({"status": 200, "error": null, "response": results}));
	});


			}
			  } else {

res.send(JSON.stringify({"status": 401, "error": "invalid credentials"}));
console.log("invalid credentials")
}
});
});
	
});

// DELETE -- delete employee with EmployeeID of :id, return status code 200 if successful
router.delete("/api/:table/:user/:password/:id",function(req,res){
	console.log(req.params);
	const table= req.params.table;
const p_key= get_pkey(table);
const username=req.params.user;
	const password=req.params.password;
	global.connection.query('SELECT Password, IsAdmin, EmployeeID FROM Employee WHERE Username = ?', [username],function (error, results, fields) {
		if (error) throw error;
		if (results[0]==undefined){
		res.send(JSON.stringify({"status": 401, "error": "invalid credentials"}));
		return;
		}
		const hash = results[0].Password;const admin=results[0].IsAdmin;const empid=results[0].EmployeeID;
	  bcrypt.compare(password, hash, function(err, success) {
		if (err) throw err;
		if (success && admin == 1){
	//read a single employee with RestauantID = req.params.id (the :id in the url above), return status code 200 if successful, 404 if not
	  qr_str="";
	  qr_str=qr_str.concat("DELETE FROM ",table," WHERE ", p_key," = ?")
	global.connection.query(qr_str, [req.params.id],function (error, results, fields) {
		if (error) throw error;
		res.send(JSON.stringify({"status": 200, "error": null, "response": results}));
	});} else {

res.send(JSON.stringify({"status": 401, "error": "invalid credentials"}));
console.log("invalid credentials")
}
});
});
});




// start server running on port 3000 (or whatever is set in env)
app.use(express.static(__dirname + '/'));
app.use("/",router);
app.set( 'port', ( process.env.PORT || config.port || 3000 ));

app.listen(app.get( 'port' ), function() {
	console.log( 'Node server is running on port ' + app.get( 'port' ));
	console.log( 'Environment is ' + env);
});
