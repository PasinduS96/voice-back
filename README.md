# Oral Interview Evaluation System - Backend


[![GPL License][license-shield]][license-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]

# Smart Interviewing System
## Project Description
Nowadays, almost everything is equipped with technology. People can save time by using modern day technological applications in the most convenient way. Smart Interviewing System is one such software/tool which automates the traditional interviewing process using modern Natural Language Processing techniques and deep learning applications. The system will be mainly beneficial for interviewers and HR management employees working for different organizations who conduct technology related interviews. The system works with human voice and writing patterns. The system converts human language into system understandable text-based inputs, and these are used as inputs in the automated interviewing process. The system then checks the accuracy of the answers which candidates provided on the both oral interviews/ technical interviews and written tests. Later, the system automatically predicts scores for each answer using concepts of the deep learning. Interviewers can reduce the effort that they have to put in for selecting the most suitable candidates who are qualified enough to work with their organization. SIS is developed based on modern DL and NLP concepts using Python programming language alongside with ReactJS Framework. This system checking and evaluating candidate more accurately in every stage of the interview using advance evaluation parameters than human oriented evaluations. Above process lead system to find more human errors which critically can be affected to future of the organizations. Because of that, it can be led organizations to find best human resources comparing to the traditional interviewing process by sacrificing less time and effort.

