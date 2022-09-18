# Error codes for Download-Compress-Media

These are custom error codes that I have created for my own script.

If there is an error that is being shown, and you know for sure it shouln't be shown, please create an issue with the following information:

* Python version
* Dependency versions
* OS type and version
* URL that you tried to download
* Error message

I will update the list as I see fit.

*Current as of 9/18/22*

---

ERROR CODES:

0 - Unknown error. Youtube-DL was unable to download the media for some unspecified reason. This may be because of an error message not implemented yet.

1 - URL does not point to a valid media source. Check the URL and try again. Make sure you can access the URL on a browser.

2 - Unable to extract media source. - Youtube-DL was unable to find a valid media source. Please use the direct link instead.

3 - Unable to download webpage: HTTP Error 404: - The URL is not valid. Please make sure the URL is valid and try again. 

---

PYTHON ERROR CODES:

[Errno 75] Value too large for defined data type: 'URL.txt' -> 'URL.txt.bak' - This has only been triggered when the script does not have read/write permissions for URL.txt

TODO:

