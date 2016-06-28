# SimplePythonServer

a simple python server handles POST and GET request and have simple router function

for example, when you come in a request say GET /TestInterface/User/GetUserInfo
you need to write a class in the project folder following the request path
TestInterface.User.GetUserInfo and have a method called do_GET() where you should
return the result for this request in bytes data. The POST request acts the same way
but use do_POST() method.

whatever error, the server will return 404

see the code and the test classes for more detail