## System Diagram 
![System Diagram](https://i.imgur.com/CEVmIAX.png)

## Main Research Problem :

Developing countries, such as Sri Lanka, heavily depends on their work force. People are employed in different industries in order to build a stronger economy. Recently, IT industry started getting more recognition inside Sri Lanka. As the “Sri Lanka Startup Report 2019” provided by the SLASSCOM indicates, Sri Lanka rose 11 places in the World Bank’s 2019 “Doing Business index” and now ranks 100 among 190 economies in the ease of doing business (13th in Asia) and 83rd in “Starting a business” index. Even before 2019, Sri Lanka was a great place to start businesses. Successful companies such as Creately, Wow.lk, Pickme and 4Axis Solutions shows how easier it was to start a business in Sri Lanka.

Above companies do their business in different areas such as transport, software development and e-commerce. They basically need people who knows different and newer technologies working under them in order to continue to grow their businesses. Apart from that, if we consider IFS, a multinational enterprise software company, recently shifted about 60% of their Research & Development section to Sri Lanka. CEO of IFS even stated that “We would not be where we are today without Sri Lanka” during an interview. This statement indicates how important the IT industry in Sri Lanka. 

Starting new companies, expanding existing companies require new employees. Currently, IT industry in Sri Lanka is experiencing this. Large number of candidates are recruited every day. This recruitment process includes interviews in order to evaluate the candidates. Traditional interviews completely depend on humans. Hence, the mistakes can be made and sometimes candidates who should not be hired might be recruited and the ones who should be hired can be left out. As an example, if the interviewer has a personal or work-related problem in their mind while evaluating a candidate, this might affect the candidate’s evaluation process.

Also, sometimes the interviewers tend to ask their interviewees questions that are more relevant to their operations within the company. Most of the times, these questions can be unfair towards interviewees since they might not have an idea about how companies operate since most of the companies do not let outside people to know their inside information. Hiring a candidate that is not suitable can affect badly and leaving out a suitable candidate as a mistake is not fair for the candidate and a loss for company.

In order to avoid this problem, different researches have been conducted and different software solutions have been proposed. But none of them are completely automated processes and there are chances of occurring human errors.

## Main Objective :

The purpose of this research is to find a method to conduct interviews, which would require less human involvement. An interview basically has few stages where a candidate is evaluated based on their technical knowledge and candidate is evaluated based on their personal traits. The decided idea is to divide the interview process into 4 stages and automate each of these phaces.

1. Vocal Interview
2. Technical Interview - Written exam
3. Candidate Categorization
4. HR Interview

---

# Individual Research Components:

## Voice Interview / Oral Interview

### Objective:

As it is explained in the overall objective of the research, objective of the first component is to automate the vocal interview in order to minimize the human prone errors.

### Description: 

As a solution to 1st phase, interviewees must face a oral interview. During the interview, interviewees will be asked questions to evaluate their technical knowledge. The answers to these technical questions offered by the interviewees will be evaluated by the system. To do so, our program will use keyword checks to analyze the content of their responses.

This component will be built on the basis of NLP techniques where we hope these measures will be applied one by one;

> Creating a voice detector & extracting preferred voice output for other dependable components.

> Extract important data such as personal information and suitable areas.

> Choose random questions from a pre-defined collection.

> Evaluate answers by matching keywords using voice inputs.

After the voice inputs are taken in as texts the words will be vectorized using Doc2Vec model. After that, using cosine similarity method, word similarities will be checked. Word similarity is checked to see the accuracy of the answers provided by the interviewee. The results will be stored in a No-SQL database, because there are many unstructured data to be saved for future uses. MongoDB Atlas is used as the database of the system. Also, collected voice input data will be used to detect specific keywords related to different working areas. This keyword detection will be mostly based on examples the candidate use to explain software engineering theories or applications. These keywords will also be stored in the database and later will be used by the third component.

During the training of the model, a pipeline has been used since CountVectorizer and Tf-Idf Transformer is also used. Below code snippet is used to train the model.

```python
txt_cls = Pipeline([('C_vec', CountVectorizer()),
                    ('Tfid_trans', TfidfTransformer()),
                    ('classf', MultinomialNB())])

txt_cls.fit(train.data, train.target)
```
---
# Front End Project
## Folder Structure
Folder structure used during the implementation of front-end of the application is displayed below.
```bash
Frontend
│
├───public
└───src
     ├───api
     ├───images
     ├───Pages
     │   └───extra
     └───Partials
```
- **api** : api folder contains all the API calls.
- **images** : images folder contains all the images.
- **Pages** : created interface are in Pages folder.
- **extra** : extra folder contains the re-used react components.
- **Partials** : Partials folder also contains re-used react components.

## Execution

**Download Dependencies** : ```node install```

**Start FrontEnd Project** : ```npm start```

To use the application, open [http://localhost:3000](http://localhost:3000) from your web browser.

---
# Back End Project

Each component has its own server-side projects. All of the 4 projects needs to be executed in order to work with all 4 components.

## Execution


>Open project using pyCharm

>Install Dependencies - ```pip install -r requirements.txt```

>Run Project Using "Run" button
---
# Dependencies

|Front End|Back End|
|:--|:--|
|@coreui/coreui: ^3.3.0|aniso8601==8.0.0|
|@coreui/react: ^3.3.0|click==7.1.2|
|@material-ui/core :  ^4.11.0 |flask==1.0.2|
|@testing-library/jest-dom :  ^4.2.4|Flask-Cors==3.0.9|
|@testing-library/react :  ^9.3.2|Flask-PyMongo==2.3.0|
|@testing-library/user-event :  ^7.1.2|Flask-RESTful==0.3.8|
|bootstrap :  ^4.5.2|gunicorn==19.9.0|
|react :  ^16.13.1|itsdangerous==1.1.0|
|react-bootstrap :  ^1.3.0|Jinja2==2.11.2|
|react-dom :  ^16.13.1|joblib==0.14.1|
|react-icons :  ^3.11.0|MarkupSafe==1.1.1|
|react-loader-spinner :  ^3.1.14|numpy>=1.15.0|
|react-router-dom :  ^5.2.0|pandas>=0.23.3|
|react-scripts :  3.4.3|pymongo==3.11.0|
|reactstrap :  ^8.6.0|python-dateutil==2.8.1|
|recharts :  ^1.8.5|pytz==2020.1|
|uuid :  ^8.3.0|scikit-learn>=0.19.1|
|mdbreact :  ^4.27.0|scipy>=1.1.0|
|axios :  ^0.20.0|six==1.14.0|
|react-alert :  ^7.0.2|sklearn==0.0|
|react-alert-template-basic :  ^1.0.0|textdistance==4.2.0|
|react-component-countdown-timer :  ^0.1.8|utils==1.0.1|
|react-animated-text :  ^0.1.4|Werkzeug==1.0.1|
|react-sidebar :  ^3.0.2|requests==2.20.0|
|react-sidemenu :  ^1.1.0|SpeechRecognition==3.8.1|
||bcrypt==3.1.7|
||bson==0.5.9|
||certifi==2020.6.20|
||DateTime==4.3|
||pycparser==2.20|
||zope.interface==5.1.0|
---



[license-shield]: https://img.shields.io/github/license/PasinduS96/voice-back?style=for-the-badge
[license-url]: https://github.com/PasinduS96/voice-back/blob/main/LICENSE
[forks-shield]: https://img.shields.io/github/forks/PasinduS96/voice-back?style=for-the-badge
[forks-url]: https://github.com/PasinduS96/voice-back/network/members
[stars-shield]: https://img.shields.io/github/stars/PasinduS96/voice-back?style=for-the-badge
[stars-url]: https://github.com/PasinduS96/voice-back/stargaze

