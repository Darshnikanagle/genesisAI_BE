from langchain.chat_models import init_chat_model
import os
from langchain_community.vectorstores.faiss import FAISS
from app.util import llm as model


from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

template = """You are good recruiter. Your task is to precisely review resume based on the provided crieteria and tell if it is being shortlisted or not'. If shortlisted then just return 'Shortlisted' otherwise provide the criteria that are not met. Do not provide any additional explaination in the response.
\n
Example of response for shortlisted:
{{
"file_name": "",
"status": "Shortlisted",
"details": {{
    "Java Technology": "Worked in Java",
    "5 Years experience": "Total 7 years of experience"
}},
"summary": "The candiadate has total 7 years of experience in Java technology."
}}
\n
Example of response for non-shortlisted:
{{
"file_name": "",
"status": "Rejected",
"details": {{
    "Java Technology": "Worked in Java",
    "5 Years experience": "Total 3 years of experience"
}},
"summary": "The candiadate has total 3 years of experience in Java technology."
}}


\n
Resume Content: {content}
\n
crieteria: {crieteria}
"""
prompt_template = ChatPromptTemplate.from_messages(
        [("system", template)]
    )

def screen_resume(content, crieteria):
    try:
        result = prompt_template.invoke({"content": content, "crieteria": crieteria})

        # print(result.to_messages())
        
        print("submitted question to llm, awaiting response")
        response = model.invoke(result.to_messages())
        print("Response received")
        # print(response)
        return response.content

    except Exception as e:
     print(f"An unexpected error occurred: {e}")



# try:


#     file_path = (
#     "C:\\Users\\keshav.varma\\Downloads\\RohitRoteResume.pdf"
# )
    
#     from langchain_community.document_loaders import PyPDFLoader

#     loader = PyPDFLoader(file_path)
#     documents = loader.load()

#     print("total pages:", len(documents))

#     # pages = []
#     # for page in documents:
#     #     pages.append(page)

#     # print(f"{pages[0].metadata}\n")
#     # print(pages[0].page_content)


#     from langchain_community.document_loaders import TextLoader
#     from langchain_text_splitters import RecursiveCharacterTextSplitter

#     # sentence = "This is a test sentence."
#     # embedding = model.encode(sentence)

#     # print(embedding.shape)  # Output: (384,)


#     # Load the document, split it into chunks, embed each chunk and load it into the vector store.
#     # raw_documents = TextLoader('state_of_the_union.txt').load()
#     # text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
#     # documents = text_splitter.split_documents(raw_documents)

#     # print("Embedding model initialized")

#     # text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
#     # documents = text_splitter.split_documents(documents)

#     print("Chunk prepared")

#     # print("initilizing vector db")
#     # vector_db = FAISS.from_documents(documents=documents, embedding=embedding)
#     # print("vector db initilized")
#     # print("Saving vectors into local db")
#     # vector_db.save_local(LOCAL_DB_DIRECTORY)
#     # print("vectors saved successfully")

#     # vector_db = FAISS.load_local(LOCAL_DB_DIRECTORY
#     #         , embeddings=embedding
#     #         , allow_dangerous_deserialization = True
#     #     )
    
#     # retriever = vector_db.as_retriever()

#     # query = "How much IPL contributed to indian GDP in 2015??"
#     # docs = vector_db.similarity_search(query)
   
#     # print("similarity_search\n", docs[0].page_content)


#     # docs = retriever.invoke(query)
#     # print("retriever", docs[0].page_content)

    
    
    

