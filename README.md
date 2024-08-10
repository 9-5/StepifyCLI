# StepifyCLI
A casual approach to turning a YouTube video's transcript into an easy to follow along step-by-step process straight from the command line.
---
## About
The following script uses Stepify.tech's API to simplify a YouTube video into a set of simple text instructions. Meant as an early morning brain exercise out of sheer boredom.
---
## Pre-requisites
The following are required to be installed:
- Python
- Chrome 127.0.6533.89 or higher

The following Python libraries:
- Selenium
- Requests

Execute the command `pip install selenium requests` to install the required libraries.
---
## Usage
```
1.) Find a YouTube video you would like to simplify to step-by-step instructions and copy the URL.
2.) Execute the script by running the command "python StepifyCLI.py [YouTube URL]"
3.) If a URL is not inputted as an argument, then an option to input the URL will appear.
4.) The step-by-step tutorial is outputted to the console in a similar manner to the 'more' command.
```
---
## Credits
Stepify.Tech - Providing the API and resources to accomplish this.
