# Lecture Download Script
Simple script for downloading lectures from echo360 for university of melbourne students.

Requires Python 3.5+ with Selenium Webdriver package, google chrome, appropriate chromedriver.
Webdriver can be plaed in PATH or else in same folder as python script.

Need to created an echo360 account, and link it to your unimelb account (allows you to login to echo360 without going through the LMS)

## Usage:
For more info on usage, use the --help flag  (eg python lecturedownloader.py --help)

### Positional args (required)
lectureDownloader [URL of echo360 lecture page][echo360 email][unimelbUsername][unimelbPassword]

### Flags (optional)
-d :    Download location (relative to downloads folder, eg specify a new folder to create)
-w :    Time to wait (seconds) between webdriver actions (defaults to 3 seconds, extend if              slower connections)
-s  :   Number of initial lectures to skip downloading (useful if a previous execution was              interrupted)

### Example Usage

`python lecdownloader.py https://echo360.org.au/section/90f4ef0a-fd08-4efb-9c9e-b7ba9a5e0150/home ccarner13@gmail.com ccarner COLTONSPW01 -d securityLectures -w 5`
- Downloads from echo360 page located at https://echo360.org.au/section/90f4ef0a-fd08-4efb-9c9e-b7ba9a5e0150/home
- Has an Echo360 account set up associated with the email ccarner13@gmail.com
- Unimelb Username of ccarner
- Unimelb Password of COLTONSPW01
- Saving to downloads/securityLectures
- Waits for 5 seconds between clicks
