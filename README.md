### Usage

Install the protobuf compiler and Go support:
```
brew update && brew install protobuf && brew install protoc-gen-go
```

Install the node modules:
```
cd $PROJECT_ROOT/node-plugin && npm install
```

Generate the protobuf code for the plugin host:
```
cd $PROJECT_ROOT/host && protoc -I=. --go_out=plugins=grpc:. ./protoDef/cli-plugin.proto
```

Run the example:
```
cd $PROJECT_ROOT/host && go run main.go
```