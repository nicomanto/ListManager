class Message:
    commandSend = '"invia la lista nome lista al bot telegram"'
    commandConfiguration = '"configurazione"'
    reprompt = "Vuoi provare?"

    def open(self):
        return f"Benvenuto. Se è la prima volta che utilizzi questa skill, puoi utilizzare il comando {self.commandConfiguration} per collegare Alexa al bot ListManager"

    def help(self):
        return f"Per inviare una lista al bot telegram usa il comando {self.commandSend}"

    def fallback(self):
        return f"Non ho capito bene. {self.helpMessagge()}"

    def stop(self):
        return "Ciao ciao"

    def error(self):
        return "Houston, abbiamo un problema. Riprova più tardi"

    def errorTG(self):
        return f"Sembra che il bot ListManager non risponda, controlla che non sia bloccato. In caso contrario, prova a reimpostare l'identificativo del bot tramite il comando {self.commandConfiguration}"

    def errorChatIDNotSetted(self):
        return f"Sembra che non sia stato collegato il bot ListManager ad Alexa, pronuncia il comando {self.commandConfiguration}"

    def sentList(self, listName):
        return f'Lista "{listName}" inviata al bot'

    def errorListNotFound(self, listName):
        return f"Lista \"{listName}\" non presente nell'app Alexa"

    def configurationSuccess(self):
        return f"Alexa è stata collegata correttamente al bot ListManager"

    def configurationFailed(self):
        return f"Non è stato possibile collegare Alexa al bot ListManager, riprova più tardi"
