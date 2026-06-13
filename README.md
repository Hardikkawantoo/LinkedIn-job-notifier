Hi, This is a simple python script project that uses jobspy and pandas to scrape job openings from linkedin that have been posted in the last 1 hour and sends it to your email id.
##################################################################################################################################################################################
To run this project yourself you have 2 options:
1. You can either download the script and run it in your local machine with python installed
<img width="1688" height="680" alt="image" src="https://github.com/user-attachments/assets/b8b7adc7-1223-4daa-b32a-4fe897ace858" />





2. Or you can run it in your github actions as a runnable pipline.
<img width="2033" height="1136" alt="image" src="https://github.com/user-attachments/assets/9fd22355-73c2-405f-93b5-39bd4d91551f" />


Steps for running in github actions:
To run this project added these required details in the area here.
<img width="581" height="133" alt="image" src="https://github.com/user-attachments/assets/8a826bab-90fe-4c2b-a0be-3cc554e7bbad" />

Note: It is recommended to not add your details directly into the code as hardcoded values. Instead use the secrets feature in github itself. This will iject your secrets directly in run time to you variales in the python script. [Link](https://docs.github.com/en/actions/concepts/security/secrets)

* For the SENDER_PASSWORD do not add your sender emails actual password. Otherwise google will ban your email request. Get the app password for you email.
* (This step is common for running in your local machine aswell.) [Link](https://support.google.com/mail/answer/185833?hl=en)

Here is how its working for me and Good luck with your job hunt. I know its hard but lets not lose hope and keep trying. :)
<img width="2241" height="1169" alt="image" src="https://github.com/user-attachments/assets/d4b7a0bf-5c42-4d11-81ed-a0bd989dc412" />
