from openai import OpenAI

class SendRequest:
    def __init__(self, theKey):
        self.client = OpenAI(
            api_key = theKey
        )

        # {"role" : "system", "content" : "sysPrompt"}
        self.chatHistory = []
        self.startingPrompt = "You are a D&D host. If there are more instructions, read those and continue the story as the player responds. If there are not, guide the player in a new D&D journey by making their character, setting the world, and so on. Teach the player when they ask. Instructions: "
        self.setChatHistory(self.startingPrompt)

    def setChatHistory(self, sysPrompt):
        self.chatHistory = [{"role" : "system", "content" : sysPrompt}]

    def sendResponseWithHistory(self, userPrompt):
        self.chatHistory.append({"role" : "user", "content" : userPrompt})
        response = self.client.chat.completions.create(
            model="gpt-4o-2024-08-06",
            messages = self.chatHistory
        )
        self.chatHistory.append({"role" : "assistant", "content" : response.choices[0].message.content})

        return response.choices[0].message.content

    def summarizeCurrentStory(self, sysPrompt):
        newText = self.sendResponseWithHistory("Summarize the current character and storyline so far into text form, as you will have continue the story as a DND host without prior knowledge of the current events. Make sure to get all of the important parts of the character and story such as character stats, weapons, items as well as the current story line.")
        self.setChatHistory([{"role" : "system", "content" : sysPrompt + newText}])
