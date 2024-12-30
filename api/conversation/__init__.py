from api.conversation.openai_conversations import AzureOpenAIAudioConversations


def executor():
    return AzureOpenAIAudioConversations().handler() 

def audio_download():
    return AzureOpenAIAudioConversations().audio_download() 

