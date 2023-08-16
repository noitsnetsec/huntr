 .S    S.    .S       S.    .S_sSSs    sdSS_SSSSSSbs   .S_sSSs    
.SS    SS.  .SS       SS.  .SS~YS%%b   YSSS~S%SSSSSP  .SS~YS%%b   
S%S    S%S  S%S       S%S  S%S   `S%b       S%S       S%S   `S%b  
S%S    S%S  S%S       S%S  S%S    S%S       S%S       S%S    S%S  
S%S SSSS%S  S&S       S&S  S%S    S&S       S&S       S%S    d*S  
S&S  SSS&S  S&S       S&S  S&S    S&S       S&S       S&S   .S*S  
S&S    S&S  S&S       S&S  S&S    S&S       S&S       S&S_sdSSS   
S&S    S&S  S&S       S&S  S&S    S&S       S&S       S&S~YSY%b   
S*S    S*S  S*b       d*S  S*S    S*S       S*S       S*S   `S%b  
S*S    S*S  S*S.     .S*S  S*S    S*S       S*S       S*S    S%S  
S*S    S*S   SSSbs_sdSSS   S*S    S*S       S*S       S*S    S&S  
SSS    S*S    YSSP~YSSY    S*S    SSS       S*S       S*S    SSS  
       SP                  SP               SP        SP          
       Y                   Y                Y         Y           
                                                                                                                                   
version 1.0.0
                                                                                                               
                                                                                                                                                                                                              
HUNTR Security Tool README.txt
_____________________________________________________________________________________________________________________________________________________________________________________________________________
*************
ABOUT
*************

For my Cybersecurity Bootcamp Course Capstone Project. 

With this all in one security testing tool, you can explore, find digital clues, and test systems for security gaps. 

Whether you're just starting out or have some experience, Huntr aims to be your go-to tool for security checks.

_____________________________________________________________________________________________________________________________________________________________________________________________________________
*********
IMPORTANT
*********

- Make sure to read the entire README.txt file to ensure you have an understanding of how the tool and it's features work.

- Always ensure proper permissions before conducting any tests.
_____________________________________________________________________________________________________________________________________________________________________________________________________________
*************
RECONAISSANCE
*************

- Ping Scanner: 
   - Quickly identify active hosts in a network.
   - Used to check if a host is up.
   - Essential for initial network mapping and footprinting.
   - Provides round-trip time metrics for network diagnostics.

- Port Scanner: 
   - Identify open ports on target hosts.
   - Recognize running services and potential vulnerabilities.
   - Supports both TCP and UDP scans.
   - Uses Nmap, an install would be required based on the OS you are using, see more info under "Installation".

- Email Scanner:
   -  Retrieve email addresses associated with a domain.
   - Identify potential targets for phishing campaigns.
   - Gauge the digital footprint of an organization.
   - Uses Hunter.io's databse and requires their API Key which is free.

- TheHarvester GUI:
   - Simular to the Email Scanner but reaches out to many more databases using TheHarvester, but requires some API Keys to for more detailed information.
   - Extract names, emails, and subdomains from various sources.
   - Aids in gathering comprehensive target information.
   - Intuitive GUI enhances ease of use.

- Information Gathering:
   - Whois Domain Lookup: Get details about domain ownership, registration, and expiration.
   - Whois IP Lookup: Learn about IP ownership, associated organizations, and contact details.
   - Reverse DNS Lookup: Convert IP addresses to hostnames for better clarity.
   - IP Geolocation: Locate IP origins including city, country, and sometimes even more granular details.
   - HTTP Headers: Extract server metadata, security policies, and potential misconfigurations.
   - Subnet Calculator: Compute essential network details like address range, broadcast, and netmask.

- Directory Buster:
   - Custom directory busting tool made in python.
   - Discover hidden directories and files.
   - Use custom or popular wordlists for targeted scans.
   - Unearth potential vulnerabilities or sensitive data.
   - Provides the option to use your own wordlists.

- Recon-ng:
   - A comprehensive reconnaissance framework written in Python.
   - Conduct web-based discovery of assets.
   - Incorporate various modules for different reconnaissance tasks.
   - Easily extendable with custom modules.
   - Integrates with popular third-party services and databases for gathering intelligence.

NOTE: The default wordlists uses a top 1000 subdomain list
_____________________________________________________________________________________________________________________________________________________________________________________________________________
*********
FORENSICS
*********

- Hash Identifier:
   - Distinguish between various hash types (e.g., MD5, SHA1, SHA256, SHA512).
   - Facilitates decryption and security assessment processes.
   - Works fast, 1000 Attempts per second.
   - Notification sound upon succesfully cracking the hash.
_____________________________________________________________________________________________________________________________________________________________________________________________________________
*********
OFFENSIVE
*********

- Hash Cracker:
   - Attempt to reverse hashed passwords.
   - Utilize brute force, dictionary, and rainbow table techniques.
   - Assess the resilience of password protection mechanisms.

- Web Login Bruteforcing Tool:
   - Challenge web login mechanisms.
   - Identify weak passwords and misconfigurations.
   - Supports various authentication types and methods.

- GoPhish:
   - Open-source phishing toolkit designed for businesses and penetration testers.
   - Allows users to easily create and execute phishing campaigns.
   - Features a user-friendly web interface for campaign creation and monitoring.
   - Collects detailed metrics on user responses to measure the effectiveness of training.
   - Provides the option for template customization to mimic various types of phishing attacks.

_____________________________________________________________________________________________________________________________________________________________________________________________________________
*************
MISCELLANEOUS
*************

- Tor Integration:
   - Route traffic through the Tor network.
   - Enhance privacy and circumvent geo-restrictions.
   - Useful for both anonymized browsing and testing.

###########
PLEASE NOTE

When you enable Tor within Huntr, the software will modify the proxy settings for your entire system to route traffic through the Tor network.

For Windows users: This means the tool will make changes to your system registry, specifically at "Computer\HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings".

Linux aficionados: The command "gsettings set org.gnome.system.proxy mode 'manual'" will be invoked, along with additional settings.

When you stop tor these settings will be reset to what they were.

For peace of mind, users can opt to establish their Tor connection manually if they're wary of this automated process.

############

- Resources:
   - Collated list of helpful guides, references, and tools.
   - Stay updated with the latest in cybersecurity.
   - Enhance your skills and knowledge base.

_____________________________________________________________________________________________________________________________________________________________________________________________________________
***************
TROUBLESHOOTING
***************

1. **Huntr fails to start**:
   - Ensure that all prerequisites, as mentioned in the 'Installation' section, are correctly installed and configured.


2. **Issues with Tor Integration**:
   - Ensure you have the latest version of Tor installed and if you are on Windows replace the Tor folder in the huntr directory.
   - Check your system's proxy settings to ensure that they have not been altered by other software.

3. **Error messages during scans**:
   - Ensure that you have proper permissions for the network or system you're scanning.

_____________________________________________________________________________________________________________________________________________________________________________________________________________
*********
CHANGELOG
*********

Version 1.0.0 - [September 9 2023]
- Initial release of Huntr [UPCOMING]

_____________________________________________________________________________________________________________________________________________________________________________________________________________
****
FAQ
****

1. What is Huntr?
   - Huntr is an all-in-one security testing tool designed to explore, find digital clues, and test systems for security gaps.

2. Do I need any prior knowledge to use Huntr?
   - While Huntr is designed to be user-friendly for both beginners and experts, some basic understanding of cybersecurity concepts will be beneficial.

3. Is Huntr free?
   - Yes, Huntr is free and open source, feel free to change and redistribute it.

4. How do I report bugs or issues with Huntr?
   - Please refer to the 'Feedback and Reporting Bugs' section for information on how to report issues.

_____________________________________________________________________________________________________________________________________________________________________________________________________________
************
INSTALLATION
************

#
##########
WINDOWS 10

Downloading the Huntr Directory:

1. Navigate to the directory where you wish to install Huntr
2. Download the files using Git.

Running:

1. Navigate to the Huntr directory.
2. Open terminal in the Huntr directory on the Huntr executable or run it from the command prompt using "python huntr.py"

Prerequisites:
- Nmap: You can download the latest version of Nmap for Windows from their official website. Once downloaded, simply follow the installation instructions.
- Python: Make sure you have Python installed. If not, download it from the official website and follow the setup guide.
- Tor: Tor should be located in the Huntr directory under "Addons" but if you are having errors follow the instructions below.

Installing Nmap on Windows:

1. Go to NMAP's official download page.
2. Download the Windows Installer
3. Look for the section labeled "Microsoft Windows Binaries" and download the latest stable version available as a self-installer.
4. Install NMAP
5. Once the download is complete, locate the downloaded file (it should have an .exe extension) and run it. This will launch the NMAP installer.
6. Follow the on-screen instructions. During the installation process, you may be prompted to install WinPcap and Npcap. It's recommended to install these as they are essential for NMAP's packet capturing capabilities.
7. Confirm Installation
8. Once the installation is complete, open the Command Prompt and type nmap then press Enter. If NMAP is installed correctly, you should see its version details and usage options.
9. Make sure it is added to your system's PATH in the enviroment variables settings. (Look online for help if needed)

Installing Python:
1. Visit Python's Official Website
2. Go to Downloads
3. Hover over the "Downloads" tab at the top of the page.
4. Click on the "Windows" option from the dropdown.
5. Download the Latest Version
6. Run the Installer
7. At the bottom of the installation window, there's an option that says "Add Python X.Y to PATH" (where X.Y is the version number). Ensure you check this box. This step is crucial to add Python to your system's PATH.
8. Click on the "Install Now" option, which will install Python with the default settings.
9. To verify the installation open command prompt and enter "python --version". This command should display the Python version you installed, confirming that Python was successfully installed and added to the PATH.

Installing Tor:
1. Navigate to https://www.torproject.org/download/tor/
2. Select the Tor Expert Bundle for Windows (x86_64)
3. Download the installer.
4. Install Location should be placed in the Tor folder in the Huntr directory under "Addons" and replace the current tor file.
5. Make sure the directory is simular to how the preinstalled Tor folder was displayed.



#
###################
LINUX Debian/Ubuntu

Downloading the Huntr Directory:

1. Navigate to the directory where you wish to install Huntr
2. Download the files using Git.

Running Huntr:

1. Navigate to the Huntr directory using your terminal or open a terminal in that directory.
2. Run the tool using "python huntr.py"

Prerequisites:
- Nmap: sudo apt-get install nmap.
- Tor: sudo apt-get install tor
- Python: sudo apt install python3
  - Most Linux distributions come with Python pre-installed. If not, install it using your package manager.

Installing Nmap on Linux:

1. Open the terminal.
2. Simply type "sudo apt-get update" to update your package list.
3. Enter sudo "apt-get install nmap" to install Nmap.
4. Once the installation is complete, type nmap and press Enter in the terminal. If Nmap is installed correctly, you should see its version details and usage options.

Installing Python:
1. Open the terminal.
2. Kali Linux usually comes with Python pre-installed. However, to ensure you have the latest version, type "sudo apt-get update"
3. If you dont have Python installed use "sudo apt-get python3".
4. To verify the installation, enter "python3 --version" in the terminal. This command should display the Python version you installed, confirming that Python was successfully installed.

Installing Tor:
1. Open the terminal.
2. Update your repositories and package list with "sudo apt-get update"
3. Install Tor using "sudo apt-get install tor"
4. To verify you have installed Tor type in your terminal "which tor", you should see the location it has installed to if this didnt work seek online help.


#
#####################################################
Recon-ng Windows Installation

1. **Install or Enable Windows Subsystem for Linux (WSL):**
   - Open PowerShell as Administrator and run:
     ```
     wsl --install
     ```
or

   - Search "Turn Windows Features on or off"

[RESTART REQUIRED]

2. **Install a Linux Distribution:**
   - Go to the Microsoft Store.
   - Search for and install Ubuntu.
   - Run the ubuntu enviroment you have installed

3. **Set up Linux Distribution:**
   - Once installed, launch the Linux distribution from the Start Menu.
   - [IMPORTANT] Set the username to "ubuntu" to make sure Huntr knows where to execute it
   - Complete the initial setup by creating a user and setting a password.


4. **Update & Upgrade:**
   - Run the following commands to update the package list and upgrade existing packages:
     ```
     sudo apt update && sudo apt upgrade -y
     ```

5. **Install Recon-ng:**
   - Run the following commands:
     ```
     sudo apt install recon-ng
     ```

Now when you type "start" in the recon-ng feature it will open a ubuntu command prompt where u can interact with recon-ng

Follow some online tutorials on how to set it up and install your modules

#####################################################
Recon-ng Kali Linux Installation


1. **Update & Upgrade:**
   - Update the package list and upgrade existing packages using:
     ```
     sudo apt update && sudo apt upgrade -y
     ```

2. **Install Recon-ng:**
   - Simply run:
     ```
     sudo apt install recon-ng
     ```

Now when you type "start" in the recon-ng feature it will open a new terminal where u can interact with recon-ng.

Follow some online tutorials on how to set it up and install your modules

To shut down recon-ng make sure to type exit when you are ready
_____________________________________________________________________________________________________________________________________________________________________________________________________________
*******
UPDATES
*******

Keeping Huntr up-to-date ensures you're utilizing the latest features and security patches. Check for updates regularly to maintain an optimal experience.

As I am a begginer and do not have the skills currently to add an "check for updates" feature yet, for now you would have to:

1. Reinstall the Huntr directory from Github and place it in the same location
2. If you installed Tor yourself on windows make sure to add it to the Addons/Tor folder again.
3. You can then run the updated version with "python huntr.py"

If an update is available, you are not required but is it optional as a new version could have implimented features and bug fixes.
_____________________________________________________________________________________________________________________________________________________________________________________________________________
***************************
FEEDBACK AND REPORTING BUGS
***************************

I Value feedback from the users and are committed to improving Huntr based on your experiences and suggestions. Should you encounter any bugs or issues, please help me make the tool better by reporting them.

1. Feedback:
   - For general feedback, suggestions, or inquiries, reach out to me on Github.

2. Reporting Bugs:
   - Please submit a in-depth submission on the github in the "Issues" section. 
   - Please include the following details in your report:
     - Your Operating System and its version.
     - The version of Huntr you're using.
     - A step-by-step guide to reproduce the bug or issue.
     - Screenshots or screen recordings, if possible.
     - Any error messages you received.
   - The more detailed your report, the faster I can diagnose and address the issue.

3. Response Time:
   - I will aim to respond to feedback and bug reports within 48 hours. However, resolution times for bugs can vary based on the complexity of the issue.

Your collaboration helps me enhance Huntr and serve it's users better. I appreciate your understanding and patience.
_____________________________________________________________________________________________________________________________________________________________________________________________________________
********
GLOSSARY
********

1. **Ping Scanner**: A tool that sends ICMP requests to a range of IP addresses to determine if they are "alive" or responsive.

2. **Port Scanner**: A tool that checks for open ports on a networked device.

3. **TheHarvester**: A tool used in the initial phases of penetration testing to gather public information about a target.

4. **Whois Domain/IP Lookup**: A query used to obtain domain or IP ownership, registration details, and other related information.

5. **Reverse DNS Lookup**: A method to determine the hostname associated with a given IP address.

6. **HTTP Headers**: The request and response messages of HTTP, which include details about the requested page, the browser used, server type, etc.

7. **Directory Buster**: A tool that attempts to find hidden directories on a web server.

8. **Hash Identifier**: A tool to recognize various hash types.

9. **Tor**: Free software for enabling anonymous communication on the Internet.

10. **GoPhish**: An open-source tool for creating and monitoring phishing campaigns.

11. **recon-ng**: A Python-based web reconnaissance framework for gathering target data.

If you're unfamiliar with any term, consider further research or seeking educational resources to expand your knowledge.


Dont be a script kiddie.
_____________________________________________________________________________________________________________________________________________________________________________________________________________
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
IMPORTANT DISCLAIMER

Huntr is designed for security professionals to test systems for which they have explicit permission. 

Illegal use of this tool can result in criminal penalties, and the developer will not be held responsible for any unauthorized or illegal use. 

Always ensure that you have proper permissions before conducting any tests. Use Huntr responsibly and ethically.

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
_____________________________________________________________________________________________________________________________________________________________________________________________________________

