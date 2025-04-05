import handler
import json
import streamlit as st

"""
# External Average Testing (EAT).
EAT is a fun, little website that you can use to send funny, short forms to your friends, with ChatGPT capabilities. 
"""

# new code:
# new session state variable location keeps track of locations

# setup
if not "client" in st.session_state:
    apiKey = st.text_input("API Key")
    apiPress = st.button("Set client:")
    if apiPress:
        st.session_state["client"] = handler.SendRequest(apiKey)
        st.session_state["location"] = "Menu"
        st.session_state["data"] = {"questions" : [], "qType" : [], "options" : []}
        st.rerun()

def displayQuiz(isEdit):
    # ["questions"] is the question text in json list
    # ["qType"] is the question type in json list
    # ["options"] is the options for only select boxes (which is a list) in json list
    if (isEdit): st.text("----PREVIEW----")
    topText = st.text("The Quiz: ")
    answerBoxes = []

    for i in range(len(st.session_state["data"]["questions"])):
        if st.session_state["data"]["qType"][i] == "selectbox":
            # add options to select box
            answerBoxes.append(st.selectbox(st.session_state["data"]["questions"][i], st.session_state["data"]["options"][i], key=i))
        elif st.session_state["data"]["qType"][i] == "text_input":
            answerBoxes.append(st.text_input(st.session_state["data"]["questions"][i], key=i))
    
    st.session_state["answerBoxes"] = answerBoxes

    bottomText = st.text("Wow, you finished the quiz!")
    if (isEdit): st.text("----END OF PREVIEW----")

def editQuiz():
    # display quiz
    displayQuiz(True)

    editMessage = st.selectbox("Do you want to insert a question, delete a question, or exit to the Menu.", ["Insert", "Delete", "Menu"])
    editButton = st.button("Enter.", key="e2")

    if editButton:
        st.session_state["locationEdit"] = editMessage
    
    if not "locationEdit" in st.session_state: return
    if st.session_state["locationEdit"] == "Insert":
        insertText = st.text_input("What will your new question ask?")
        insertType = st.selectbox("Is it a dropdown menu or a free response?", ["text_input", "selectbox"])
        insertOptions = st.text_input("Write all your dropdown options (LEAVE BLANK IF FREE RESPONSE) seperated with spaces.")

        insertLocation = [str(i+1) for i in range(len(st.session_state["data"]["questions"]) + 1)]
        insertMessage = st.selectbox("Which question number is it? It will make space to place the question by moving others.", insertLocation)

        insertButton = st.button("Enter.", key="e3")
        if insertButton:
            dropMenuStuff = insertOptions.split()
            dropMenuStuff.insert(0, "")
            st.session_state["data"]["questions"].insert(int(insertMessage) - 1, insertText)
            st.session_state["data"]["qType"].insert(int(insertMessage) - 1, insertType)
            st.session_state["data"]["options"].insert(int(insertMessage) - 1, dropMenuStuff)
            st.rerun()
    elif editMessage == "Delete":
        delOptions = [str(i+1) for i in range(len(st.session_state["data"]["questions"]))]
        delMessage = st.selectbox("Which question are you going to delete?", delOptions)
        delButton = st.button("Enter.", key="e4")

        if delButton:
            st.session_state["data"]["questions"].pop(int(delMessage) - 1)
            st.session_state["data"]["qType"].pop(int(delMessage) - 1)
            st.session_state["data"]["options"].pop(int(delMessage) - 1)
            st.rerun()
    elif editMessage == "Menu":
        st.session_state.pop("locationEdit")
        st.session_state["location"] = "Menu"
        st.rerun()

def answerQuiz():
    displayQuiz(False)

    finishButton = st.button("Finish.")
    if finishButton:
        print(st.session_state["answerBoxes"])
        st.session_state["location"] = "Menu"
        st.rerun()

# make it so that button presses are change the location variable so that everything does not restart everytime you click something
if "location" in st.session_state:
    if st.session_state["location"] == "Menu":
        userMessage = st.selectbox("Do you want to clear the quiz, load a quiz, save the quiz, edit the quiz, or answer the quiz?", ["Clear", "Load", "Save", "Edit", "Answer"])
        enterButton = st.button("Enter.", key="e1")

        if (enterButton):
            if userMessage == "Clear":
                st.session_state["data"] = {"questions" : [], "qType" : [], "options" : []}
                st.rerun() # will immediately rerun
            elif userMessage == "Load":
                quizJSON = open("quiz.json", "r")
                st.session_state["data"] = json.loads(quizJSON.read())
                st.rerun()
            elif userMessage == "Save":
                quizJSON = open("quiz.json", "w")
                quizJSON.write(json.dumps(st.session_state["data"]))
                st.rerun()
            st.session_state["location"] = userMessage
            st.rerun()
    elif st.session_state["location"] == "Edit": editQuiz()
    elif st.session_state["location"] == "Answer": answerQuiz()