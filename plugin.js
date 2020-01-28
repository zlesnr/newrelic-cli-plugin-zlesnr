const { spawn } = require('child_process');

const cliCommand = "nr1"

function discover(call, callback) {
    commands = {
        Commands: [{
            Use: "abc",
            Short: "def",
            Long: "ghi",
        }]
    }

    //console.error(commands)
    callback(null, commands)
}

function exec(call, callback) {
    var cmd = call.request.command
    var args = call.request.args

    cmd = spawn(cliCommand, [cmd, ...args])
    cmd.stdout.on('data', (data) => {
        call.write({
            stdout: data
        })
    });
    cmd.stderr.on('data', (data) => {
        call.write({
            stderr: data
        })
    });
    cmd.on('close', (code) => {
        call.end()
    });
}

module.exports = { discover, exec }