#     content = """ROHIT ANIL ROTE
# Frontend Developer
# 9623891150 rohitrote8806@gmail.com Pune
# SUMMARY
# Skilled Frontend Developer with experience in HTML, CSS, JavaScript, and frameworks like Angular, React, React Native. Focused on
# building responsive, user-friendly interfaces and optimizing performance. Strong collaboration and problem-solving abilities.
# EXPERIENCE
# Frontend Developer, Rabbit And Tortoise Technology Solutions. 08/2022 - Present
# Project: UJD to Tags(Amdocs)
# A web application built using Angular technology, aimed at generating test artifacts through a GenAI model using uploaded
# documents. The application enhances data transformation and visualization, making test artifact generation more efficient.
# Responsibilities:
# Developed a web application for automating test case generation from user journey documents ( UJD) , reducing manual effort
# and improving efficiency.
# Implemented OAuth for secure third-party authentication in the project
# Designed and implemented a component-based architecture in Angular to ensure scalability, reusability, and modularity of the
# application
# Enabled users to:
# Upload documents and generate test cases dynamically.
# Visualize test cases in a tabular format with options for manual editing.
# Export test cases as Excel files, streamlining test management processes.
# Collaborated with backend developers to integrate APIs for seamless document processing and data retrieval.
# Deployed the application on an IIS server, ensuring a stable and accessible hosting environment.
# Focused on creating a user-friendly interface to simplify workflows and enhance usability.
# Project: Ask Lisa Use Case(Amdocs)
# A web application built using Angular technology, focused on providing graphical representation of employee data for analytical
# purposes.
# The application leverages the NG2 Charts library to create interactive and visually appealing charts, simplifying data interpretation
# and enabling better decision-making.
# Responsibilities:
# Designed and developed a web application for graphical representation of data using Angular, enabling users to analyze data
# through interactive visualizations.
# Built component-based architecture to ensure reusability, scalability, and maintainability of code.
# Implemented various charts including line, bar, pie, multiline, doughnut, histogram, and scattered charts to cater to diverse data
# analysis requirements
# Utilized NG2 Charts and Chart.js libraries to create dynamic and customizable chart components.
# Managed application state efficiently using NGXS Store, improving data flow and reducing complexity in the application.
# Worked closely with stakeholders to gather requirements, incorporate feedback, and deliver user-focused solutions.

# Project: Quality Management System (Internal)
# A web application built in React.js designed to streamline quality processes and ensure compliance with industry standards. The
# system facilitates efficient tracking, documentation, and reporting of quality issues, audits, and corrective actions.
# Responsibilities:
# Designed intuitive UI to enhance user experience and facilitate seamless navigation.
# Integrated APIs to implement essential functionalities for effective data management.
# Developed multiple features, including:
# Organizing meetings for different users.
# Calendar view for scheduled meetings.
# Audit calendar for tracking quality compliance.
# Collaborated with cross-functional teams to ensure alignment with project goals and user needs.
# Deployed the application on an AWS EC2 instance, ensuring high availability, scalability, and secure access.
# •
# www.enhancv.com Powered by
# :
# :
# :
# EXPERIENCE
# Project: Pheal Care Mobile Application (Pheal Care India)
# Comprehensive cross-platform mobile application ( Android and iOS) that connects patients with qualified physiotherapists. The app
# provides users with personalized physiotherapy care, improving health outcomes through seamless patient-therapist interactions.
# Equipped with innovative features to enhance engagement and streamline healthcare processes.
# Responsibilities:
# Developed a cross-platform mobile application for physiotherapists using React Native to support both Android and iOS
# platforms, improving accessibility for users.
# Built the admin portal for managing the application’s data and operations using React.js, ensuring ease of use and efficient
# management of patient and hospital details.
# Implemented key features including:
# Doctors registration and profile management for seamless onboarding.
# Digitalized prescriptions for physiotherapy treatments, improving patient care accuracy and ease of access.
# Hospital management system with QR code attendance, streamlining patient tracking and attendance records.
# Integrated Razorpay payment gateway for secure, efficient, and smooth payment transactions.
# Configured push notifications to keep patients and physiotherapists updated on appointments and activities.
# Deployed the mobile app on Google Play Store and Apple App Store, ensuring a smooth release process and handling the
# necessary configurations for successful deployment.
# Collaborated with backend developers to integrate APIs, enabling efficient data flow between the app and the server.
# Focused on enhancing the user experience by implementing responsive layouts, intuitive navigation, and interactive features.
# •
# •
# EDUCATION
# BSc Computer Science
# Marathwada Mitra Mandal's College (Pune University) 2017 - 2020
# MSc Computer Application
# Modern Collage,Ganeshkhind (Pune University) 2020 - 2022
# SKILLS
# Frontend Html, css, JavaScript, TypeScript, React JS, React Native, Angular, Next JS
# Backend Node JS, Express JS
# Database MySQL , MongoDB
# COURSES
# MERN Stack Certification (8 Months)Institute: Seven
# Mentors Pvt Ltd, Pune 411005
# LANGUAGES
# English Hindi Marathi
# """

#     crieteria = """2 Years of experience, Angular developer 
# """


    
    
# except Exception as e:
#      print(f"An unexpected error occurred: {e}")
