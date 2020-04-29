### Usage

Install the protobuf compiler and Go support:
```
brew update && brew install protobuf && brew install protoc-gen-go
```

Install the python modules:
```
pip install -r requirements
```

Compile protocols for pytohn.

```
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. extention.proto
```
