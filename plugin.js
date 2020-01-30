const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');


const cliCommand = "nr1"
const commandMap = {
    "validate": "nerdpack:validate"
}

function discover(call, callback) {
    var file = path.join(__dirname, 'plugin.json')
    var data = fs.readFileSync(file);
    var plugin = JSON.parse(data)
    callback(null, plugin)
}

function exec(call, callback) {
    var cmd = call.request.command
    var args = call.request.args

    if (cmd in commandMap) {
        cmd = commandMap[cmd]
    }

    var env = Object.create( process.env );
    env.FORCE_COLOR = 1
    cmd = spawn(cliCommand, [cmd, ...args], { env: env })
    cmd.stdout.on('data', (data) => {
        //console.error(data.toString())
        call.write({
            stdout: data
        })
    });
    cmd.stderr.on('data', (data) => {
        //console.error(data.toString())
        call.write({
            stderr: data
        })
    });
    cmd.on('close', (code) => {
        call.end()
    });
}

module.exports = { discover, exec }