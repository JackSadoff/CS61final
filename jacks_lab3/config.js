var config = {
sunapee: {
	database: {
		host     : 'sunapee.cs.dartmouth.edu', 
		user     : 'your username', //'your sunapee username here'
		password : 'your password', //'your sunapee password here'
		schema : 'nyc_inspections' //'your sunapee default schema'
	},
	port: 3000
},
local: {
	database: {
		host     : 'localhost', 
		user     : 'empadmin', //'your localhost username here'
		password : '12345', //your localhost password here'
		schema : 'nyc_inspections' //'your localhost default schema here'
	},
	port: 3000
}
};
module.exports = config;
